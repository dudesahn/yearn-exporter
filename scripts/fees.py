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
from yearn.events import get_logs_asap_2

def main():
    print("We've started")
    if chain.id == 1:
        from_block = 12059089
        dai = contract("0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    else:
        from_block = 8042204 # 302 days ago

        dai = contract("0x0DEC85e74A92c52b7F708c4B10207D9560CEFaf0")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    print(f"Starting from block {from_block}")

    print(f"abi: {dai.events.Transfer().abi}")

    # ADD YOUR ADDRESSES HERE
    my_wallets = ['0x03ebbFCc5401beef5B4A06c3BfDd26a75cB09A84', '0x05B7D0dfdD845c58AbC8B78b02859b447b79ed34']

    topics = construct_event_topic_set(
        dai.events.Transfer().abi,
        web3.codec,
        {'receiver': my_wallets},
    )

    logs = get_logs_asap_2(topics, from_block, chain.height, 1)

    print(f"Logs fetched. size = {len(logs)}")
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
                "0x03E173Ad8d1581A4802d3B532AcE27a62c5B81dc", # THALES
                "0x6810e776880C02933D47DB1b9fc05908e5386b96", # GNO
                "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2", # SUSHI
                "0x584bC13c7D411c00c01A62e8019472dE68768430", # Hegic
            ]
        elif chain.id == 250:
            to_skip = [
                # FTM
                "0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE", # BOO
                "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75", # USDC
                "0x328A7b4d538A2b3942653a9983fdA3C12c571141", # iUSDC
                "0xD0660cD418a64a1d44E9214ad8e459324D8157f1", # WOOFY
                "0x049d68029688eAbF473097a2fC38ef61633A3C7A", # fusdt
                "0xf16e81dce15B08F326220742020379B855B87DF9", # ice
                "0x92D5ebF3593a92888C25C0AbEF126583d4b5312E", # fusdt+dai+usdc
                "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522", # fusdt+dai+usdc gauge
                "0x1E4F97b9f9F913c46F1632781732927B9019C68b", # crv
                "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E", # dai
                "0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40", # dai-usdc
                "0x8866414733F22295b7563f9C5299715D2D76CAf4", # dai-usdc gauge
                "0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83", # wftm
                "0x2F96f61a027B5101E966EC1bA75B78f353259Fb3", # TNGLv3
                "0x82f0B8B456c1A451378467398982d4834b6829c1", # mim
                "0x2dd7C9371965472E5A5fD28fbE165007c61439E1", # 3poolv2-f
                "0x5Cc61A78F164885776AA610fb0FE1257df78E59B", # spirit
                "0xD02a30d33153877BC20e5721ee53DeDEE0422B2F", # g3crv
                "0xd4F94D0aaa640BBb72b5EEc2D85F6D114D81a88E", # g3crv gauge
                "0xd8321AA83Fb0a4ECd6348D4577431310A6E0814d", # geist
                "0x87e377820010D818aA316F8C3F1C2B9d025eb5eE", # spam
                "0x06e3C4da96fd076b97b7ca3Ae23527314b6140dF", # fUSDT+DAI+USDC-gauge
                "0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605", # anyUSDC
                "0x2823D10DA533d9Ee873FEd7B16f4A962B2B7f181", # anyUSDT
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

        # Avoid double dipping
        if src in my_wallets:
            print(f"Skipping sending form {src} to {dst}")
            continue

        # ignore income from addresses we know weren't fee distros. mainly other transfers and mints.
        addresses_to_ignore = [
            "0x677Ae1C4FDa1A986a23a055Bbd0A94f8e5b284De",  # deposited test to ib vault here, then sent over
            "0x0000000000000000000000000000000000000000",  # burn/mint address
            "0x25B28EE7f335F0396f41f129039F1583345B21b8",  # dudesahn.eth
            "0xF5BCE5077908a1b7370B9ae04AdC565EBd643966",  # bentobox FTM
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
