# Crypto Wallets

Project for learning how to work with cryptocurrency wallets in different networks.

## What's included

- **TRC20 wallet** - full functionality for TRON network (TRX/USDT)
- **Bitcoin wallet** - full functionality for Bitcoin network
- **Modular architecture** - clean separation of concerns
- Wallet generation, balance checking, cryptocurrency sending
- Console interface
- Wallet saving to file

## Installation & Setup

### TRC20 (TRON) - detailed instructions:

1. **Install dependencies:**
   ```bash
   cd TRC20
   pip install -r requirements.txt
   ```

2. **Get API key:**
   - Register at [TronGrid](https://www.trongrid.io/)
   - Get free API key

3. **Configure `config.py`:**
   ```python
   TRON_API_KEY = 'your_trongrid_api_key'
   
   SUPPORTED_TOKENS = {
       'TRX': 'NONE',  
       'USDT': 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t',  # USDT contract
   }
   ```

4. **Network switching:**
   - For **testnet**: use Nile testnet API
   - For **mainnet**: use main TronGrid API

5. **Run:**
   ```bash
   python main.py
   ```

### Other networks (Bitcoin, Ethereum, etc.):

**Same installation process:**
```bash
cd [NETWORK_FOLDER]
pip install -r requirements.txt
# Configure config.py if needed
python main.py
```

**Each network has its own specific config settings - check `config.py` in each folder.**

## Usage

1. **Create wallet** - choose option "2"
2. **Connect existing** - choose option "1"
3. **Commands:**
   - `/info` - show wallet address
   - `/balance` - show balance
   - `/send` - send cryptocurrency

## Project Structure

```
Crypto-wallets/
├── TRC20/                     # TRON wallet
│   ├── modules/
│   │   ├── generate_wallet.py # Wallet generation
│   │   ├── get_balance.py     # Balance checking
│   │   ├── send_tokens.py     # Token sending
│   │   └── wallet_storage.py  # File operations
│   ├── trc20_wallet.py        # Main wallet class
│   ├── main.py               # Console application
│   ├── config.py             # Settings
│   └── requirements.txt      # Dependencies
├── BTC/                      # Bitcoin wallet (same structure)
├── .gitignore
└── README.md
```

## Security

⚠️ **IMPORTANT:**
- **For learning and personal use only**
- **Keep private keys secure**
- **Test on testnet first**
- **Never share private keys**

## License

Educational project. Use at your own risk.