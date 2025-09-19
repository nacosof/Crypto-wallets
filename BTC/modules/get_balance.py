from bitcoinlib.services.services import Service
from config import TESTNET


def get_main_coin_balance(address):
    if not address:
        return {"balance": 0, "error": "No wallet address"}
    
    try:
        service = Service(network='testnet' if TESTNET else 'bitcoin')
        balance = service.getbalance(address)
        return {"balance": balance / 100000000, "error": None}
    except Exception as e:
        error_msg = str(e)
        return {"balance": 0, "error": f"API Error: {error_msg}"}


def get_token_balance(address, token_address=None):
    return get_main_coin_balance(address)


def get_all_balances(address):
    balances = {}
    errors = {}
    
    result = get_main_coin_balance(address)
    balances["BTC"] = result["balance"]
    if result["error"]:
        errors["BTC"] = result["error"]
        
    return {"balances": balances, "errors": errors}