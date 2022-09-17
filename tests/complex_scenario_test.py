from brownie import ERC20Staking, ERC20Token, accounts, chain

ONE_HOUR = 3600
REWARDS_PER_HOUR = 100 * 10**18
STAKING_PERIOD = 13 * ONE_HOUR
TOTAL_REWARDS = 13 * REWARDS_PER_HOUR

# Margin of error is 0.1 Tokens in this situation. It happens due to transactions not being instant and
# the time staked is not exactly a multiple of 1 hour
MARGIN_OF_ERROR = 1 * 10**17

# Scenario:
# User One Stakes 100 Tokens
# User Two Stakes 200 Tokens
# User Three Stakes 100 Tokens
# User One Withdraws 100 Tokens
# User One Claims Rewards
# User Three Stakes 100 Tokens
# User Two Withdraws 200 Tokens
# User Two Claims Rewards
# User Three Withdraws 200 Tokens
# User Three Claims Rewards


def test_main():
    # Setup
    owner = accounts[0]
    user_one = accounts[1]
    user_two = accounts[2]
    user_three = accounts[3]
    # Deploy
    reward_token = ERC20Token.deploy({"from": owner})
    lp_token = ERC20Token.deploy({"from": owner})
    staking = ERC20Staking.deploy(
        lp_token.address, reward_token.address, {"from": owner})
    # Mint
    lp_token.mint(user_one.address, 100 * 10**18, {"from": owner})
    lp_token.mint(user_two.address, 200 * 10**18, {"from": owner})
    lp_token.mint(user_three.address, 200 * 10**18, {"from": owner})
    reward_token.mint(staking.address, TOTAL_REWARDS, {"from": owner})
    # Approve
    lp_token.approve(staking.address, 100 * 10**18, {"from": user_one})
    lp_token.approve(staking.address, 200 * 10**18, {"from": user_two})
    lp_token.approve(staking.address, 200 * 10**18, {"from": user_three})
    # Set up Staking Period
    staking.setStakingPeriod(TOTAL_REWARDS,
                             STAKING_PERIOD, {"from": owner})
    # Forward in time 3 hours
    chain.mine(blocks=1, timedelta=ONE_HOUR * 3)
    # User One Stakes 100 Tokens
    staking.stake(100 * 10**18, {"from": user_one})
    # Forward in time 2 hours
    chain.mine(blocks=1, timedelta=ONE_HOUR * 2)
    # Assert rewards accumulation
    user_one_info_1 = staking.userStakeInfo(user_one.address)
    assert (REWARDS_PER_HOUR * 2 -
            MARGIN_OF_ERROR) < user_one_info_1[1] < (REWARDS_PER_HOUR * MARGIN_OF_ERROR)
    # User Two Stakes 200 Tokens
    staking.stake(200 * 10**18, {"from": user_two})
    # Forward in time 1 hour
    chain.mine(blocks=1, timedelta=ONE_HOUR)
    # Assert rewards accumulation
    user_one_info_2 = staking.userStakeInfo(user_one.address)
    assert (REWARDS_PER_HOUR / 3 + user_one_info_1[1] - MARGIN_OF_ERROR) < user_one_info_2[1] < (
        REWARDS_PER_HOUR / 3 + user_one_info_1[1] + MARGIN_OF_ERROR)
    user_two_info_1 = staking.userStakeInfo(user_two.address)
    assert ((REWARDS_PER_HOUR / 3) * 2 - MARGIN_OF_ERROR) < user_two_info_1[1] < (
        (REWARDS_PER_HOUR / 3) * 2 + MARGIN_OF_ERROR)
    # User Three Stakes 1 Tokens
    staking.stake(100 * 10**18, {"from": user_three})
    # Forward in time 3 hours
    chain.mine(blocks=1, timedelta=ONE_HOUR * 3)
    # Assert rewards accumulation
    user_one_info_3 = staking.userStakeInfo(user_one.address)
    assert (REWARDS_PER_HOUR * 3 / 4 + user_one_info_2[1] - MARGIN_OF_ERROR) < user_one_info_3[1] < (
        REWARDS_PER_HOUR * 3 / 4 + user_one_info_2[1] + MARGIN_OF_ERROR)
    user_two_info_2 = staking.userStakeInfo(user_two.address)
    assert (REWARDS_PER_HOUR * 3 / 2 + user_two_info_1[1] - MARGIN_OF_ERROR) < user_two_info_2[1] < (
        REWARDS_PER_HOUR * 3 / 2 + user_two_info_1[1] + MARGIN_OF_ERROR)
    user_three_info_1 = staking.userStakeInfo(user_three.address)
    assert (REWARDS_PER_HOUR * 3 / 4 - MARGIN_OF_ERROR) < user_three_info_1[1] < (
        REWARDS_PER_HOUR * 3 / 4 + MARGIN_OF_ERROR)
    # User One Withdraws 100 Tokens
    staking.withdraw(100 * 10**18, {"from": user_one})
    # Enable claiming
    staking.setClaimingState(True, {"from": owner})
    # User One Claim Rewards
    staking.claimRewards({"from": user_one})
    # Assert rewards claiming
    assert user_one_info_3[1] - MARGIN_OF_ERROR < reward_token.balanceOf(
        user_one.address) < user_one_info_3[1] + MARGIN_OF_ERROR
    # Forward in time 1 hours
    chain.mine(blocks=1, timedelta=ONE_HOUR)
    # Assert rewards accumulation
    user_two_info_3 = staking.userStakeInfo(user_two.address)
    assert (REWARDS_PER_HOUR / 3 * 2 + user_two_info_2[1] - MARGIN_OF_ERROR) < user_two_info_3[1] < (
        REWARDS_PER_HOUR / 3 * 2 + user_two_info_2[1] + MARGIN_OF_ERROR)
    user_three_info_2 = staking.userStakeInfo(user_three.address)
    assert (REWARDS_PER_HOUR / 3 + user_three_info_1[1] - MARGIN_OF_ERROR) < user_three_info_2[1] < (
        REWARDS_PER_HOUR / 3 + user_three_info_1[1] + MARGIN_OF_ERROR)
    # User Three Stakes 100 Tokens
    staking.stake(100 * 10**18, {"from": user_three})
    # Forward in time 1 hours
    chain.mine(blocks=1, timedelta=ONE_HOUR)
    # Assert rewards accumulation
    user_two_info_4 = staking.userStakeInfo(user_two.address)
    assert (REWARDS_PER_HOUR / 2 + user_two_info_3[1] - MARGIN_OF_ERROR) < user_two_info_4[1] < (
        REWARDS_PER_HOUR / 2 + user_two_info_3[1] + MARGIN_OF_ERROR)
    user_three_info_3 = staking.userStakeInfo(user_three.address)
    assert (REWARDS_PER_HOUR / 2 + user_three_info_2[1] - MARGIN_OF_ERROR) < user_three_info_3[1] < (
        REWARDS_PER_HOUR / 2 + user_three_info_2[1] + MARGIN_OF_ERROR)
    # User Two Withdraws 200 Tokens
    staking.withdraw(200 * 10**18, {"from": user_two})
    # User Two Claim Rewards
    staking.claimRewards({"from": user_two})
    # Assert rewards claiming
    assert user_two_info_4[1] - MARGIN_OF_ERROR < reward_token.balanceOf(
        user_two.address) < user_two_info_4[1] + MARGIN_OF_ERROR
    # Forward in time 2 hours
    chain.mine(blocks=1, timedelta=ONE_HOUR * 2)
    # Assert rewards accumulation
    user_three_info_4 = staking.userStakeInfo(user_three.address)
    assert (REWARDS_PER_HOUR * 2 + user_three_info_3[1] - MARGIN_OF_ERROR) < user_three_info_4[1] < (
        REWARDS_PER_HOUR * 2 + user_three_info_3[1] + MARGIN_OF_ERROR)
    # User Three Withdraws 200 Tokens
    staking.withdraw(200 * 10**18, {"from": user_three})
    # User Three Claim Rewards
    staking.claimRewards({"from": user_three})
    # Assert rewards claiming
    assert user_three_info_4[1] - MARGIN_OF_ERROR < reward_token.balanceOf(
        user_three.address) < user_three_info_4[1] + MARGIN_OF_ERROR
    # Assert balance left in Stkaing Contract for first 3 hours
    assert REWARDS_PER_HOUR * 3 - MARGIN_OF_ERROR < reward_token.balanceOf(
        staking.address) < REWARDS_PER_HOUR * 3 + MARGIN_OF_ERROR
