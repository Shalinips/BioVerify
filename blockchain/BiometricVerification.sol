// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract BiometricVerification {

    struct Verification {
        string userId;
        string verificationHash;
        bool verified;
        uint256 timestamp;
    }

    // Directly connects each user ID to their verification record
    mapping(string => Verification) public verifications;

    // Keeps track of how many users/records have been stored
    uint256 public verificationCount;

    function recordVerification(
        string memory _userId,
        string memory _verificationHash,
        bool _verified
    ) public {

        verifications[_userId] = Verification(
            _userId,
            _verificationHash,
            _verified,
            block.timestamp
        );

        verificationCount++;
    }

    function getVerification(
        string memory _userId
    )
        public
        view
        returns (
            string memory userId,
            string memory verificationHash,
            bool verified,
            uint256 timestamp
        )
    {
        Verification memory v = verifications[_userId];

        return (
            v.userId,
            v.verificationHash,
            v.verified,
            v.timestamp
        );
    }
}