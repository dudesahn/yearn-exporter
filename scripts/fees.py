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
        from_block = 33506480
        dai = contract("0xF137D22d7B23eeB1950B3e19d1f578c053ed9715")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    print(f"Starting from block {from_block}")

    print(f"abi: {dai.events.Transfer().abi}")
    topics = construct_event_topic_set(
        dai.events.Transfer().abi,
        web3.codec,
        #{'receiver': ['0x98AA6B78ed23f4ce2650DA85604ceD5653129A21', '0xC3D6880fD95E06C816cB030fAc45b3ffe3651Cb0', '0xE7a43665677AcfC6A3B15f00b68119c486EC56A3']},
        {'receiver': ['0x5C46eee2edFb8a00b1C9269C4365e206F7C9FBdC']},
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
                "0x34278F6f40079eae344cbaC61a764Bcf85AfC949",  # scam token FF9
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
                "0xfA00D65F0873059d2858f1CF7e9a0822754418dd",  # YBPT
                "0x32296969Ef14EB0c6d29669C550D4a0449130230",  # B-stETH-STABLE
                "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # WBTC
                "0x33Dde19C163cDccE4E5a81f04a2Af561b9Ef58d7",
                "0x76a34D72b9CF97d972fB0e390eB053A37F211c74", # element
                "0x90CA5cEf5B29342b229Fb8AE2DB5d8f4F894D652",
                "0x52C9886d5D87B0f06EbACBEff750B5Ffad5d17d9",
                "0x7C9cF12d783821d5C63d8E9427aF5C44bAd92445",
                "0xF1294E805B992320A3515682c6aB0Fe6251067E5",
                "0x8a2228705ec979961F0e16df311dEbcf097A2766",
                "0x10a2F8bd81Ee2898D7eD18fb8f114034a549FA59",
                "0x9e030b67a8384cbba09D5927533Aa98010C87d91",
                "0xF6d2699b035FC8fD5E023D4a6Da216112ad8A985",
                "0x449D7C2e096E9f867339078535b15440d42F78E8",
                "0xA47D1251CF21AD42685Cc6B8B3a186a73Dbd06cf",
                "0xB70c25D96EF260eA07F650037Bf68F5d6583885e",
                "0x7Edde0CB05ED19e03A9a47CD5E53fC57FDe1c80c",
                "0xa47c8bf37f92aBed4A126BDA807A7b7498661acD", # UST
                "0xbA38029806AbE4B45D5273098137DDb52dA8e62F", # PLP
                "0x2ba592F78dB6436527729929AAf6c908497cB200", # cream
                "0x92B767185fB3B04F881e3aC8e5B0662a027A1D9f", # crdai
                "0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8", # yDAI+yUSDC+yUSDT+yTUSD
                "0xED196D746493bC855f95Ce5346C0161F68DB874b", # SHIK
                "0x82dfDB2ec1aa6003Ed4aCBa663403D7c2127Ff67", # akSwap.io
                "0x0316EB71485b0Ab14103307bf65a021042c6d380", # HBTC
                "0xEb1a6C6eA0CD20847150c27b5985fA198b2F90bD", # element
                "0x2361102893CCabFb543bc55AC4cC8d6d0824A67E",
                "0xEb1a6C6eA0CD20847150c27b5985fA198b2F90bD",
                "0x2361102893CCabFb543bc55AC4cC8d6d0824A67E",
                "0x49D72e3973900A195A155a46441F0C08179FdB64", # creth2
                "0x6Bba316c48b49BD1eAc44573c5c871ff02958469", # gas
            ]
            if token in to_skip:
                print("\nNon-vault token from our list to skip")
                continue

        print(f"contract {token}")
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
