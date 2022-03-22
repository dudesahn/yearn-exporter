from collections import defaultdict
from datetime import datetime

from brownie import chain, web3
from rich import print
from rich.progress import track
from rich.table import Table
from web3._utils.events import construct_event_topic_set
from yearn.prices.magic import get_price
from yearn.utils import contract
from brownie.exceptions import ContractNotFound


def main():
    print("We've started")
    if chain.id == 1:
        from_block = 12059089
        dai = contract("0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    else:
        from_block = 29418132 # Fantom, ~1000 blocks before I got my first rewards
        dai = contract("0xF137D22d7B23eeB1950B3e19d1f578c053ed9715")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    print(f"Starting from block {from_block}")

    print(f"abi: {dai.events.Transfer().abi}")
    topics = construct_event_topic_set(
        dai.events.Transfer().abi,
        web3.codec,
        {'receiver': ['0x0']},
    )
    logs = web3.eth.get_logs(
        {'topics': topics, 'fromBlock': from_block, 'toBlock': chain.height}
    )

    events = dai.events.Transfer().processReceipt({'logs': logs})
    income_by_month = defaultdict(float)

    for event in track(events):
        ts = chain[event.blockNumber].timestamp
        token = event.address

        if chain.id == 1:
            # skip scam tokens or repeated ones we know aren't vault tokens
            to_skip = [
                "0xfFA55849a7309C7f4fB4De88d804fD546A66C271",  # scam token dydex
                "0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C",  # BNT
                "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
                "0x5282a4eF67D9C33135340fB3289cc1711c13638C",  # Iron Bank pool token
                "0x48Fb253446873234F2fEBbF9BdeAA72d9d387f94",  # vBNT
                "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
                "0x2aECCB42482cc64E087b6D2e5Da39f5A7A7001f8",  # RULER (lol)
                "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
                "0x99D8a9C45b2ecA8864373A26D1459e3Dff1e17F3",  # MIM
                "0x6Df2B0855060439251fee7eD34952b87b68EeEd9",  # ruler wbtc token
                "0xf085c77B66cD32182f3573cA2B10762DF3Caaa50",  # ruler weth token
                "0xe1237aA7f535b0CC33Fd973D66cBf830354D16c7",  # ruler DAI token
                "0x8781407e5acBB728FF1f9289107118f8163880D9",  # ruler DAI token 2
                "0xA3D87FffcE63B53E0d54fAa1cc983B7eB0b74A9c",  # sETH pool token
                "0x06325440D014e39736583c165C2963BA99fAf14E",  # stETH pool token
                "0x5a6A4D54456819380173272A5E8E9B9904BdF41B",  # MIM pool token
                "0x4E15361FD6b4BB609Fa63C81A2be19d873717870",  # FTM
                "0x96E61422b6A9bA0e068B6c5ADd4fFaBC6a4aae27",  # ibEUR
                "0x19b080FE1ffA0553469D20Ca36219F17Fcf03859",  # ibEUR+sEUR-f
                "0xB01371072fDcB9B4433b855e16A682B461F94AB3",  # anyFTM
                "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",  # YFI
                "0x090185f2135308BaD17527004364eBcC2D37e5F6",  # SPELL
                "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
                "0x2e9d63788249371f1DFC918a52f8d799F4a38C94",  # TOKE
                "0x5Fa464CEfe8901d66C09b85d5Fcdc55b3738c688",  # Uni v2 pool
                "0x1b429e75369EA5cD84421C1cc182cee5f3192fd3",  # uni v2 crap
                "0xc770EEfAd204B5180dF6a14Ee197D99d808ee52d",  # FOX
                "0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B",  # FRAX3CRV-f
                "0x853d955aCEf822Db058eb8505911ED77F175b99e",  # FRAX
                "0x57Ab1ec28D129707052df4dF418D58a2D46d5f51",  # sUSD
            ]
            if token in to_skip:
                print("\nNon-vault token from our list to skip")
                continue

        token_contract = contract(token)

        try:
            token_contract.apiVersion()
        except:
            print(
                "\n",
                token_contract.symbol(),
                token,
                "is not a vault token and shouldn't be counted",
            )
        src, dst, amount = event.args.values()

        # ignore income from addresses we know weren't fee distros. mainly other transfers and mints.
        addresses_to_ignore = [
            "0x677Ae1C4FDa1A986a23a055Bbd0A94f8e5b284De",  # deposited test to ib vault here, then sent over
            "0x0000000000000000000000000000000000000000",  # burn/mint address
            "0x25B28EE7f335F0396f41f129039F1583345B21b8",  # dudesahn.eth
        ]
        if src in addresses_to_ignore:
            print("\nNot a fee distro, skip")
            continue

        try:
            amount /= 10 ** contract(token).decimals()
        except (ValueError, ContractNotFound, AttributeError):
            continue

        try:
            price = get_price(event.address, block=event.blockNumber)
        except:
            print("\nPricing error for", token_contract.symbol(), "on", token_contract.address, "****************************************")
            print(f"Amount: {amount}")
            continue
        print("\nToken Symbol:", token_contract.symbol())
        print(f"Amount: {amount}")
        print(f"Price: {price}")
        month = datetime.utcfromtimestamp(ts).strftime('%Y-%m')
        income_by_month[month] += amount * price

    table = Table()
    table.add_column('month')
    table.add_column('income')
    for month in sorted(income_by_month):
        table.add_row(month, f'{income_by_month[month]:,.0f}')

    print(table)
    print(sum(income_by_month.values()))
