# Crypto Wallets

Project for learning how to work with cryptocurrency wallets in different networks.

## What's included

- **TRC20 wallet** - full functionality for TRON network
- **Modular architecture** - clean separation of concerns
- Wallet generation, balance checking, TRX/USDT sending
- Console interface
- Wallet saving to file

## Quick start

1. **Install dependencies:**
   ```bash
   cd TRC20
   pip install -r requirements.txt
   ```

2. **Get API key** from [TronGrid](https://www.trongrid.io/)

3. **Configure `config.py`:**
   - Insert your TronGrid API key into `TRON_API_KEY`
   - Find USDT contract address and insert into `USDT_CONTRACT_ADDRESS`

4. **Run:**
   ```bash
   python main.py
   ```

## How to use

- **Create wallet** - choose option "2"
- **Connect to existing** - choose option "1"
- **Commands:**
  - `/info` - show address
  - `/balance` - show balance
  - `/send` - send cryptocurrency

## Structure

```
TRC20/
├── modules/                    
│   ├── generate_wallet.py     # Wallet generation
│   ├── get_balance.py         # Balance checking
│   ├── send_tokens.py         # Token sending
│   └── wallet_storage.py      # File operations
├── trc20_wallet.py            # Main wallet class
├── main.py                    # Console application
├── config.py                  # Settings
└── requirements.txt           # Dependencies
```

## Important

- **For learning and personal use only** 
- **Keep private keys secure**
- **Test on test networks**

## License

Educational project. Use at your own risk.