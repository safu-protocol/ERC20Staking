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
    # Mint
    lp_token.mint(owner.address, 10 * 10**18, {"from": owner})
    lp_token.approve(staking.address, 10 * 10**18, {"from": owner})
    token.mint(staking.address, 100 * 10**18, {"from": owner})
    # Set up Staking Period
    staking.setStakingPeriod(100 * 10**18, 3600, {"from": owner})
    # Stake
    lp_token.approve(staking.address, 10 * 10**18, {"from": owner})
    stake_tx1 = staking.stake(10 * 10**18, {"from": owner})
    # Forward in time
    chain.mine(blocks=1, timedelta=3601)
    deposti_info = staking.userStakeInfo(owner.address)
    # Withdraw all not working when claiming disabled
    with brownie.reverts():
        staking.withdrawAll({"from": owner})
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # Withdraw all
    staking.withdrawAll({"from": owner})
    # Assert withdraw all
    assert staking.userStakeInfo(owner.address) == [0, 0]
    assert token.balanceOf(owner.address) == deposti_info[1]
