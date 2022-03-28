from brownie import accounts, config, network, Lottery, Contract
from brownie import MockV3Aggregator, VRFCoordinatorMock, LinkToken
from scripts.deploy_mocks import deploy_mocks

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract('price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['keyhash'],
        config['networks'][network.show_active()]['vrffee'],
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify', False),
    )
    return lottery

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in ['development', 'ganache-local']:
        return accounts[0]
    return accounts.add(config['wallets']['from_key'])

def get_contract(c_name):
    name2mock = {'price_feed': MockV3Aggregator, 'vrf_coordinator': VRFCoordinatorMock, 'link_token': LinkToken}
    c_type = name2mock[c_name]
    if network.show_active() in ['development', 'ganache-local']:
        if len(c_type) <= 0:
            deploy_mocks()
        contract = c_type[-1]
    else:
        c_address = config['networks'][network.show_active()][c_name]
        contract = Contract.from_abi(c_type._name, c_address, c_type.abi)
    return contract


def main():
    deploy_lottery()