# simulation.py
import hashlib
import argparse
import sys
from time import sleep, time
from cryptography.fernet import Fernet
import networkx as nx
import matplotlib.pyplot as plt

from blockchain_core import Blockchain
from key_manager import KeyManager

class Satellite:
    def __init__(self, satellite_id: str, blockchain: Blockchain, key_manager: KeyManager):
        self.id = satellite_id
        self.blockchain = blockchain
        self.key_manager = key_manager
        self.secure_key_storage = {}

    def receive_key(self, session_id, key):
        print(f"[{self.id}] {session_id} için oturum anahtarını aldı ve güvenli deposuna kaydetti.")
        self.secure_key_storage[session_id] = key

    def encrypt_message(self, target_id: str, message: str):
        session_id = tuple(sorted((self.id, target_id)))
        key = self.secure_key_storage.get(session_id)
        if not key:
            print(f"HATA [{self.id}]: {target_id} ile iletişim için şifreleme anahtarı bulunamadı.")
            return None
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        print(f"\n[{self.id} -> {target_id}] Mesaj şifrelendi: {encrypted_message.decode()[:30]}...")
        return encrypted_message

    def decrypt_message(self, source_id: str, encrypted_message: bytes):
        print(f"[{self.id}] {source_id} uydusundan şifreli mesaj alındı. Deşifrelemeden önce anahtar doğrulanıyor...")
        session_id = tuple(sorted((self.id, source_id)))
        local_key = self.secure_key_storage.get(session_id)
        if not local_key:
            return f"HATA [{self.id}]: Bu oturum için yerel anahtarım yok."

        local_key_hash = hashlib.sha256(local_key).hexdigest()
        valid_hash_on_chain = self.key_manager.get_valid_key_hash_from_chain(self.id, source_id)

        print(f"  - Yerel Anahtarın Hash'i: {local_key_hash[:15]}...")
        print(f"  - Zincirdeki Geçerli Hash: {valid_hash_on_chain[:15] if valid_hash_on_chain else 'Bulunamadı'}...")

        if local_key_hash == valid_hash_on_chain:
            print("  - DOĞRULAMA BAŞARILI: Anahtar, blockchain kaydı ile uyumlu.")
            f = Fernet(local_key)
            decrypted_message = f.decrypt(encrypted_message).decode()
            return f"BAŞARILI: Deşifre Edilen Mesaj: '{decrypted_message}'"
        else:
            return "HATA: DOĞRULAMA BAŞARISIZ! Anahtar geçersiz veya güncel değil. Mesaj deşifre edilmeyecek."

def visualize_network(blockchain: Blockchain, satellites: list, show_plot: bool = True, save_path: str = None):
    """Simple network visualization using networkx and matplotlib.
    Nodes are satellites, edges represent key requests between satellites found in the blockchain.
    Each block's transactions are inspected and edges added accordingly.
    """
    G = nx.Graph()
    # add satellite nodes
    for s in satellites:
        G.add_node(s.id)

    # add edges from transactions in the chain
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.get('type') == 'KEY_REQUEST':
                sess = tx.get('session_id')
                # make sure we handle different possible serializations
                if isinstance(sess, (list, tuple)) and len(sess) == 2:
                    a, b = sess[0], sess[1]
                else:
                    # try to parse string repr like "('SAT-A', 'SAT-B')"
                    try:
                        s = str(sess).strip("() ").replace("'", "")
                        parts = [p.strip() for p in s.split(',') if p.strip()]
                        a, b = parts[0], parts[1]
                    except Exception:
                        continue
                G.add_edge(a, b)

    plt.figure(figsize=(7,5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    if save_path:
        plt.savefig(save_path)
        print(f"Ağ görselleştirmesi kaydedildi: {save_path}")
    if show_plot:
        plt.show()
    plt.close()

def run_interactive():
    print("--- GÜVENLİ UZAY AĞI (GÜN) SİMÜLASYONU (Gelişmiş) ---")
    VALIDATOR_SATELLITES = {'SAT-C', 'SAT-D', 'SAT-E'}
    gun_blockchain = Blockchain(validators=VALIDATOR_SATELLITES, poa_delay_seconds=0.02)
    gun_key_manager = KeyManager(blockchain=gun_blockchain, isl_delay_seconds=0.01)

    sat_a = Satellite('SAT-A', gun_blockchain, gun_key_manager)
    sat_b = Satellite('SAT-B', gun_blockchain, gun_key_manager)
    sat_c = Satellite('SAT-C', gun_blockchain, gun_key_manager)
    satellites = [sat_a, sat_b, sat_c]

    while True:
        print('\nSeçenekler:\n 1. Anahtar talep et (SAT-A -> SAT-B)\n 2. Blok oluştur (SAT-C doğrulayıcı)\n 3. Mesaj gönder (SAT-A -> SAT-B)\n 4. Ağı görselleştir\n 5. Zincir geçerliliğini kontrol et\n 6. Çıkış')
        choice = input('Seçiminiz (1-6): ').strip()
        if choice == '1':
            gun_key_manager.request_key_transaction('SAT-A', 'SAT-B')
        elif choice == '2':
            new_block = gun_blockchain.add_block('SAT-C')
            if new_block:
                print('Yeni blok oluşturuldu:')
                print(new_block)
        elif choice == '3':
            session_id = tuple(sorted(('SAT-A', 'SAT-B')))
            session_key = gun_key_manager.get_session_key_for_simulation('SAT-A', 'SAT-B')
            if not session_key:
                print('HATA: Oturum anahtarı yok. Önce anahtar talep edip blok ekleyin.')
                continue
            sat_a.receive_key(session_id, session_key)
            sat_b.receive_key(session_id, session_key)
            secret_message = input('Gönderilecek gizli mesajı yazın: ').strip()
            encrypted = sat_a.encrypt_message('SAT-B', secret_message)
            if encrypted:
                result = sat_b.decrypt_message('SAT-A', encrypted)
                print(result)
        elif choice == '4':
            visualize_network(gun_blockchain, satellites, show_plot=True)
        elif choice == '5':
            print('Zincir geçerliliği:', gun_blockchain.is_chain_valid())
        elif choice == '6':
            print('Çıkılıyor...')
            break
        else:
            print('Geçersiz seçim. Tekrar deneyin.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GÜN Simülasyonu - CLI')
    parser.add_argument('--nogui', action='store_true', help='Görselleştirmeyi göstermeden çalıştır (headless)')
    args = parser.parse_args()

    try:
        run_interactive()
    except KeyboardInterrupt:
        print('\nKullanıcı tarafından durduruldu. Çıkılıyor...')
        sys.exit(0)
