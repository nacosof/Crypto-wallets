from bitcoinlib.services.services import Service
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Key
from config import TESTNET


def validate_recipient_address(address):
    try:
        if address.startswith(('1', '3', 'bc1', 'm', '2', 'tb1')):
            return len(address) >= 26 and len(address) <= 62
        return False
    except:
        return False


def validate_amount(amount):
    return amount > 0


def send_btc(from_address, private_key, to_address, amount):
    try:
        service = Service(network='testnet' if TESTNET else 'bitcoin')
        
        tx = Transaction(network='testnet' if TESTNET else 'bitcoin')
        tx.add_input(from_address, amount)
        tx.add_output(to_address, amount)
        
        key = Key.from_wif(private_key)
        tx.sign(key)
        
        txid = service.sendrawtransaction(tx.raw_hex())
        
        return {
            "success": True,
            "txid": txid,
            "amount": amount,
            "token": "BTC",
            "to_address": to_address
        }
        
    except Exception as e:
        return {"success": False, "error": f"Send error: {str(e)}"}


def send_token(from_address, private_key, to_address, amount, token_name):
    if not validate_recipient_address(to_address):
        return {"success": False, "error": "Invalid recipient address format"}
    
    if not validate_amount(amount):
        return {"success": False, "error": "Amount must be greater than 0"}
    
    if token_name == 'BTC':
        return send_btc(from_address, private_key, to_address, amount)
    else:
        return {"success": False, "error": f"Token {token_name} not supported"}