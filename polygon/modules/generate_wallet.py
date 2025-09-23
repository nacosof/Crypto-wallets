import time
from web3 import Web3
from config import TESTNET, MAINNET_RPC, TESTNET_RPC


def create_wallet():
    try:
        rpc_url = TESTNET_RPC if TESTNET else MAINNET_RPC
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        account = web3.eth.account.create()
        
        address = account.address
        private_key = account.key.hex()
        
        return address, private_key
    except Exception as e:
        raise Exception(f"Failed to create wallet: {str(e)}")


def validate_address(address):
    try:
        if not address or not isinstance(address, str):
            return False
        
        if not address.startswith('0x'):
            return False
        
        if len(address) != 42:
            return False
        
        Web3.to_checksum_address(address)
        return True
    except:
        return False


def validate_private_key(private_key):
    try:
        if not private_key or not isinstance(private_key, str):
            return False
        
        if private_key.startswith('0x'):
            private_key = private_key[2:]
        
        if len(private_key) != 64:
            return False
        
        account = Web3().eth.account.from_key(private_key)
        return account is not None
    except:
        return False
