from web3 import Web3
from scripts.aave_borrow import (
    get_asset_price,
    get_lending_pool,
    get_account,
    get_borrowable_data,
    get_weth,
    approve_erc20,
)
from brownie import config, network, interface


def test_get_asset_price():
    # Arrange act
    asset_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # Assert
    assert asset_price > 0


def test_get_asset_price_weth():
    # Arrange act
    asset_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # Assert
    assert asset_price > 0


def test_get_borrowable_data():
    # Arrange
    avail_borrow_eth = -1
    tot_debt_eth = -1
    lpap = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )

    lending_pool = get_lending_pool(lpap)
    account = get_account()

    # Act
    avail_borrow_eth, tot_debt_eth = get_borrowable_data(lending_pool, account)

    # Assert
    assert avail_borrow_eth >= 0 and tot_debt_eth >= 0


def test_get_weth():
    # Arrange
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    init_weth_balance = weth.balanceOf(account.address)
    init_eth_balance = account.balance()

    # Act
    get_weth()
    last_weth_balance = weth.balanceOf(account.address)
    last_eth_balance = account.balance()

    # Assert
    assert (init_eth_balance - Web3.toWei(0.2, "ether")) == last_eth_balance
    assert (init_weth_balance + Web3.toWei(0.2, "ether")) == last_weth_balance


def test_get_lending_pool():
    # Arrange
    lpap = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    # Act
    lending_pool = get_lending_pool(lpap)
    # Assert
    assert lending_pool is not None


def test_approve_erc20():
    # Arrange
    account = get_account()
    lpap = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool = get_lending_pool(lpap)
    amount = 1 * 10**18
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    # Act
    result = approve_erc20(amount, lending_pool.address, erc20_address, account)

    # Assert
    assert result is True
