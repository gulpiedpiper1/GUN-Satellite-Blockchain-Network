# key_manager.py
import hashlib
from time import time, sleep
from cryptography.fernet import Fernet
from typing import Tuple

from blockchain_core import Blockchain

class KeyManager:
    """Simulates key management for satellites. Generates session keys, writes a hashed record to blockchain,
    and stores the actual key locally for simulation purposes."""
    def __init__(self, blockchain: Blockchain, isl_delay_seconds: float = 0.01):
        self.blockchain = blockchain
        self.session_keys = {}
        self.isl_delay_seconds = isl_delay_seconds  # inter-satellite link propagation / processing delay

    def _generate_aes_key(self) -> bytes:
        return Fernet.generate_key()

    def request_key_transaction(self, sat_A_id: str, sat_B_id: str, expiration_minutes: int = 60) -> dict:
        """Create a key request transaction and put it into the blockchain pending pool.
        The actual (simulated) key is stored locally in session_keys so satellites can receive it in the sim."""
        new_key = self._generate_aes_key()
        key_hash = hashlib.sha256(new_key).hexdigest()

        session_id = tuple(sorted((sat_A_id, sat_B_id)))
        self.session_keys[session_id] = new_key

        transaction = {
            "type": "KEY_REQUEST",
            "session_id": session_id,
            "key_hash": key_hash,
            "expires_at": time() + expiration_minutes * 60,
            "requested_by": sat_A_id,
            "requested_for": sat_B_id,
            "timestamp": time()
        }

        # simulate ISL delay for the key request propagation
        if self.isl_delay_seconds and self.isl_delay_seconds > 0:
            sleep(self.isl_delay_seconds)

        self.blockchain.add_transaction(transaction)
        print(f"[{sat_A_id}<->{sat_B_id}] için anahtar talebi oluşturuldu ve bloğa eklenmek üzere havuza alındı.")
        return transaction

    def get_valid_key_hash_from_chain(self, sat_A_id: str, sat_B_id: str) -> str:
        session_id = tuple(sorted((sat_A_id, sat_B_id)))
        for block in reversed(self.blockchain.chain):
            for tx in reversed(block.transactions):
                # transactions were JSON-serialized; compare safely using default=str
                if str(tx.get("session_id")) == str(session_id):
                    if tx.get("expires_at", 0) > time():
                        return tx["key_hash"]
        return None

    def get_session_key_for_simulation(self, sat_A_id: str, sat_B_id: str) -> bytes:
        session_id = tuple(sorted((sat_A_id, sat_B_id)))
        return self.session_keys.get(session_id)
