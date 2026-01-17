# blockchain_core.py
import hashlib
import json
from time import time, sleep
from datetime import datetime
from typing import List, Any, Iterable

class Block:
    """Represents a block in the blockchain."""
    def __init__(self, index: int, transactions: List[Any], previous_hash: str, validator_id: str):
        self.index = index
        self.timestamp = time()
        self.transactions = list(transactions)  # store a copy
        self.previous_hash = previous_hash
        self.validator_id = validator_id
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Return SHA-256 hash of the block contents. Transactions are serialized with default=str to be JSON-safe."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "validator_id": self.validator_id
        }, sort_keys=True, default=str).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self) -> str:
        readable_time = datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        tx_json = json.dumps(self.transactions, indent=2, default=str)
        return (f"Block #{self.index} | Time: {readable_time} | Validator: {self.validator_id}\n"
                f"  Hash: {self.hash}\n"
                f"  Prev. Hash: {self.previous_hash}\n"
                f"  Transactions: {tx_json}")


class Blockchain:
    """Simple PoA blockchain for simulation. Provides optional PoA delay to mimic validator signing time."""
    def __init__(self, validators: Iterable[str], poa_delay_seconds: float = 0.02):
        self.chain: List[Block] = []
        self.pending_transactions: List[dict] = []
        self.validators = set(validators)
        self.poa_delay_seconds = poa_delay_seconds
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], previous_hash="0", validator_id="System")
        self.chain.append(genesis_block)

    @property
    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: dict) -> int:
        """Add a transaction to the pending pool and return the index of the block it will be included in."""
        self.pending_transactions.append(transaction)
        return self.get_last_block.index + 1

    def add_block(self, validator_id: str):
        """Create a block from pending transactions and append it to the chain if validator is authorized.
        Simulates a PoA signing delay (self.poa_delay_seconds)."""
        if validator_id not in self.validators:
            print(f"HATA: {validator_id} yetkili bir doğrulayıcı değil.")
            return None

        if not self.pending_transactions:
            print("Uyarı: Eklenecek bekleyen işlem yok.")
            return None

        # simulate PoA signing delay
        if self.poa_delay_seconds and self.poa_delay_seconds > 0:
            sleep(self.poa_delay_seconds)

        last_block = self.get_last_block
        # copy pending txs into the block to avoid later mutation
        transactions_for_block = list(self.pending_transactions)

        new_block = Block(
            index=last_block.index + 1,
            transactions=transactions_for_block,
            previous_hash=last_block.hash,
            validator_id=validator_id
        )

        # clear pending txs after they have been included
        self.pending_transactions = []
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

