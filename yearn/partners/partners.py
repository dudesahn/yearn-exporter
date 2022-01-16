from yearn.partners.snapshot import (
    BentoboxWrapper,
    Partner,
    WildcardWrapper,
    Wrapper,
    YApeSwapFactoryWrapper,
)

partners = [
    Partner(
        name='coinomo',
        treasury='0xd3877d9df3cb52006b7d932e8db4b36e22e89242',
        wrappers=[
            Wrapper(
                name='yvUSDC',
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper='0xd3877d9df3cb52006b7d932e8db4b36e22e89242',
            ),
        ],
    ),
    Partner(
        name='alchemix',
        treasury='0x8392F6669292fA56123F71949B52d883aE57e225',
        wrappers=[
            Wrapper(
                name='dai 0.3.0',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0x014dE182c147f8663589d77eAdB109Bf86958f13',
            ),
            Wrapper(
                name='dai 0.3.0 transmuter',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0x491EAFC47D019B44e13Ef7cC649bbA51E15C61d7',
            ),
            Wrapper(
                name='dai 0.4.3',
                vault='0xdA816459F1AB5631232FE5e97a05BBBb94970c95',
                wrapper='0xb039eA6153c827e59b620bDCd974F7bbFe68214A',
            ),
            Wrapper(
                name='dai 0.4.3 transmuter',
                vault='0xdA816459F1AB5631232FE5e97a05BBBb94970c95',
                wrapper='0x6Fe02BE0EC79dCF582cBDB936D7037d2eB17F661',
            ),
            Wrapper(
                name='weth 0.4.2',
                vault='0xa258C4606Ca8206D8aA700cE2143D7db854D168c',
                wrapper='0x546E6711032Ec744A7708D4b7b283A210a85B3BC',
            ),
            Wrapper(
                name='weth 0.4.2 transmuter',
                vault='0xa258C4606Ca8206D8aA700cE2143D7db854D168c',
                wrapper='0x6d75657771256C7a8CB4d475fDf5047B70160132',
            ),
        ],
    ),
    Partner(
        name='inverse',
        treasury='0x926dF14a23BE491164dCF93f4c468A50ef659D5B',
        wrappers=[
            Wrapper(
                name='dai-wbtc',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0xB0B02c75Fc1D07d351C991EBf8B5F5b48F24F40B',
            ),
            Wrapper(
                name='dai-yfi',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0xbE21650b126b08c8b0FbC8356a8B291010ee901a',
            ),
            Wrapper(
                name='dai-weth',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0x57faa0dec960ed774674a45d61ecfe738eb32052',
            ),
            Wrapper(
                name='usdc-weth',
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper='0x698c1d40574cd90f1920f61D347acCE60D3910af',
            ),
            Wrapper(
                name='dola-stabilizer',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0x973F509c695cffcF355787456923637FF8A34b29',
            ),
        ],
    ),
    Partner(
        name='frax',
        treasury='0x8d0C5D009b128315715388844196B85b41D9Ea30',
        wrappers=[
            Wrapper(
                name='usdc',
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper='0xEE5825d5185a1D512706f9068E69146A54B6e076',
            ),
        ],
    ),
    Partner(
        name='pickle',
        treasury='0x066419EaEf5DE53cc5da0d8702b990c5bc7D1AB3',
        wrappers=[
            Wrapper(
                name='usdc',
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper='0xEecEE2637c7328300846622c802B2a29e65f3919',
            ),
            Wrapper(
                name='lusd',
                vault='0x5fA5B62c8AF877CB37031e0a3B2f34A78e3C56A6',
                wrapper='0x699cF8fE0C1A6948527cD4737454824c6E3828f1',
            ),
        ],
    ),
    Partner(
        name='badger',
        treasury='0xB65cef03b9B89f99517643226d76e286ee999e77',
        wrappers=[
            Wrapper(
                name='wbtc',
                vault='0xA696a63cc78DfFa1a63E9E50587C197387FF6C7E',
                wrapper='0x4b92d19c11435614CD49Af1b589001b7c08cD4D5',
            ),
        ],
    ),
    Partner(
        name='deus',
        treasury='0x4e8a7c429192bfda8c9a1ef0f3b749d0f66657aa',
        wrappers=[
            Wrapper(
                name='aeth',
                vault='0x132d8D2C76Db3812403431fAcB00F3453Fc42125',
                wrapper='0x4e8a7c429192bfda8c9a1ef0f3b749d0f66657aa',
            )
        ],
    ),
    Partner(
        name='basketdao',
        treasury='0x7301C46be73bB04847576b6Af107172bF5e8388e',
        wrappers=[
            WildcardWrapper(
                name='bdi',
                wrapper='0x0309c98B1bffA350bcb3F9fB9780970CA32a5060',
            ),
            WildcardWrapper(
                name='bmi',
                wrapper='0x0aC00355F80E289f53BF368C9Bdb70f5c114C44B',
            ),
        ],
    ),
    Partner(
        name='gb',
        treasury='0x6965292e29514e527df092659FB4638dc39e7248',
        wrappers=[
            WildcardWrapper(
                name='gb1',
                wrapper='0x6965292e29514e527df092659FB4638dc39e7248',
            ),
        ],
    ),
    Partner(
        name='donutapp',
        treasury='0x9eaCFF404BAC19195CbD131a4BeA880Abd09B35e',
        wrappers=[
            Wrapper(
                name='yvDAI',
                vault='0x19D3364A399d251E894aC732651be8B0E4e85001',
                wrapper='0x9eaCFF404BAC19195CbD131a4BeA880Abd09B35e',
            ),
        ],
    ),
    Partner(
        name="yieldster",
        treasury='0x2955278aBCE187315D6d72B0d626f1217786DF60',
        wrappers=[
            WildcardWrapper(
                name="liva-one",
                wrapper="0x2747ce11793F7059567758cc35D34F63ceE8Ac00",
            ),
        ],
    ),
    Partner(
        name="akropolis",
        treasury='0xC5aF91F7D10dDe118992ecf536Ed227f276EC60D',
        wrappers=[
            WildcardWrapper(
                name="vaults-savings-v2",
                wrapper="0x6511D8686EB43Eac9D4852458435c1beC4D67bc6",
            ),
        ],
    ),
    Partner(
        name="Mover",
        treasury='0xf6A0307cb6aA05D7C19d080A0DA9B14eAB1050b7',
        wrappers=[
            Wrapper(
                name="savings_yUSDCv2",
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper="0x541d78076352a884C8358a2ac3f36408b99a18dB",
            ),
        ],
    ),
    Partner(
        name='yapeswap',
        treasury='0x10DE513EE154BfA97f1c2841Cab91E8C389c7c72',
        wrappers=[
            YApeSwapFactoryWrapper(
                'yapeswap', '0x46aDc1C052Fafd590F56C42e379d7d16622835a2'
            ),
        ],
    ),
    Partner(
        name='abracadabra',
        treasury='0x5A7C5505f3CFB9a0D9A8493EC41bf27EE48c406D',
        # brownie run abracadabra_wrappers
        wrappers=[
            BentoboxWrapper(
                name='yvCurve-IronBank',
                vault='0x27b7b1ad7288079A66d12350c828D3C00A6F07d7',
                wrapper='0xEBfDe87310dc22404d918058FAa4D56DC4E93f0A',
            ),
            BentoboxWrapper(
                name='yvCurve-stETH',
                vault='0xdCD90C7f6324cfa40d7169ef80b12031770B4325',
                wrapper='0x0BCa8ebcB26502b013493Bf8fE53aA2B1ED401C1',
            ),
            BentoboxWrapper(
                name='yvUSDC',
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper='0x6cbAFEE1FaB76cA5B5e144c43B3B50d42b7C8c8f',
            ),
            BentoboxWrapper(
                name='yvUSDT',
                vault='0x7Da96a3891Add058AdA2E826306D812C638D87a7',
                wrapper='0x551a7CfF4de931F32893c928bBc3D25bF1Fc5147',
            ),
            BentoboxWrapper(
                name='yvWETH',
                vault='0xa258C4606Ca8206D8aA700cE2143D7db854D168c',
                wrapper='0x920D9BD936Da4eAFb5E25c6bDC9f6CB528953F9f',
            ),
            BentoboxWrapper(
                name='yvYFI',
                vault='0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1',
                wrapper='0xFFbF4892822e0d552CFF317F65e1eE7b5D3d9aE6',
            ),
            BentoboxWrapper(
                name='yvWETH',
                vault='0xa9fE4601811213c340e850ea305481afF02f5b28',
                wrapper='0x6Ff9061bB8f97d948942cEF376d98b51fA38B91f',
            ),
        ],
    ),
    Partner(
        name='chfry',
        treasury='0x3400985be0b41Ce9778823E9618074115f830799',
        wrappers=[
            Wrapper(
                name='USDT yVault',
                vault='0x7Da96a3891Add058AdA2E826306D812C638D87a7',
                wrapper='0x87e51ebF96eEB023eCc28536Ad0DBca83dEE0203',
            ),
            Wrapper(
                name='DAI yVault',
                vault='0xdA816459F1AB5631232FE5e97a05BBBb94970c95',
                wrapper='0xd5F38f4F1e0c157dd1AE8Fd66EE2761A14eF7324',
            ),
            Wrapper(
                name='USDC yVault',
                vault='0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9',
                wrapper='0x782bc9B1F11cDBa13aCb030cDab04f04FB667846',
            ),
        ],
    ),
]
