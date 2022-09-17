from brownie import ERC20Staking, ERC20Token, accounts, chain
import brownie


def test_main():
    # Setup
    owner = accounts[0]
    # Deploy
    reward_token = ERC20Token.deploy({"from": owner})
    lp_token = ERC20Token.deploy({"from": owner})
    staking = ERC20Staking.deploy(
        lp_token.address, reward_token.address, {"from": owner})
    # Mint
    lp_token.mint(owner.address, 10 * 10**18, {"from": owner})
    lp_token.approve(staking.address, 10 * 10**18, {"from": owner})
    reward_token.mint(staking.address, 100 * 10**18, {"from": owner})
    # Set up Staking Period
    staking.setStakingPeriod(100 * 10**18, 3600, {"from": owner})
    # Stake
    staking.stake(10 * 10**18, {"from": owner})
    # Forward in time
    chain.mine(blocks=1, timedelta=3601)
    # Get claimable rewards for address
    stake_details = staking.userStakeInfo(owner.address)
    # Assert Claiming not working when disabled
    with brownie.reverts():
        staking.claimRewards({"from": owner})
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # Claim rewards
    staking.claimRewards({"from": owner})
    # Assert rewards claiming
    assert reward_token.balanceOf(owner.address) == stake_details[1]
