from tronpy.keys import PrivateKey


def create_wallet():
    key = PrivateKey.random()
    address = key.public_key.to_base58check_address()
    private_key = key.hex()
    return address, private_key


def validate_address(address):
    return address.startswith('T') and len(address) == 34


def validate_private_key(private_key):
    return len(private_key) == 64 and all(c in '0123456789abcdef' for c in private_key.lower())