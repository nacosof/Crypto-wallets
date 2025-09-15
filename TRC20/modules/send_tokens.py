from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider
from config import TRON_API_KEY, SUPPORTED_TOKENS, USDT_FEE_LIMIT


def validate_recipient_address(address):
    return address.startswith('T') and len(address) == 34


def validate_amount(amount):
    return amount > 0


def send_trx(from_address, private_key, to_address, amount):
    try:
        provider = HTTPProvider(api_key=TRON_API_KEY)
        client = Tron(provider=provider)
        
        txn = (
            client.trx.transfer(from_address, to_address, int(amount * 1_000_000))
            .build()
            .sign(PrivateKey(bytes.fromhex(private_key)))
        )
        
        result = txn.broadcast()
        
        return {
            "success": True,
            "txid": result['txid'],
            "amount": amount,
            "token": "TRX",
            "to_address": to_address
        }
        
    except Exception as e:
        return {"success": False, "error": f"Send error: {str(e)}"}


def send_usdt(from_address, private_key, to_address, amount):
    try:
        provider = HTTPProvider(api_key=TRON_API_KEY)
        client = Tron(provider=provider)
        contract = client.get_contract(SUPPORTED_TOKENS['USDT'])
        
        txn = (
            contract.functions.transfer(to_address, int(amount * 1_000_000))
            .with_owner(from_address)
            .fee_limit(USDT_FEE_LIMIT)
            .build()
            .sign(PrivateKey(bytes.fromhex(private_key)))
        )
        
        result = txn.broadcast()
        
        return {
            "success": True,
            "txid": result['txid'],
            "amount": amount,
            "token": "USDT",
            "to_address": to_address
        }
        
    except Exception as e:
        return {"success": False, "error": f"Send error: {str(e)}"}


def send_token(from_address, private_key, to_address, amount, token_name):
    if not validate_recipient_address(to_address):
        return {"success": False, "error": "Invalid recipient address format"}
    
    if not validate_amount(amount):
        return {"success": False, "error": "Amount must be greater than 0"}
    
    if token_name == 'TRX':
        return send_trx(from_address, private_key, to_address, amount)
    elif token_name == 'USDT':
        return send_usdt(from_address, private_key, to_address, amount)
    else:
        return {"success": False, "error": f"Token {token_name} not supported"}