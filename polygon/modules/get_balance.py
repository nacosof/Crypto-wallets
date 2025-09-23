from web3 import Web3
from config import TESTNET, MAINNET_RPC, TESTNET_RPC, SUPPORTED_TOKENS


def get_main_coin_balance(address):
    if not address:
        return {"balance": 0, "error": "No wallet address"}
    
    try:
        rpc_url = TESTNET_RPC if TESTNET else MAINNET_RPC
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not web3.is_connected():
            return {"balance": 0, "error": "Cannot connect to Polygon network"}
        
        balance_wei = web3.eth.get_balance(address)
        balance_eth = web3.from_wei(balance_wei, 'ether')
        
        return {"balance": float(balance_eth), "error": None}
    except Exception as e:
        return {"balance": 0, "error": f"API Error: {str(e)}"}


def get_token_balance(address, token_address):
    if not address:
        return {"balance": 0, "error": "No wallet address"}
    
    if not token_address or token_address == 'NONE':
        return get_main_coin_balance(address)
    
    try:
        rpc_url = TESTNET_RPC if TESTNET else MAINNET_RPC
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not web3.is_connected():
            return {"balance": 0, "error": "Cannot connect to Polygon network"}
        
        erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function",
            }
        ]
        
        token_address = Web3.to_checksum_address(token_address)
        
        contract = web3.eth.contract(address=token_address, abi=erc20_abi)
        
        balance_wei = contract.functions.balanceOf(address).call()
        
        decimals = contract.functions.decimals().call()
        
        balance = balance_wei / (10 ** decimals)
        
        return {"balance": float(balance), "error": None}
    except Exception as e:
        return {"balance": 0, "error": f"Token balance error: {str(e)}"}


def get_all_balances(address):
    balances = {}
    errors = {}
    
    matic_result = get_main_coin_balance(address)
    balances["MATIC"] = matic_result["balance"]
    if matic_result["error"]:
        errors["MATIC"] = matic_result["error"]
    
    for token_name, token_address in SUPPORTED_TOKENS.items():
        if token_name == 'MATIC':
            continue
            
        token_result = get_token_balance(address, token_address)
        balances[token_name] = token_result["balance"]
        if token_result["error"]:
            errors[token_name] = token_result["error"]
    
    return {"balances": balances, "errors": errors}