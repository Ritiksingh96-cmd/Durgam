// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title MerkleEvidenceLocker
 * @author Project DURGAM (SIH 2026 / I4C National Cybercrime Reporting)
 * @notice Sovereign On-Chain Merkle Evidence Notarization for Section 63 BSA Compliance
 * 
 * Slashes on-chain transaction footprint by batching 500 complaints / hourly Merkle roots.
 * Reduces national sovereign gas expenditure to < 0.032 POL/day (~ ₹1.25/day for all of India).
 */
contract MerkleEvidenceLocker {
    address public sovereignAuthority;
    
    struct EvidenceBatch {
        bytes32 merkleRoot;
        uint256 batchId;
        uint256 complaintCount;
        uint256 timestamp;
        string jurisdictionCode; // e.g. "DL-DELHI", "JK-JAMMU", "NAT-CENTRAL"
        bytes signature;
    }
    
    // batchId => EvidenceBatch
    mapping(uint256 => EvidenceBatch) public evidenceBatches;
    uint256 public totalBatches;
    uint256 public totalComplaintsSealed;
    
    event MerkleRootCommitted(
        uint256 indexed batchId,
        bytes32 indexed merkleRoot,
        uint256 complaintCount,
        uint256 timestamp,
        string jurisdictionCode
    );
    
    modifier onlyAuthority() {
        require(msg.sender == sovereignAuthority, "DURGAM: Caller is not authorized sovereign node");
        _;
    }
    
    constructor() {
        sovereignAuthority = msg.sender;
    }
    
    function setSovereignAuthority(address _newAuthority) external onlyAuthority {
        require(_newAuthority != address(0), "Invalid address");
        sovereignAuthority = _newAuthority;
    }
    
    /**
     * @notice Commits an hourly/500-complaint Merkle Root off-chain calculated by DURGAM backend
     */
    function commitMerkleRoot(
        bytes32 _merkleRoot,
        uint256 _complaintCount,
        string calldata _jurisdictionCode,
        bytes calldata _signature
    ) external onlyAuthority returns (uint256 batchId) {
        totalBatches++;
        batchId = totalBatches;
        
        evidenceBatches[batchId] = EvidenceBatch({
            merkleRoot: _merkleRoot,
            batchId: batchId,
            complaintCount: _complaintCount,
            timestamp: block.timestamp,
            jurisdictionCode: _jurisdictionCode,
            signature: _signature
        });
        
        totalComplaintsSealed += _complaintCount;
        
        emit MerkleRootCommitted(batchId, _merkleRoot, _complaintCount, block.timestamp, _jurisdictionCode);
        return batchId;
    }
    
    /**
     * @notice Cryptographic inclusion verification for Section 63 BSA court presentation
     * @dev Validates whether a specific leaf hash exists within the committed Merkle Root
     */
    function verifyEvidenceInclusion(
        uint256 _batchId,
        bytes32 _leafHash,
        bytes32[] calldata _merkleProof
    ) external view returns (bool isValid, uint256 sealedTimestamp, string memory jurisdiction) {
        EvidenceBatch memory batch = evidenceBatches[_batchId];
        require(batch.batchId != 0, "Batch does not exist");
        
        bytes32 computedHash = _leafHash;
        for (uint256 i = 0; i < _merkleProof.length; i++) {
            bytes32 proofElement = _merkleProof[i];
            if (computedHash <= proofElement) {
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }
        
        isValid = (computedHash == batch.merkleRoot);
        sealedTimestamp = batch.timestamp;
        jurisdiction = batch.jurisdictionCode;
    }
}
