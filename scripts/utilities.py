from brownie import Contract, network, accounts, config, interface
from enum import Enum

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
contract_to_mock = {}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]  # primo account offerto da Ganache
    if id:
        return accounts.load(id)

    # siamo in mainnet
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_enum):
    """
    Ottiene il contract specificato.
    Se la blockchain è un fork o esterna, lo prende leggendo l'address da brownie-config;
    altrimenti, se siamo su una blockchain locale, viene deployato un mock e restituito.

    Args:
        contract_enum (MockContract): enum del contratto da ottenere

    Returns:
        brownie.network.contract.ProjectContract : l'ultima versione deployata del contratto,
        che può essere un mock o un contratto "reale" già presente sul network
    """
    contract_type = contract_to_mock[contract_enum]

    if is_local_blockchain():
        if len(contract_type) == 0:  # contratto mai deployato
            pass  # deploy_mock(contract_enum)
        contract = contract_type[-1]  # prendo l'ultimo contratto deployato

    else:
        # il contratto esiste già nella blockchain (testnet o fork)
        contract_address = config["networks"][network.show_active()][
            contract_enum.value
        ]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


def is_local_blockchain():
    return network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
