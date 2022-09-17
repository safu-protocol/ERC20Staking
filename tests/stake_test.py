from brownie import ERC20Staking, ERC20Token, accounts, chain


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
    stake_tx1 = staking.stake(10 * 10**18, {"from": owner})
    # Assert staking
    deposti_info = staking.userStakeInfo(owner.address)
    assert deposti_info[0] == 10 * 10**18
