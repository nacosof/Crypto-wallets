import time
import bitcoinlib
from bitcoinlib.keys import Key
from config import TESTNET


def create_wallet():
    bit_wallet_name = f"MyWallet_{int(time.time())}"
    wallet = bitcoinlib.wallets.Wallet.create(bit_wallet_name, network='testnet' if TESTNET else 'bitcoin')
    bit_key = wallet.get_key()
    address = bit_key.address
    private_key = bit_key.wif
    return address, private_key


def validate_address(address):
    try:
        if address.startswith(('1', '3', 'bc1', 'm', '2', 'tb1')):
            return len(address) >= 26 and len(address) <= 62
        return False
    except:
        return False


def validate_private_key(private_key):
    try:
        key = Key.from_wif(private_key)
        return key is not None
    except:
        return False