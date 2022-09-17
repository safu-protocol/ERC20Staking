from brownie import ERC20Staking, ERC20Token, accounts, chain

# Multiple staking periods without the user withdrawing the NFT between them


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
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # Stake
    staking.stake(10 * 10**18, {"from": owner})
    # Forward in time
    chain.mine(blocks=1, timedelta=3601)
    # Get claimable rewards for address
    stake_details_1 = staking.userStakeInfo(owner.address)
    # Claim rewards
    staking.claimRewards({"from": owner})
    # Assert rewards claiming
    assert token.balanceOf(owner.address) == stake_details_1[1]
    # Set up Second Staking Period
    token.mint(staking.address, 100 * 10**18, {"from": owner})
    staking.setStakingPeriod(100 * 10**18, 3600, {"from": owner})
    # Forward in time
    chain.mine(blocks=1, timedelta=3601)
    # Get claimable rewards for address
    stake_details_2 = staking.userStakeInfo(owner.address)
    # Claim rewards
    staking.claimRewards({"from": owner})
    # Assert rewards claiming
    assert token.balanceOf(
        owner.address) == stake_details_1[1] + stake_details_2[1]
