// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Copyright {
    struct File {
        string content;  // 文章內容
        bool registered; // 是否已註冊
    }

    mapping(uint256 => File) public registeredFiles; // 已註冊的文章
    uint256 public totalFiles; 
    address public owner; 

    //把合約持有者設為部署者地址
    constructor() {
        owner = msg.sender;
        totalFiles = 0;
    }
    
    // 檢查是否為合約持有者
    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner!"); 
        _;
    }

    // 註冊新文章
    function registerFile(string memory content) public onlyOwner {
        totalFiles++;
        registeredFiles[totalFiles] = File(content, true); 
    }

    // 檢查文章是否已註冊
    function isWorkRegistered(uint256 fileId) public view returns (bool) {
        return registeredFiles[fileId].registered; 
    }

    // 獲取文章的內容
    function getWorkContent(uint256 fileId) public view returns (string memory) {
        return registeredFiles[fileId].content;
    }

    // 獲取文章總數
    function getToTalFiles() public view returns (uint256) {
        return totalFiles;
    }
}
