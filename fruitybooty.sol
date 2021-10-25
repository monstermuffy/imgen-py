// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract FruityBooties is ERC721Enumerable, Ownable {
    using Strings for uint256;
    
    //events
    event BaseTokenURIChanged(string baseTokenURI);

    // uint256 constant state variables
    uint256 public constant TOTAL_FRUITS = 12000; // Maximum amount of Fruity Booties
    uint256 public constant RESERVED_FRUITS = 200; // Amount reserved for the team/giveaways
    uint256 public constant TOTAL_MINT = TOTAL_FRUITS - RESERVED_FRUITS; // Maximum amount of Fruity Booties
    uint256 public constant PRESALE_FRUITS = 6000; // Maximum to be minted during presale
    uint256 public constant MAX_PRESALE = 2; // Maximum fruits that can be minted per address in presale
    uint256 public constant MAX_PER_MINT = 5; // Maximum fruits to be minted per transaction
    uint256 public constant MAX_PER_ADDR = 50; // Each person can't mint more than 50
    uint256 public constant PRICE = 0.05 ether; // Price of mint in ether

    uint256 public reservedClaimed;

    // addresses of the teams wallets
    address public constant devAddress = 0x09Ec8699b5974cD1e1F2eaF84954E6Ae2607ACaf;

    // booleans for whether presale/public sale has started
    bool public publicSaleStarted;
    bool public presaleStarted;

    // mapping addresses for presale list
    mapping(address => bool) private _presaleList;
    mapping(address => uint256) private _presaleClaimed;

    // string variables
    string private _baseTokenURI;
    
    // ERC721 constructor
    constructor() ERC721("Fruity Booty Kitchen Club", "FBKC") {}

    function claimedReserved(uint256 amount, address addr) external onlyOwner {
        require(reservedClaimed != RESERVED_FRUITS, "All reserved fruits have been claimed");
        require(reservedClaimed + amount <= RESERVED_FRUITS, "Claiming this many fruits would exceed total supply");
        require(addr != address(0), "Cannot claim to null address");
        require(totalSupply() < TOTAL_FRUITS, "All fruits have been minted/claimed");
        require(totalSupply() + amount <= TOTAL_FRUITS, "Minting would exceed total supply");

        for (uint256 i = 0; i < amount; i++) {
            _safeMint(addr, totalSupply() + 1);
        }
        reservedClaimed += amount;
    }
    // presale minting function
    function mintPresale(uint256 quantity) external payable {
        require(totalSupply() < TOTAL_MINT, "All booties have been minted");        
        require(quantity > 0, "Must mint at least one");
        require(_presaleList[msg.sender], "Address not on the presale list");
        require(presaleStarted == true, "Presale has not started");
        require(_presaleClaimed[msg.sender] < MAX_PRESALE, "Address has reached their presale limit");
        require(_presaleClaimed[msg.sender] + quantity <= MAX_PRESALE, "Minting this many would exceed presale limit");
        require(PRICE * quantity == msg.value, "ETH amount incorrect");
        require(totalSupply() + quantity <= TOTAL_MINT, "Minting would exceed max supply");

        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(msg.sender, totalSupply() + 1);
            _presaleClaimed[msg.sender] += 1;
        }
    }

    //public sale minting function
    function mintPublic(uint256 quantity) external payable {
        require(totalSupply() < TOTAL_MINT, "All booties have been minted");
        require(quantity > 0, "Must mint at least one");
        require(publicSaleStarted == true, "Public sale has not started");
        require(quantity <= MAX_PER_MINT, "Can mint more than 5 at once");
        require(PRICE * quantity == msg.value, "ETH amount incorrect");
        require(totalSupply() + quantity <= TOTAL_MINT, "Minting would exceed max supply");

        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(msg.sender, totalSupply() + 1);
        }
    }
    
    //set the baseTokenURI
    function setBaseTokenURI(string calldata URI) external onlyOwner {
        _baseTokenURI = URI;
        emit BaseTokenURIChanged(URI);
    }

    //return the baseTokenURI
    function baseTokenURI() public view returns (string memory) {
        return _baseTokenURI;
    }

    //checks URI of a specific token
    function tokenURI(uint256 tokenId) public view override(ERC721) returns (string memory) {
        require(_exists(tokenId), "Cannot query non-existent token");
        
        return string(abi.encodePacked(_baseTokenURI, tokenId.toString()));
    }

    // function to toggle the presale
    function togglePresaleStarted() external onlyOwner {
        presaleStarted = !presaleStarted;
    }

    // function to toggle the public sale
    function togglePublicSaleStarted() external onlyOwner {
        publicSaleStarted = !publicSaleStarted;
    }

    // to check if an address has been added to the presale list
    function checkPresaleList(address addr) external view returns (bool) {
        return _presaleList[addr];
    }

    // function to add a list of addresses to the presale list
    function addToPresaleList(address[] calldata addresses) external onlyOwner {
        for(uint256 i = 0; i < addresses.length; i++) {
            require(addresses[i] != address(0), "Can't add to null address");
            require(!_presaleList[addresses[i]], "Address is already in presale");

            _presaleList[addresses[i]] = true;
            _presaleClaimed[addresses[i]] = 0;
        }
    }

    function removeFromPresale(address addr) external onlyOwner {
            _presaleList[addr] = false;
    }

    function numClaimedPresale(address addr) external view returns (uint256) {            
            return _presaleClaimed[addr];
        }

    function withdrawAll() public onlyOwner {
        require(payable(devAddress).send(address(this).balance), "Failed to withdraw");
    }
}