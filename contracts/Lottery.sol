// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    address payable[] public players;
    uint public usdPrice = 5 * 10 ** 18;

    enum State {Open, Close, Calculating}
    State public state;

    AggregatorV3Interface internal priceFeed;
    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        state = State.Close;
    }

    function enter() public payable {
        require(msg.value >= getEntryFee());
        require(state == State.Open);
        players.push(payable(msg.sender));

    }

    function getEntryFee() public view returns(uint) {
        (, int price,,,,) = priceFeed.latestRoundData;
        return uint((usdPrice * 10 **8) / uint(price));
    }

    function start() public onlyOwner {}

    function end() public onlyOwner {}
}