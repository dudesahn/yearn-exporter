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
        '0xBedf3Cf16ba1FcE6c3B751903Cf77E51d51E05b8',
        '0x8Ef63b525fceF7f8662D98F77f5C9A86ae7dFE09',
        '0x986176Df2e9dC6225DfB498D1869ABA04893dcE1',
    ]

    my_wallets = dudesahn
    print("Current chain height:", chain.height)
    dates = []
    tx_ids = []
    symbols = []
    prices = []
    amounts = []

    if chain.id == 1:
        from_block = 14750404
        # first block for dudesahn, 5580662
        # newer block for recent distros, 14750404
        dai = contract("0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
    else:
        # fantom
        from_block = 34803211
        dai = contract("0x0DEC85e74A92c52b7F708c4B10207D9560CEFaf0")
        dai = web3.eth.contract(str(dai), abi=dai.abi)
        # 35803211 March 30 2022
        # 8042204 poolpi's date
        # 29418132 ~1000 blocks before I got my first rewards on Fantom
        # 17994789 midday 9-30-21
        # 4306100, 100k before my first tx that shows up on ftmscan, but there are 4 more pages, maybe error tho
        
    # set our to_block if we want
    USE_TO_BLOCK = True
    to_block = chain.height
    if USE_TO_BLOCK:
        to_block = 14796496 # 1 block after our last distro for fantom, 14796496 for mainnet
        print(f"Ending with block {to_block}")
    else:
        print(f"Ending with current chain height {chain.height}")
    

    print(f"Starting from block {from_block}")
    print(f"abi: {dai.events.Transfer().abi}")

    topics = construct_event_topic_set(
        dai.events.Transfer().abi,
        web3.codec,
        {'receiver': my_wallets},
    )

    logs = get_logs_asap(topics, None, from_block, to_block, 1)

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
            "0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C",  # BNT
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
            "0x5282a4eF67D9C33135340fB3289cc1711c13638C",  # Iron Bank pool token
            "0x48Fb253446873234F2fEBbF9BdeAA72d9d387f94",  # vBNT
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
            "0x76a34D72b9CF97d972fB0e390eB053A37F211c74",  # element
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
            "0xa47c8bf37f92aBed4A126BDA807A7b7498661acD",  # UST
            "0xbA38029806AbE4B45D5273098137DDb52dA8e62F",  # PLP
            "0x2ba592F78dB6436527729929AAf6c908497cB200",  # cream
            "0x92B767185fB3B04F881e3aC8e5B0662a027A1D9f",  # crdai
            "0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8",  # yDAI+yUSDC+yUSDT+yTUSD
            "0xED196D746493bC855f95Ce5346C0161F68DB874b",  # SHIK
            "0x82dfDB2ec1aa6003Ed4aCBa663403D7c2127Ff67",  # akSwap.io
            "0x0316EB71485b0Ab14103307bf65a021042c6d380",  # HBTC
            "0xEb1a6C6eA0CD20847150c27b5985fA198b2F90bD",  # element
            "0x2361102893CCabFb543bc55AC4cC8d6d0824A67E",
            "0xEb1a6C6eA0CD20847150c27b5985fA198b2F90bD",
            "0x2361102893CCabFb543bc55AC4cC8d6d0824A67E",
            "0x49D72e3973900A195A155a46441F0C08179FdB64",  # creth2
            "0x6Bba316c48b49BD1eAc44573c5c871ff02958469",  # gas
            "0x03E173Ad8d1581A4802d3B532AcE27a62c5B81dc",  # THALES
            "0x6810e776880C02933D47DB1b9fc05908e5386b96",  # GNO
            "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",  # SUSHI
            "0x584bC13c7D411c00c01A62e8019472dE68768430",  # Hegic
            "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522",  # USDN3Crv
            "0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72",  # ENS
            "0x908599FDf490b73D171B57731bd4Ca95b7F0DE6a",  # scam
            "0x111111111117dC0aa78b770fA6A738034120C302",
            "0x41D5D79431A913C4aE7d69a668ecdfE5fF9DFB68",
            "0x865377367054516e17014CcdED1e7d814EDC9ce4",
            "0xdBdb4d16EdA451D0503b854CF79D55697F90c8DF",
            "0xA952dC25d8454a7611277cD77BE8285cD0192ceE",
            "0xc85E0474068dbA5B49450c26879541EE6Cc94554",
            "0x74232704659ef37c08995e386A2E26cc27a8d7B1",  # STRK
        ]
    elif chain.id == 250:
        to_skip = [
            # FTM
            "0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE",  # BOO
            "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75",  # USDC
            "0x328A7b4d538A2b3942653a9983fdA3C12c571141",  # iUSDC
            "0xD0660cD418a64a1d44E9214ad8e459324D8157f1",  # WOOFY
            "0xc5A9848b9d145965d821AaeC8fA32aaEE026492d",  # OXDv2
            "0x888EF71766ca594DED1F0FA3AE64eD2941740A20",  # SOLID
            "0xc165d941481e68696f43EE6E99BFB2B23E0E3114",  # OXDv1
            "0xDA0053F0bEfCbcaC208A3f867BB243716734D809",  # oxSOLID
            "0x9aC7664060a3e388CEB157C5a0B6064BeFFAb9f2",  # anyFTM/FTM LP
            "0x6362496Bef53458b20548a35A2101214Ee2BE3e0",  # anyFTM
            "0xbcab7d083Cf6a01e0DdA9ed7F8a02b47d125e682",  # USDC/MIM LP
            "0x049d68029688eAbF473097a2fC38ef61633A3C7A",  # fusdt
            "0xf16e81dce15B08F326220742020379B855B87DF9",  # ice
            "0x92D5ebF3593a92888C25C0AbEF126583d4b5312E",  # fusdt+dai+usdc
            "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522",  # fusdt+dai+usdc gauge
            "0x1E4F97b9f9F913c46F1632781732927B9019C68b",  # crv
            "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E",  # dai
            "0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40",  # dai-usdc
            "0x8866414733F22295b7563f9C5299715D2D76CAf4",  # dai-usdc gauge
            "0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83",  # wftm
            "0x2F96f61a027B5101E966EC1bA75B78f353259Fb3",  # TNGLv3
            "0x82f0B8B456c1A451378467398982d4834b6829c1",  # mim
            "0x2dd7C9371965472E5A5fD28fbE165007c61439E1",  # 3poolv2-f
            "0x5Cc61A78F164885776AA610fb0FE1257df78E59B",  # spirit
            "0xD02a30d33153877BC20e5721ee53DeDEE0422B2F",  # g3crv
            "0xd4F94D0aaa640BBb72b5EEc2D85F6D114D81a88E",  # g3crv gauge
            "0xd8321AA83Fb0a4ECd6348D4577431310A6E0814d",  # geist
            "0x87e377820010D818aA316F8C3F1C2B9d025eb5eE",  # spam
            "0x06e3C4da96fd076b97b7ca3Ae23527314b6140dF",  # fUSDT+DAI+USDC-gauge
            "0x95bf7E307BC1ab0BA38ae10fc27084bC36FcD605",  # anyUSDC
            "0x2823D10DA533d9Ee873FEd7B16f4A962B2B7f181",  # anyUSDT
            "0xfcef8a994209d6916EB2C86cDD2AFD60Aa6F54b1",  # fBEETS
            "0xF24Bcf4d1e507740041C9cFd2DddB29585aDCe1e",  # BEETS
            "0xe826F3C308aEB14cF901e19af1E5a0f7E73b625C",  # scam token
        ]

    for event in track(events):
        ts = chain[event.blockNumber].timestamp
        token = event.address
        # print("\nToken address:", token)  # use this for debugging when we crash on a token

        if token in to_skip:
            print("Non-vault token from our list to skip")
            continue

        try:
            token_contract = contract(token)
            token_contract.apiVersion()
        except:
            print(
                token,
                "is not a vault token and shouldn't be counted",
            )
            continue

        src, dst, amount = event.args.values()
        tx_hash = event.transactionHash.hex()

