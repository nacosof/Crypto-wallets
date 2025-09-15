from modules.generate_wallet import create_wallet, validate_address, validate_private_key
from modules.get_balance import get_main_coin_balance, get_token_balance, get_all_balances
from modules.send_tokens import send_token
from modules.wallet_storage import save_wallet_to_file, load_wallet_from_file
from config import SUPPORTED_TOKENS, MIN_TRX_FEE


class TRC20Wallet:
    
    def __init__(self):
        self.address = None
        self.key = None
        self.supported_tokens = SUPPORTED_TOKENS
    
    def create_wallet(self):
        address, private_key = create_wallet()
        self.address = address
        self.key = private_key
        return address, private_key
    
    def validate_address(self, address):
        return validate_address(address)
    
    def validate_private_key(self, private_key):
        return validate_private_key(private_key)
    
    def get_main_coin_balance(self):
        return get_main_coin_balance(self.address)
    
    def get_token_balance(self, token_address):
        return get_token_balance(self.address, token_address)
    
    def get_all_balances(self):
        return get_all_balances(self.address)
    
    def send_token(self, to_address, amount, token_name):
        if not self.address or not self.key:
            return {"success": False, "error": "Wallet not initialized"}
        
        if not validate_address(to_address):
            return {"success": False, "error": "Invalid recipient address format"}
        
        if amount <= 0:
            return {"success": False, "error": "Amount must be greater than 0"}
        
        if token_name == 'TRX':
            balance_result = self.get_main_coin_balance()
            if balance_result["error"]:
                return {"success": False, "error": f"Cannot check balance: {balance_result['error']}"}
            
            balance = balance_result["balance"]
            if balance < amount:
                return {"success": False, "error": f"Insufficient TRX. Balance: {balance}, required: {amount}"}
        
        elif token_name == 'USDT':
            usdt_result = self.get_token_balance(self.supported_tokens['USDT'])
            if usdt_result["error"]:
                return {"success": False, "error": f"Cannot check USDT balance: {usdt_result['error']}"}
            
            usdt_balance = usdt_result["balance"]
            if usdt_balance < amount:
                return {"success": False, "error": f"Insufficient USDT. Balance: {usdt_balance}, required: {amount}"}
            
            trx_result = self.get_main_coin_balance()
            if trx_result["error"]:
                return {"success": False, "error": f"Cannot check TRX balance: {trx_result['error']}"}
            
            trx_balance = trx_result["balance"]
            if trx_balance < MIN_TRX_FEE:
                return {"success": False, "error": f"Insufficient TRX for fees. Balance: {trx_balance}, minimum required: {MIN_TRX_FEE}"}
        
        return send_token(self.address, self.key, to_address, amount, token_name)
    
    def save_wallet_to_file(self, filename=None):
        if filename is None:
            filename = "wallet.txt"
        return save_wallet_to_file(self.address, self.key, filename)
    
    def load_wallet_from_file(self, filename=None):
        if filename is None:
            filename = "wallet.txt"
        result = load_wallet_from_file(filename)
        if result["success"]:
            self.address = result["address"]
            self.key = result["private_key"]
        return result["success"]