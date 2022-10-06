from brownie import ERC20Staking, ERC20Token, accounts, chain

duration = 60 * 60 * 24 * 30 * 3  # 3 months
rewards_amount = 500000 * 10**18


def test_main():
    # Setup
    owner = accounts[0]
    # Deploy
    token = ERC20Token.deploy({"from": owner})
    lp_token = ERC20Token.deploy({"from": owner})
    staking = ERC20Staking.deploy(
        lp_token.address, token.address, {"from": owner})
    # Mint
    lp_token.mint(owner.address, 0.9 * 10**18, {"from": owner})
    token.mint(staking.address, rewards_amount, {"from": owner})
    # Set up Staking Period
    staking.setStakingPeriod(rewards_amount, duration, {"from": owner})
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # Stake
    lp_token.approve(staking.address, 0.9 * 10**18, {"from": owner})
    stake_tx1 = staking.stake(0.9 * 10**18, {"from": owner})
    print(stake_tx1.info())
    # Forward in time
    chain.mine(blocks=1, timedelta=duration + 1000)
    # Check the rewards
    print(
        f"Rewards for user after staking period are: {staking.userStakeInfo(owner.address)[1] / 10**18}")
