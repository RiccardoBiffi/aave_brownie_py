import time
from brownie import config, network, interface
from web3 import Web3
from scripts.utilities import get_account
from scripts.get_weth import get_weth
from web3 import Web3
from decimal import Decimal


AMOUNT = Web3.toWei(0.01, "ether")
STABLE_RATE = 1
LPAP = interface.ILendingPoolAddressesProvider(
    config["networks"][network.show_active()]["lending_pool_addresses_provider"]
)
BORROW_WEAKEN = Decimal(0.9)


def main():
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    lending_pool = get_lending_pool()

    # I need to approve() to authorize the lending contract to take AMOUNT of my tokens from the token contract
    approve_erc20(AMOUNT, lending_pool.address, weth_address, account)
    deposit_erc20(weth_address, lending_pool, account)

    # Now I can lend something using the deposit as collateral.
    # Let's get some info on our position
    borrowable_eth, borrowed = get_borrowable_data(lending_pool, account)

    # Let's borrow some DAI (in terms of ETH borrow power)
    # AAVE uses chainlink as a conversion Oracle, we'll use it's methods
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * BORROW_WEAKEN)
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_erc20(lending_pool, Web3.toWei(dai_to_borrow, "ether"), dai_address, account)

    # Let's see our updated position
    borrowable_eth, borrowed = get_borrowable_data(lending_pool, account)

    # Let's repay our debt
    # repay_erc20(lending_pool, Web3.toWei(dai_to_borrow, "ether"), dai_address, account)

    # Let's see our updated position
    borrowable_eth, borrowed = get_borrowable_data(lending_pool, account)

    time.sleep(1)


def repay_erc20(lending_pool, amount_to_repay, erc20_address, account):
    approve_erc20(amount_to_repay, lending_pool.address, erc20_address, account)
    tx = lending_pool.repay(
        erc20_address,
        amount_to_repay,
        STABLE_RATE,
        account.address,
        {"from": account},
    )
    tx.wait(1)
    amount_to_repay = Web3.fromWei(amount_to_repay, "ether")
    print(f"{amount_to_repay} ERC20 token rapayed!\n")
    return tx


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)
    price = dai_eth_price_feed.latestRoundData()[1]  # take 2nd output of the pentupla
    price = Web3.fromWei(price, "ether")
    print(f"The ERC20 price is {price} ETH")
    return price


def borrow_erc20(lending_pool, amount_to_borrow, erc20_address, account):
    # 1 stable interest rate, 2 variabile interest rate
    tx = lending_pool.borrow(
        erc20_address,
        amount_to_borrow,
        STABLE_RATE,
        0,
        account.address,
        {"from": account},
    )
    tx.wait(1)
    amount_to_borrow = Web3.fromWei(amount_to_borrow, "ether")
    print(f"{amount_to_borrow} ERC20 token borrowed!\n")
    return tx


def get_borrowable_data(lending_pool, account):
    (
        tot_collateral_eth,
        tot_debt_eth,
        avail_borrow_eth,
        liquidation_threshold,
        ltv,
        health,
    ) = lending_pool.getUserAccountData(account.address)
    tot_collateral_eth = Web3.fromWei(tot_collateral_eth, "ether")
    tot_debt_eth = Web3.fromWei(tot_debt_eth, "ether")
    avail_borrow_eth = Web3.fromWei(avail_borrow_eth, "ether")
    liquidation_threshold = liquidation_threshold / 100
    ltv = ltv / 100
    print(f"TOT collateral: {tot_collateral_eth}")
    print(f"TOT borrowed: {tot_debt_eth}")
    print(f"Borrow power left: {avail_borrow_eth}")
    print(f"Liquidation threshold: {liquidation_threshold}%")
    print(f"Loan to value: {ltv}%")
    print(f"Health factor: {health}")
    return (avail_borrow_eth, tot_debt_eth)


def deposit_erc20(weth_address, lending_pool, account):
    tx = lending_pool.deposit(
        weth_address, AMOUNT, account.address, 0, {"from": account}
    )  # _referralCode parameter is now deprecated, always set 0
    print("ERC20 token deposited!\n")
    return tx


def approve_erc20(amount, approved_spender, erc20_address, account):
    token = interface.IERC20(erc20_address)
    tx = token.approve(approved_spender, amount, {"from": account})
    print("ERC20 token approved!\n")
    return tx


def get_lending_pool():
    # I need to get the address from the right AAVE market using the AddressProvider
    lending_pool_address = LPAP.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