#         # check that our source of tokens is a strategy
#         try:
#             strategy = contract(src)
#             strategy.apiVersion()
#             strategy.want()  # do this to ignore vault tokens
#         except:
#             print(f"Transaction: {tx_hash}")
#             print(f"Source: {src}")
#             print(
#                 "Appears to be a transfer, not a fee distro **********************************************"
#             )
#             continue

        try:
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
        print("Token Symbol:", symbol, f"Price: {price}", "Amount:", amount)
        dates.append(date)
        tx_ids.append(tx_hash)
        symbols.append(symbol)
        prices.append(price)
        amounts.append(amount)

    # visualize all of our data
    column_titles = [
        "Date",
        "Tx ID",
        "Token Symbol",
        "Amount",
        "Price",
    ]
    data = pd.DataFrame(
        zip(
            dates,
            tx_ids,
            symbols,
            amounts,
            prices,
        ),
        columns=column_titles,
    )

    data["Price"] = data["Price"].map("${:,.9f}".format)

    if chain.id == 1:
        data.to_excel(
            "/Users/dudesahn/Documents/GitHub/dudesahn/TestingGround/scripts/distro_amounts_and_prices.xlsx",
            index=False,
        )
    else:
        data.to_excel(
            "/Users/dudesahn/Documents/GitHub/dudesahn/TestingGround/scripts/distro_amounts_and_prices_ftm.xlsx",
            index=False,
        )
