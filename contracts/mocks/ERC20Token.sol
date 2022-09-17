// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20Token is ERC20 {
    constructor() ERC20("Test Token", "TT") {}

    function mint(address _account, uint256 _amount) public {
        super._mint(_account, _amount);
    }
}
