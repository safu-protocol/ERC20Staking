from brownie import ERC20Staking, accounts, config


def main():
    account = accounts.add(config["wallets"]["from_key"])
    lp_address = input("Enter your LP Token Contract Address: ")
    token_address = input("Enter your ERC20 Rewards Token Address: ")
    staking = ERC20Staking.deploy(
        lp_address, token_address, {"from": account}, publish_source=True
    )
