from bisect import bisect_left
from datetime import datetime, timedelta
from yearn.v2.vaults import Vault as VaultV2
from semantic_version.base import Version

from yearn.apy.common import (
    Apy,
    ApyError,
    ApyPoints,
    ApyFees,
    ApySamples,
    SharePricePoint,
    calculate_roi,
)


def aggregate(vault, samples: ApySamples) -> Apy:
    harvests = sorted(
        [harvest for strategy in vault.strategies for harvest in strategy.harvests]
    )

    # set our parameters
    contract = vault.vault
    price_per_share = contract.pricePerShare

    # calculate our current price
    now_price = price_per_share(block_identifier=samples.now)

    # get our inception data
    inception_price = 10 ** contract.decimals()
    inception_block = harvests[:2][-1]

    if now_price == inception_price:
        raise ApyError("v2:inception", "no change from inception price")

    # check our historical data
    if samples.week_ago > inception_block:
        week_ago_price = price_per_share(block_identifier=samples.week_ago)
    else:
        week_ago_price = inception_price

    if samples.month_ago > inception_block:
        month_ago_price = price_per_share(block_identifier=samples.month_ago)
    else:
        month_ago_price = inception_price

    now_point = SharePricePoint(samples.now, now_price)
    week_ago_point = SharePricePoint(samples.week_ago, week_ago_price)
    month_ago_point = SharePricePoint(samples.month_ago, month_ago_price)
    inception_point = SharePricePoint(inception_block, inception_price)

    week_ago_apy = calculate_roi(now_point, week_ago_point)
    month_ago_apy = calculate_roi(now_point, month_ago_point)
    inception_apy = calculate_roi(now_point, inception_point)

    strategy_fees = []
    keep_crv = 0
    now_apy = 0
    is_curve = False
    boost = 0
    pool_apy = 0
    base_apr = 0
    boosted_apr = 0
    reward_apr = 0
    cvx_apr = 0
    # generate our average strategy APY and get our fees
    for strategy in vault.strategies:
        total_debt_ratio_allocated = vault.vault.debtRatio()
        if total_debt_ratio_allocated > 0:
            debt_ratio = (
                contract.strategies(strategy.strategy)['debtRatio']
                / total_debt_ratio_allocated
            )
        else:
            debt_ratio = 0
        strategy_apy = strategy.apy.net_apy
        now_apy += debt_ratio * strategy_apy
        performance_fee = contract.strategies(strategy.strategy)['performanceFee']
        proportional_fee = debt_ratio * performance_fee
        strategy_fees.append(proportional_fee)

        # aggregate our data for curve vaults
        if strategy.apy.fees.keep_crv != None:
            is_curve = True
            keep_crv += strategy.apy.fees.keep_crv * debt_ratio
            boost += strategy.apy.composite["boost"] * debt_ratio
            pool_apy += strategy.apy.composite["pool_apy"] * debt_ratio
            base_apr += strategy.apy.composite["base_apr"] * debt_ratio
            boosted_apr += strategy.apy.composite["boosted_apr"] * debt_ratio
            reward_apr += strategy.apy.composite["rewards_apr"] * debt_ratio
            cvx_apr += strategy.apy.composite["cvx_apr"] * debt_ratio

    composite = {
        "boost": boost,
        "pool_apy": pool_apy,
        "base_apr": base_apr,
        "boosted_apr": boosted_apr,
        "rewards_apr": reward_apr,
        "cvx_apr": cvx_apr,
    }

    # use the first non-zero apy, ordered by precedence
    apys = [now_apy, week_ago_apy, month_ago_apy]
    two_months_ago = datetime.now() - timedelta(days=60)
    if contract.activation() > two_months_ago.timestamp():
        # if the vault was activated less than two months ago then it's ok to use
        # the inception apy, otherwise using it isn't representative of the current apy
        apys.append(inception_apy)

    net_apy = next((value for value in apys if value != 0), 0)

    strategy_performance = sum(strategy_fees)
    vault_performance = (
        contract.performanceFee() if hasattr(contract, "performanceFee") else 0
    )
    management = contract.managementFee() if hasattr(contract, "managementFee") else 0
    performance = vault_performance + strategy_performance

    performance /= 1e4
    management /= 1e4

    # assume we are compounding every week
    compounding = 52

    # calculate our APR after fees
    # if net_apy is negative no fees are charged
    apr_after_fees = (
        compounding * ((net_apy + 1) ** (1 / compounding)) - compounding
        if net_apy > 0
        else net_apy
    )

    # calculate our pre-fee APR
    gross_apr = apr_after_fees / (1 - performance) + management

    # 0.3.5+ should never be < 0% because of management
    if net_apy < 0 and Version(vault.api_version) >= Version("0.3.5"):
        net_apy = 0

    points = ApyPoints(now_apy, week_ago_apy, month_ago_apy, inception_apy)
    fees = ApyFees(performance=performance, management=management, keep_crv=keep_crv)

    if is_curve:
        return Apy(
            "v2:aggregate", gross_apr, net_apy, fees, points=points, composite=composite
        )

    else:
        return Apy("v2:aggregate", gross_apr, net_apy, fees, points=points)
