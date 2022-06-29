import time
from scripts.utilities import get_account
from brownie import interface, network, config


def main():
    get_weth()
    time.sleep(1)  # gives time to last transaction to complete


def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    # To call a deployed contract we need an ABI and an address
    account = get_account()
    # I don't use get_contract() for semplicity (I'm not gonna deploy anything)
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.02 * 10**18})
    print("Deposited 0.03 ETH, recieved 0.02 WETH")

    return tx
