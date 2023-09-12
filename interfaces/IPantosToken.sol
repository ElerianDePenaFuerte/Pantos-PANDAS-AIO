// SPDX-License-Identifier: UNLICENSED
pragma solidity >=0.8.0 <0.9.0;
pragma abicoder v2;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./IBEP20.sol";
/**
 * @title Pantos token interface
 */
interface IPantosToken is IERC20, IBEP20 {
    event PantosForwarderSet(address pantosForwarder);
    event PantosForwarderUnset();
    // Only callable by the trusted Pantos forwarder
    function pantosTransfer(address sender, address recipient, uint256 amount)
        external;
    // Only callable by the trusted Pantos forwarder
    function pantosTransferFrom(address sender, uint256 amount) external;
    // Only callable by the trusted Pantos forwarder
    function pantosTransferTo(address recipient, uint256 amount) external;
    function getPantosForwarder() external view returns (address);
}