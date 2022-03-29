from brownie import network, exceptions
from web3 import Web3
import pytest
from scripts.deploy_lottery import get_account, get_contract, deploy_lottery

def link_payment(c_address, account=None, link_token=None, amount=10**18): 
    account = get_account()
    link_token = get_contract("link_token")
    payment = link_token.transfer(c_address, amount, {'from': account})
    payment.wait(1)
    return payment

def test_lottery():
    if network.show_active() not in ['development', 'ganache-local']:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    assert lottery.getEntryFee() == Web3.toWei(0.025, 'ether')
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from': account, 'value': lottery.getEntryFee()})
    lottery.start({"from": account})
    assert lottery.players(0) == account
    lottery.enter({'from': account, 'value': lottery.getEntryFee()})
    lottery.enter({'from': get_account(index=1), 'value': lottery.getEntryFee()})
    prev_balance = account.balance()
    prev_pool = lottery.balance()
    link_payment(lottery)
    Txn = lottery.end({'from': account})
    Txn.wait(1)
    req_id = Txn.events['RequestedRandomness']['requestId']
    get_contract('vrf_coordinator').callBackWithRandomness(req_id, 777, lottery.address, {'from': account})
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == prev_balance+prev_pool

def main():
    test_lottery()
