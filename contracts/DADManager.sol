// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DADManager {
    event DADSubmitted(address indexed sender, string dadHash);

    string[] public dadHashes;

    function submitDAD(string memory dadHash) public {
        dadHashes.push(dadHash);
        emit DADSubmitted(msg.sender, dadHash);
    }

    function getDAD(uint index) public view returns (string memory) {
        return dadHashes[index];
    }

    function getTotalDADs() public view returns (uint) {
        return dadHashes.length;
    }
}
