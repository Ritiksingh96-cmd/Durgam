import hashlib
from typing import List, Tuple, Dict, Optional

class MerkleTree:
    """
    Off-Chain Cryptographic Binary Merkle Tree for Section 63 BSA Digital Evidence Locker.
    Enables instant proof generation for court dossiers with only O(log2 N) hash elements.
    """
    def __init__(self, leaves: List[str]):
        """
        leaves: list of SHA-256 hex strings representing serialized complaint telemetry
        """
        self.raw_leaves = leaves
        self.leaf_hashes = [self._normalize_hash(l) for l in leaves] if leaves else [hashlib.sha256(b"DURGAM_GENESIS_LEAF").hexdigest()]
        self.tree_levels = self._build_tree(self.leaf_hashes)
        self.root = self.tree_levels[-1][0] if self.tree_levels else ""

    def _normalize_hash(self, val: str) -> str:
        if len(val) == 64:
            return val.lower()
        return hashlib.sha256(val.encode('utf-8')).hexdigest().lower()

    def _hash_pair(self, left: str, right: str) -> str:
        # Lexicographical sort for canonical tree matching Solidity MerkleProof
        if left <= right:
            combined = bytes.fromhex(left) + bytes.fromhex(right)
        else:
            combined = bytes.fromhex(right) + bytes.fromhex(left)
        return hashlib.sha256(combined).hexdigest().lower()

    def _build_tree(self, current_level: List[str]) -> List[List[str]]:
        levels = [current_level]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i+1] if i + 1 < len(current_level) else current_level[i]
                parent = self._hash_pair(left, right)
                next_level.append(parent)
            levels.append(next_level)
            current_level = next_level
        return levels

    def get_proof(self, leaf_index: int) -> List[Dict[str, str]]:
        """
        Generate Merkle audit proof array for a given leaf index.
        Returns list of {hash: str, position: 'left'|'right'}
        """
        if leaf_index < 0 or leaf_index >= len(self.leaf_hashes):
            raise IndexError("Leaf index out of bounds")

        proof = []
        idx = leaf_index
        for level in self.tree_levels[:-1]:
            is_right_child = (idx % 2 == 1)
            pair_idx = idx - 1 if is_right_child else idx + 1
            if pair_idx < len(level):
                sibling = level[pair_idx]
            else:
                sibling = level[idx]  # duplicate last node if odd
            
            proof.append({
                "hash": "0x" + sibling,
                "position": "left" if is_right_child else "right"
            })
            idx = idx // 2
        return proof

    @staticmethod
    def verify_proof(leaf_hash: str, proof: List[Dict[str, str]], expected_root: str) -> bool:
        """
        Verify that leaf_hash belongs to expected_root given the proof array.
        """
        current = leaf_hash.lower().replace("0x", "")
        expected = expected_root.lower().replace("0x", "")
        
        for p in proof:
            sibling = p["hash"].lower().replace("0x", "")
            if current <= sibling:
                combined = bytes.fromhex(current) + bytes.fromhex(sibling)
            else:
                combined = bytes.fromhex(sibling) + bytes.fromhex(current)
            current = hashlib.sha256(combined).hexdigest().lower()
        return current == expected

if __name__ == "__main__":
    test_leaves = [
        hashlib.sha256(f"complaint_{i}_utr_delhi_to_jammu".encode('utf-8')).hexdigest()
        for i in range(10)
    ]
    mt = MerkleTree(test_leaves)
    print("Merkle Root:", "0x" + mt.root)
    proof_0 = mt.get_proof(0)
    print(f"Proof for Leaf 0 (length {len(proof_0)}):", proof_0)
    is_valid = MerkleTree.verify_proof(test_leaves[0], proof_0, mt.root)
    print("Verification result:", is_valid)
