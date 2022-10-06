from brownie import ERC20Staking, ERC20Token, accounts, chain

duration = 60 * 60 * 24 * 30 * 3  # 3 months
rewards_amount = 500000 * 10**18


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
    lp_token.mint(owner.address, 0.005 * 10**18, {"from": owner})
    lp_token.mint(user.address, 0.045 * 10**18, {"from": user})
    token.mint(staking.address, rewards_amount, {"from": owner})
    # Set up Staking Period
    staking.setStakingPeriod(rewards_amount, duration, {"from": owner})
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # Stake
    lp_token.approve(staking.address, 0.005 * 10**18, {"from": owner})
    stake_tx1 = staking.stake(0.005 * 10**18, {"from": owner})
    lp_token.approve(staking.address, 0.045 * 10**18, {"from": user})
    stake_tx2 = staking.stake(0.045 * 10**18, {"from": user})
    # Forward in time
    chain.mine(blocks=1, timedelta=duration + 1000)
    # Check the rewards
    print(
        f"Rewards for user 1 after staking period are: {staking.userStakeInfo(owner.address)[1] / 10**18}")
    print(
        f"Rewards for user 2 after staking period are: {staking.userStakeInfo(user.address)[1] / 10**18}")
