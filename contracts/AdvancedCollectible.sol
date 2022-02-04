//SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum MHA {
        DEKU,
        TOKYAMI_ASUI,
        DEKU_DEKUPOOL
    }
    mapping(uint256 => MHA) public tokenIdToMHA;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event tokenAssigned(uint256 indexed tokenId, MHA mha);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee,
        string memory _tokenName,
        string memory _tokenSymbol
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721(_tokenName, _tokenSymbol)
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        MHA mha = MHA(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToMHA[newTokenId] = mha;
        emit tokenAssigned(newTokenId, mha);
        address sender = requestIdToSender[requestId];
        _safeMint(sender, newTokenId);
        //_setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC720:Caller is not owner or approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
