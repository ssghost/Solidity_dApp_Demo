// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    address payable public recentWinner;
    uint public usdPrice = 5 * 10 ** 18;

    enum State {Open, Close, Entered, Calculating}
    State public state;

    bytes public keyHash;
    uint public vrfFee;
    uint public randomness;

    AggregatorV3Interface internal priceFeed;
    constructor(address _priceFeed, address _vrfCoordinator, address _link, bytes _keyHash, uint _vrfFee) public VRFConsumerBase(_vrfCoordinator, _link) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        state = State.Close;
        keyHash = _keyHash;
        vrfFee = _vrfFee;
    }

    function enter() public payable {
        require(msg.value >= getEntryFee());
        require(state == State.Open);
        players.push(payable(msg.sender));
        state = State.Entered;
    }

    function getEntryFee() public view returns(uint) {
        (, int price,,,,) = priceFeed.latestRoundData;
        return uint((usdPrice * 10 ** 8) / uint(price));
    }

    function start() public onlyOwner {
        require(state == State.Close);
        state == State.Open;
    }

    function end() public onlyOwner {
        require(state == State.Entered);
        state = State.Calculating;
        bytes reqId = requestRandomness(keyHash, vrfFee);
        uint result = fulfillRandomness(reqId, randomness); 
        recentWinner = players[result];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);
        state = State.Close;
    }

    function fulfillRandomness(bytes _reqId, uint _randomness) internal override view returns(uint) {
        require(state == State.Calculating);
        require(_randomness > 0);
        return uint(_randomness % players.length);
    }
}