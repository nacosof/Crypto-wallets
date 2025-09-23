from modules.generate_wallet import create_wallet, validate_address, validate_private_key
from modules.get_balance import get_main_coin_balance, get_token_balance, get_all_balances
from modules.send_tokens import send_token
from modules.wallet_storage import save_wallet_to_file, load_wallet_from_file
from config import SUPPORTED_TOKENS, TESTNET, WALLET_FILENAME


class PolygonWallet:
    
    def __init__(self):
        self.address = None
        self.key = None
        self.testnet = TESTNET
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
        
        if token_name not in self.supported_tokens:
            return {"success": False, "error": f"Token {token_name} not supported"}
        
        if token_name == 'MATIC':
            balance_result = self.get_main_coin_balance()
            if balance_result["error"]:
                return {"success": False, "error": f"Cannot check balance: {balance_result['error']}"}
            
            balance = balance_result["balance"]
            if balance < amount:
                return {"success": False, "error": f"Insufficient MATIC. Balance: {balance}, required: {amount}"}
        else:
            token_address = self.supported_tokens[token_name]
            balance_result = self.get_token_balance(token_address)
            if balance_result["error"]:
                return {"success": False, "error": f"Cannot check balance: {balance_result['error']}"}
            
            balance = balance_result["balance"]
            if balance < amount:
                return {"success": False, "error": f"Insufficient {token_name}. Balance: {balance}, required: {amount}"}
        
        return send_token(self.address, self.key, to_address, amount, token_name)
    
    def save_wallet_to_file(self, filename=None):
        if filename is None:
            filename = WALLET_FILENAME
        return save_wallet_to_file(self.address, self.key, filename)
    
    def load_wallet_from_file(self, filename=None):
        if filename is None:
            filename = WALLET_FILENAME
        result = load_wallet_from_file(filename)
        if result["success"]:
            self.address = result["address"]
            self.key = result["private_key"]
        return result["success"]
