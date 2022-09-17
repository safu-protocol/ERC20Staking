from brownie import ERC20Staking, ERC20Token, accounts, chain
import brownie


def test_main():
    # Setup
    owner = accounts[0]
    # Deploy
    token = ERC20Token.deploy({"from": owner})
    lp_token = ERC20Token.deploy({"from": owner})
    staking = ERC20Staking.deploy(
        lp_token.address, token.address, {"from": owner})
    # Revert setStakingPeriod if Staking Contract does not have tokens
    with brownie.reverts():
        staking.setStakingPeriod(100 * 10**18, 3600, {"from": owner})
    # Send rewards tokens to Staking Contract
    token.mint(staking.address, 100 * 10**18, {"from": owner})
    # REvert setStakingPeriod if Staking Contract has less tokens then what I wish to distribute
    with brownie.reverts():
        staking.setStakingPeriod(101 * 10**18, 3600, {"from": owner})
    # Set up Staking Period
    staking.setStakingPeriod(100 * 10**18, 3600, {"from": owner})
    time_stamp = chain.time()
    print(time_stamp)
    # Check period finish
    assert staking.periodFinish() == time_stamp + 3600
