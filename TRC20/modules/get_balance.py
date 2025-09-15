from tronpy import Tron
from tronpy.providers import HTTPProvider
from config import TRON_API_KEY, SUPPORTED_TOKENS


def get_main_coin_balance(address):
    if not address:
        return {"balance": 0, "error": "No wallet address"}
    
    try:
        provider = HTTPProvider(api_key=TRON_API_KEY)
        client = Tron(provider=provider)
        account_info = client.get_account(address)
        balance = account_info['balance'] / 1_000_000
        return {"balance": balance, "error": None}
    except Exception as e:
        error_msg = str(e)
        if "account not found" in error_msg.lower():
            return {"balance": 0, "error": "Account not found - wallet needs first transaction"}
        return {"balance": 0, "error": f"API Error: {error_msg}"}


def get_token_balance(address, token_address):
    if not address or token_address == 'NONE':
        return get_main_coin_balance(address)
    
    try:
        provider = HTTPProvider(api_key=TRON_API_KEY)
        client = Tron(provider=provider)
        contract = client.get_contract(token_address)
        balance = contract.functions.balanceOf(address) / 1_000_000
        return {"balance": balance, "error": None}
    except Exception as e:
        error_msg = str(e)
        if "account not found" in error_msg.lower():
            return {"balance": 0, "error": "Account not found - wallet needs first transaction"}
        return {"balance": 0, "error": f"API Error: {error_msg}"}


def get_all_balances(address):
    balances = {}
    errors = {}
    
    for token_name, token_address in SUPPORTED_TOKENS.items():
        result = get_token_balance(address, token_address)
        balances[token_name] = result["balance"]
        if result["error"]:
            errors[token_name] = result["error"]
        
    return {"balances": balances, "errors": errors}