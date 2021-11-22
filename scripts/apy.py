import json
import dataclasses
import warnings
import logging

from brownie.exceptions import BrownieEnvironmentWarning

from tabulate import tabulate

from yearn.apy import get_samples, ApyError
from yearn.v1.registry import Registry as RegistryV1
from yearn.v2.registry import Registry as RegistryV2

from yearn.v2.vaults import Vault as VaultV2
from yearn.v2.strategies import Strategy as StrategyV2

from yearn.special import Backscratcher, YveCRVJar

warnings.simplefilter("ignore", BrownieEnvironmentWarning)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("yearn.apy")


def main():
    data = []

    samples = get_samples()

    v1_registry = RegistryV1()

    for vault in v1_registry.vaults:
        apy = vault.apy(samples)
        data.append({"product": apy.type, "name": vault.name, "apy": apy.net_apy})

    v2_registry = RegistryV2()

    for vault in v2_registry.vaults:
        try:
            apy = vault.apy(samples)
            data.append({"product": apy.type, "name": vault.name, "apy": apy.net_apy})
        except ApyError as error:
            logger.error(error)
        except Exception as error:
            print(vault)
            raise error

    data.sort(key=lambda x: -x["apy"])
    print(tabulate(data, floatfmt=",.0%"))

def lusd():
    samples = get_samples()
    address = "0x5fA5B62c8AF877CB37031e0a3B2f34A78e3C56A6"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def rai():
    samples = get_samples()
    address = "0x873fB544277FD7b977B196a826459a69E27eA4ea"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))
    
def tricrypto():
    samples = get_samples()
    address = "0x3D980E50508CFd41a13837A60149927a11c03731"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def pickleJar():
    samples = get_samples()
    special = YveCRVJar()
    print(json.dumps(dataclasses.asdict(special.apy(samples)), indent=2))

def mim():
    samples = get_samples()
    address = "0x2DfB14E32e2F8156ec15a2c21c3A6c053af52Be8"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def eurt():
    samples = get_samples()
    address = "0x0d4EA8536F9A13e4FBa16042a46c30f092b06aA5"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def yvboost():
    samples = get_samples()
    address = "0x9d409a0A012CFbA9B15F6D4B36Ac57A46966Ab9a"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def ibEUR():
    samples = get_samples()
    address = "0x67e019bfbd5a67207755D04467D6A70c0B75bF60"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def cvxCRV():
    samples = get_samples()
    address = "0x4560b99C904aAD03027B5178CCa81584744AC01f"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def ibJPY():
    samples = get_samples()
    address = "0x59518884EeBFb03e90a18ADBAAAB770d4666471e"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))
    
def ibKRW():
    samples = get_samples()
    address = "0x528D50dC9a333f01544177a924893FA1F5b9F748"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def yfi():
    samples = get_samples()
    address = "0xdb25cA703181E7484a155DD612b06f57E12Be5F0"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def sushi():
    samples = get_samples()
    address = "0x6d765CbE5bC922694afE112C140b8878b9FB0390"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def ibeur():
    samples = get_samples()
    address = "0x67e019bfbd5a67207755D04467D6A70c0B75bF60"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def ibgbp():
    samples = get_samples()
    address = "0x595a68a8c9D5C230001848B69b1947ee2A607164"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def ibkrw():
    samples = get_samples()
    address = "0x528D50dC9a333f01544177a924893FA1F5b9F748"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def dai():
    samples = get_samples()
    address = "0xdA816459F1AB5631232FE5e97a05BBBb94970c95"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def usdc():
    samples = get_samples()
    address = "0xa354F35829Ae975e850e23e9615b11Da1B3dC4DE"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def snx():
    samples = get_samples()
    address = "0xF29AE508698bDeF169B89834F76704C3B205aedf"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def usdc_old():
    samples = get_samples()
    address = "0x5f18C75AbDAe578b483E5F43f12a39cF75b973a9"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))

def steth():
    samples = get_samples()
    address = "0xdCD90C7f6324cfa40d7169ef80b12031770B4325"
    vault = VaultV2.from_address(address)
    print(json.dumps(dataclasses.asdict(vault.apy(samples)), indent=2))
    

