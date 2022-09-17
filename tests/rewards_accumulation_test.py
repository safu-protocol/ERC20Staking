from brownie import ERC20Staking, ERC20Token, accounts, chain


def test_main():
    # Setup
    owner = accounts[0]
    user = accounts[1]
    # Deploy
    token = ERC20Token.deploy({"from": owner})
    lp_token = ERC20Token.deploy({"from": owner})
    staking = ERC20Staking.deploy(
        lp_token.address, token.address, {"from": owner})
    # Mint
    lp_token.mint(owner.address, 20 * 10**18, {"from": owner})
    lp_token.mint(user.address, 20 * 10**18, {"from": owner})
    token.mint(staking.address, 1000000 * 10**18, {"from": owner})
    # Set up Staking Period
    staking.setStakingPeriod(100 * 10**18, 3600, {"from": owner})
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # Stake
    lp_token.approve(staking.address, 10 * 10**18, {"from": owner})
    stake_tx1 = staking.stake(10 * 10**18, {"from": owner})
    print(stake_tx1.info())
    # Forward in time
    chain.mine(blocks=1, timedelta=3600 / 2)
    # Stake agian form owner and user
    lp_token.approve(staking.address, 10 * 10**18, {"from": owner})
    stake_tx2 = staking.stake(10 * 10**18, {"from": owner})
    lp_token.approve(staking.address, 20 * 10**18, {"from": user})
    stake_tx3 = staking.stake(20 * 10**18, {"from": user})
    # Check for userStakeInfo accuracy
    print(staking.userStakeInfo(owner.address))
    print(staking.userStakeInfo(user.address))
    # Forward in time
    chain.mine(blocks=1, timedelta=3600 / 2)
    # Check for userStakeInfo accuracy
    print(staking.userStakeInfo(owner.address))
    print(staking.userStakeInfo(user.address))
    # Claim from owner and user
    claim_tx2 = staking.claimRewards({"from": owner})
    print(token.balanceOf(owner.address))
    claim_tx3 = staking.claimRewards({"from": user})
    print(token.balanceOf(user.address))
    # Check for userStakeInfo accuracy
    print(staking.userStakeInfo(owner.address))
    print(staking.userStakeInfo(user.address))
