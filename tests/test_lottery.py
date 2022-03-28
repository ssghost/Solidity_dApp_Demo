from brownie import Lottery, config, network
from web3 import Web3

def test_getEntryFee():
    account = get_account()
    lottery = Lottery.deploy(config['networks'][network.show_active()]['price_feed'], {'from': account})
    assert lottery.getEntryFee() > Web3.toWei(0.019, 'ether')
    assert lottery.getEntryFee() < Web3.toWei(0.021, 'ether') 
