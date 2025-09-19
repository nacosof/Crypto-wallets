import os
from config import WALLET_FILENAME


def save_wallet_to_file(address, private_key, filename=WALLET_FILENAME):
    if not address or not private_key:
        return False
    
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=== BITCOIN WALLET ===\n\n")
            f.write(f"Wallet address: {address}\n")
            f.write(f"Private key: {private_key}\n\n")
            f.write("⚠️  WARNING: NEVER SHARE OR SHOW YOUR PRIVATE KEY TO ANYONE!\n")
            f.write("⚠️  Keep this file in a safe place!\n")
            f.write("⚠️  Private key gives full access to the wallet!\n")
        
        return True
    except Exception:
        return False


def load_wallet_from_file(filename=WALLET_FILENAME):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, filename)
        
        if not os.path.exists(file_path):
            return {"address": None, "private_key": None, "success": False}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        address = None
        private_key = None
            
        for line in lines:
            if line.startswith("Wallet address:"):
                address = line.split(":")[1].strip()
            elif line.startswith("Private key:"):
                private_key = line.split(":")[1].strip()
        
        return {
            "address": address,
            "private_key": private_key,
            "success": address and private_key
        }
    except Exception:
        return {"address": None, "private_key": None, "success": False}
