from brownie import MockV3Aggregator, VRFCoordinatorMock, LinkToken
from scripts.deploy_lottery import get_account

def deploy_mocks(decimals=8, initial_value=2*10**12):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})