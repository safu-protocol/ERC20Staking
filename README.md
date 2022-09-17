# ERC20Staking Smart Contract with Dynamic Rewards
### A fixed amount of rewards is distributed in a period chosen by the Owner of the contract. Users can stake their LP Tokens to get ERC20 Token rewards. For each second of that period, there is a Tokens per Second value(Total rewards distributed devided by seconds in the Staking period), that is split between the Users that stake in the said second and each user is allocated tokens based on their stake's share of the total amount of LP Tokens staked.

#### Created using the Synthetix [Staking Rewards](https://github.com/Synthetixio/synthetix/blob/v2.76.0-alpha/contracts/StakingRewards.sol) Contract logic.

## Features:

### For users:

1. Deposit your LP Tokens and claim a dynamic amount of ERC20 Tokens calculated as a share of the total rewards distributed per second. The users share of the rewards pool is proportional to their stake's share of total LP Tokens staked.
1. Withdraw your LP Tokens.
1. Claim rewards.
1. Withdraw all your LP Tokens and Claim Rewards in one transaction.

### For owner:

1. Distribute a fixed amount of ERC20 Tokens in a set period of time by LP Tokens Locking(Staking).
1. Set a fixed amount of ERC20 Tokens to be rewarded of a staking period.
1. Set multiple staking periods.


### Dev notes:

1. Getter functions designed to help with the UX/UI have been implemented in the contract to be able to get an amount of LP Tokens staked by each staker by passing a wallet address and the amount of ERC20 Tokens earned by the specified address.

## Prerequisites:

- [Python](https://www.python.org/downloads/)
- Brownie
```
sudo apt install python3-pip
sudo apt install python3.8-venv

python3 -m pip install --user pipx
python3 -m pipx ensurepath
# restart terminal
pipx install eth-brownie
```
- A free [Infura](https://infura.io/) Project Id key for Rinkeby Network
- [Node.js](https://nodejs.org/en/) >=  v12.0.0 and npm >= 6.12.0
- [Ganache](https://github.com/trufflesuite/ganache#readme)

### Instalation 

Clone this repo:

```
git clone https://github.com/safuyield/SafuERC20Staking
cd SafuERC20Staking
```

### Run tests

You can find the test scripts in the `tests` folder. To run a test script use the command:
```
brownie test tests/<NAME_OF_THE_SCRIPT_FILE>
```

### Deploy to Goerli

- Add a `.env` file with the same contents of `.env.example`, but replaced with your variables.

- Run the command:
```
brownie run scripts/deploy.py --network goerli
```
- Input your LP Token Contract Address
- Input your ERC20 Rewards Token Contract Address

The script will deploy the LP Token Staking Smart Contract and verify it on goerli.etherscan.io.

### Made with ♥ by Andrei Toma
