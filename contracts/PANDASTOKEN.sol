// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <0.9.0;
pragma abicoder v2;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Pausable.sol";
import "./PantosBaseToken.sol";
/**
 * @title Pantos-compatible Example Token
 */
contract PANDASTOKEN is PantosBaseToken, ERC20Burnable, ERC20Pausable {
    string private constant _NAME = "PANDAS";
    string private constant _SYMBOL = "PANDAS";
    uint8 private constant _DECIMALS = 18;

    /// @dev msg.sender receives all existing tokens.
    constructor(uint256 initialSupply)
        PantosBaseToken(_NAME, _SYMBOL, _DECIMALS)
    {
        ERC20._mint(msg.sender, initialSupply);
        // Contract is paused until it is fully initialized
    }

    /// *******************************************************************************************************
    /// Override requirements
    /// *******************************************************************************************************

    /// @dev See {PantosBaseToken-decimals} and {ERC20-decimals}.
    function decimals()
        public
        view
        override(PantosBaseToken, ERC20)
        returns (uint8)
    {
        return PantosBaseToken.decimals();
    }

    /// @dev See {PantosBaseToken-symbol} and {ERC20-symbol}.
    function symbol()
        public
        view
        override(PantosBaseToken, ERC20)
        returns (string memory)
    {
        return PantosBaseToken.symbol();
    }

    /// @dev See {PantosBaseToken-name} and {ERC20-name}.
    function name()
        public
        view
        override(PantosBaseToken, ERC20)
        returns (string memory)
    {
        return PantosBaseToken.name();
    }

    /// *******************************************************************************************************
    /// Pantos Functions
    /// *******************************************************************************************************

    /// @dev See {PantosBaseToken-_setPantosForwarder}.
    function setPantosForwarder(address pantosForwarder)
        external
        onlyOwner
    {
        _setPantosForwarder(pantosForwarder);
    }

    /// *******************************************************************************************************
    /// OZ Functions - Pausable
    /// *******************************************************************************************************

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    /// @dev See {ERC20Pausable-_beforeTokenTransfer}.
    function _beforeTokenTransfer(
        address sender,
        address recipient,
        uint256 amount
    )
        internal
        override(ERC20, ERC20Pausable)
    {
        ERC20Pausable._beforeTokenTransfer(sender, recipient, amount);
    }






}