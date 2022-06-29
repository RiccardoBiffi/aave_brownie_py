import time
from brownie import config, network, interface
from scripts.utilities import get_account
from scripts.get_weth import get_weth


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lending_pool = get_lending_pool()
    print(f"Lending pool address is {lending_pool.address}")

    time.sleep(1)  # gives time to last transaction to complete


def get_lending_pool():
    # I need to get the address from the right AAVE market using the AddressProvider
    account = get_account()
    lpap = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lpap.getLendingPool()

    return interface.ILendingPool(lending_pool_address)
