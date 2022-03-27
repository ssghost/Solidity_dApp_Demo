// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;
    uint public usdPrice = 5 * 10 ** 18;

    AggregatorV3Interface internal priceFeed;
    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function enter() public payable {
        players.push(payable(msg.sender));

    }

    function getEntryFee() public view returns(uint) {
        (, int price,,,,) = priceFeed.latestRoundData;
        return uint((usdPrice * 10 **8) / uint(price));
    }

    function start() public {}

    function end() public {}
}