from brownie import accounts, config, network, Lottery

def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy()

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
    pass


def main():
    deploy_lottery()