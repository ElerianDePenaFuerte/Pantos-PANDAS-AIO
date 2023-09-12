// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <0.9.0;
pragma abicoder v2;
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../interfaces/IPantosToken.sol";
/**
 * @title Pantos base token
 */
abstract contract PantosBaseToken is IPantosToken, ERC20, Ownable {
    uint8 private _decimals;
    address private _pantosForwarder;
    constructor(string memory name_, string memory symbol_, uint8 decimals_)
        ERC20(name_, symbol_)
    {
        _decimals = decimals_;
    }
    modifier onlyPantosForwarder() virtual {
        require(
            _pantosForwarder != address(0),
            "PantosBaseToken: PantosForwarder has not been set"
        );
        require(
            msg.sender == _pantosForwarder,
            "PantosBaseToken: caller is not the PantosForwarder"
        );
        _;
    }
    /// @dev See {IPantosToken-pantosTransfer}.
    function pantosTransfer(address sender, address recipient, uint256 amount)
        public
        virtual
        override
        onlyPantosForwarder
    {
        _transfer(sender, recipient, amount);
    }
    /// @dev See {IPantosToken-pantosTransferFrom}.
    function pantosTransferFrom(address sender, uint256 amount)
        public
        virtual
        override
        onlyPantosForwarder
    {
        _burn(sender, amount);
    }
    /// @dev See {IPantosToken-pantosTransferTo}.
    function pantosTransferTo(address recipient, uint256 amount)
        public
        virtual
        override
        onlyPantosForwarder
    {
        _mint(recipient, amount);
    }
    /// @dev See {IBEP20-decimals} and {ERC20-decimals}.
    function decimals()
        public
        view
        virtual
        override(IBEP20, ERC20)
        returns (uint8)
    {
        return _decimals;
    }
    /// @dev See {IBEP20-symbol} and {ERC20-symbol}.
    function symbol()
        public
        view
        virtual
        override(IBEP20, ERC20)
        returns (string memory)
    {
        return ERC20.symbol();
    }
    /// @dev See {IBEP20-name} and {ERC20-name}.
    function name()
        public
        view
        virtual
        override(IBEP20, ERC20)
        returns (string memory)
    {
        return ERC20.name();
    }
    /// @dev See {IBEP20-getOwner} and {Ownable-owner}.
    function getOwner() public view virtual override returns (address) {
        return owner();
    }
    /// @dev See {IPantosToken-getPantosForwarder}.
    function getPantosForwarder()
        public
        view
        virtual
        override
        returns (address)
    {
        return _pantosForwarder;
    }
    function _setPantosForwarder(address pantosForwarder)
        internal
        virtual
        onlyOwner
    {
        require(
            pantosForwarder != address(0),
            "PantosBaseToken: PantosForwarder must not be the zero account"
        );
        _pantosForwarder = pantosForwarder;
        emit PantosForwarderSet(pantosForwarder);
    }
    function _unsetPantosForwarder()
        internal
        virtual
        onlyOwner
    {
        _pantosForwarder = address(0);
        emit PantosForwarderUnset();
    }
}