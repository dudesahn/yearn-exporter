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
from yearn.events import get_logs_asap
from hexbytes import HexBytes
import pandas as pd


def main():
    print("We've started")

    # ADD YOUR ADDRESSES HERE
    dudesahn = [
        '0x25B28EE7f335F0396f41f129039F1583345B21b8',
        '0x986176Df2e9dC6225DfB498D1869ABA04893dcE1',
        '0x8Ef63b525fceF7f8662D98F77f5C9A86ae7dFE09',
    ]

    my_wallets = dudesahn
    print("Current chain height:", chain.height)
    dates = []
    tx_ids = []
    symbols = []
    prices = []

    if chain.id == 1:
        from_block = 5580662
        # first block for dudesahn, 5580662
        dai = contract("0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    else:
        from_block = 4306100
        # 8042204 poolpi's date
        # 29418132 ~1000 blocks before I got my first rewards on Fantom
        # 17994789 midday 9-30-21
        # 4306100, 100k before my first tx that shows up on ftmscan, but there are 4 more pages, maybe error tho

        dai = contract("0x0DEC85e74A92c52b7F708c4B10207D9560CEFaf0")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    print(f"Starting from block {from_block}")

    print(f"abi: {dai.events.Transfer().abi}")

    topics = construct_event_topic_set(
        dai.events.Transfer().abi,
        web3.codec,
        {'sender': my_wallets},
    )

    logs = get_logs_asap(topics, None, from_block, chain.height, 1)

    print(f"Logs fetched. size = {len(logs)}")
    events = dai.events.Transfer().processReceipt({'logs': logs})
    income_by_month = defaultdict(float)

    if chain.id == 1:
        # skip scam tokens or repeated ones we know aren't vault tokens
        # mainly do this to save time or tokens that crash the script
        to_skip = [
            "0x34278F6f40079eae344cbaC61a764Bcf85AfC949",  # scam token FF9
            "0xfFA55849a7309C7f4fB4De88d804fD546A66C271",  # scam token dydex
            "0xF9d25EB4C75ed744596392cf89074aFaA43614a8",  # scam token up1
            "0xED196D746493bC855f95Ce5346C0161F68DB874b",  # SHIK
            "0x82dfDB2ec1aa6003Ed4aCBa663403D7c2127Ff67",  # akSwap.io
            "0x908599FDf490b73D171B57731bd4Ca95b7F0DE6a",  # scam
            "0x74232704659ef37c08995e386A2E26cc27a8d7B1",  # STRK
        ]
    elif chain.id == 250:
        to_skip = [
            # FTM
            "0x2F96f61a027B5101E966EC1bA75B78f353259Fb3",  # TNGLv3
            "0x87e377820010D818aA316F8C3F1C2B9d025eb5eE",  # spam
            "0xe826F3C308aEB14cF901e19af1E5a0f7E73b625C",  # scam token
        ]

    for event in track(events):
        ts = chain[event.blockNumber].timestamp
        token = event.address
        # print("\nToken address:", token)  # use this for debugging when we crash on a token

        if token in to_skip:
            print("Non-vault token from our list to skip")
            continue

        src, dst, amount = event.args.values()
        tx_hash = event.transactionHash.hex()

        try:
            token_contract = contract(token)
            amount /= 10 ** contract(token).decimals()
        except (ValueError, ContractNotFound, AttributeError):
            print("Token issue, skipping:", token)
            continue

        try:
            symbol = token_contract.symbol()
        except:
            symbol = token
            print("Token doesn't have a symbol field")

        try:
            price = get_price(event.address, block=event.blockNumber)
        except:
            print(
                "Pricing error for",
                symbol,
                "on",
                token_contract.address,
                "****************************************",
            )
            continue
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')

        print("\nDate:", date, f"Transaction: {tx_hash}")
        print("Token Symbol:", symbol, f"Price: {price}")
        dates.append(date)
        tx_ids.append(tx_hash)
        symbols.append(symbol)
        prices.append(price)

    # visualize all of our data
    column_titles = [
        "Date",
        "Tx ID",
        "Token Symbol",
        "Price",
    ]
    data = pd.DataFrame(
        zip(
            dates,
            tx_ids,
            symbols,
            prices,
        ),
        columns=column_titles,
    )

    data["Price"] = data["Price"].map("${:,.9f}".format)

    if chain.id == 1:
        data.to_excel(
            "/Users/dudesahn/Documents/GitHub/dudesahn/TestingGround/scripts/tx_prices_sent.xlsx",
            index=False,
        )
    else:
        data.to_excel(
            "/Users/dudesahn/Documents/GitHub/dudesahn/TestingGround/scripts/tx_prices_sent_ftm.xlsx",
            index=False,
        )
