from web3 import Web3
from config import TESTNET, MAINNET_RPC, TESTNET_RPC, SUPPORTED_TOKENS, ETHEREUM_CHAIN_ID, GOERLI_CHAIN_ID, DEFAULT_GAS_LIMIT, TOKEN_GAS_LIMIT


def validate_recipient_address(address):
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


def validate_amount(amount):
    return amount > 0


def send_eth(from_address, private_key, to_address, amount):
    try:
        rpc_url = TESTNET_RPC if TESTNET else MAINNET_RPC
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not web3.is_connected():
            return {"success": False, "error": "Cannot connect to Ethereum network"}
        
        from_address = Web3.to_checksum_address(from_address)
        to_address = Web3.to_checksum_address(to_address)
        
        nonce = web3.eth.get_transaction_count(from_address)
        
        gas_price = web3.eth.gas_price
        
        value = web3.to_wei(amount, 'ether')
        
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': value,
            'gas': DEFAULT_GAS_LIMIT,
            'gasPrice': gas_price,
            'chainId': GOERLI_CHAIN_ID if TESTNET else ETHEREUM_CHAIN_ID
        }
        
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return {
            "success": True,
            "txid": web3.to_hex(tx_hash),
            "amount": amount,
            "token": "ETH",
            "to_address": to_address
        }
        
    except Exception as e:
        return {"success": False, "error": f"Send ETH error: {str(e)}"}


def send_erc20_token(from_address, private_key, to_address, amount, token_name, token_address):
    try:
        rpc_url = TESTNET_RPC if TESTNET else MAINNET_RPC
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not web3.is_connected():
            return {"success": False, "error": "Cannot connect to Ethereum network"}
        
        from_address = Web3.to_checksum_address(from_address)
        to_address = Web3.to_checksum_address(to_address)
        token_address = Web3.to_checksum_address(token_address)
        
        erc20_abi = [
            {
                "name": "symbol",
                "outputs": [{"type": "string"}],
                "inputs": [],
                "constant": True,
                "type": "function"
            },
            {
                "name": "decimals",
                "outputs": [{"type": "uint8"}],
                "inputs": [],
                "constant": True,
                "type": "function"
            },
            {
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "success", "type": "bool"}],
                "type": "function"
            }
        ]
        
        contract = web3.eth.contract(address=token_address, abi=erc20_abi)
        
        decimals = contract.functions.decimals().call()
        
        value = int(amount * (10 ** decimals))
        
        nonce = web3.eth.get_transaction_count(from_address)
        
        gas_price = web3.eth.gas_price
        
        tx = contract.functions.transfer(to_address, value).build_transaction({
            'nonce': nonce,
            'gas': TOKEN_GAS_LIMIT,
            'gasPrice': gas_price,
            'chainId': GOERLI_CHAIN_ID if TESTNET else ETHEREUM_CHAIN_ID
        })
        
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return {
            "success": True,
            "txid": web3.to_hex(tx_hash),
            "amount": amount,
            "token": token_name,
            "to_address": to_address
        }
        
    except Exception as e:
        return {"success": False, "error": f"Send {token_name} error: {str(e)}"}


def send_token(from_address, private_key, to_address, amount, token_name):
    if not validate_recipient_address(to_address):
        return {"success": False, "error": "Invalid recipient address format"}
    
    if not validate_amount(amount):
        return {"success": False, "error": "Amount must be greater than 0"}
    
    if token_name not in SUPPORTED_TOKENS:
        return {"success": False, "error": f"Token {token_name} not supported"}
    
    if token_name == 'ETH':
        return send_eth(from_address, private_key, to_address, amount)
    else:
        token_address = SUPPORTED_TOKENS[token_name]
        return send_erc20_token(from_address, private_key, to_address, amount, token_name, token_address)
