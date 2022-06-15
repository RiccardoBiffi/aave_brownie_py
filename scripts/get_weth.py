from scripts.utilities import get_account
from brownie import interface, network, config


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    # To call a deployed contract we need an ABI and an address
    account = get_account()
    # I don't user get_contract() for semplicity (I'm not gonna deploy anything)
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.02 * 10**18})
    print("Recieved 0.02 WETH")

    return tx
