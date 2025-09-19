import os
from bitcoin_wallet import BitcoinWallet
from config import WALLET_FILENAME

def main():
    print("\n=============================================")
    print("           BITCOIN WALLET")
    print("=============================================")
    
    wallet = None
    
    print("\nChoose an action:")
    print("1. I have a wallet (connect to existing)")
    print("2. Create a new wallet")
    
    while True:
        choice = input("\nEnter action number (1 or 2): ").strip()
        
        if choice == "1":
            print("\nEnter your wallet data:")
            address = input("Wallet address: ").strip()
            private_key = input("Private key (WIF): ").strip()
            
            if address and private_key:
                wallet = BitcoinWallet()
                
                if not wallet.validate_address(address):
                    print("Invalid Bitcoin address format!")
                    continue
                
                if not wallet.validate_private_key(private_key):
                    print("Invalid private key format!")
                    continue
                
                wallet.address = address
                wallet.key = private_key
                print(f"\nConnected to wallet: {address}")
                break
                    
            else:
                print("Invalid wallet data!")
                continue
                
        elif choice == "2":
            if os.path.exists(WALLET_FILENAME):
                print(f"\n⚠️  Warning! File {WALLET_FILENAME} already exists!")
                overwrite = input("Overwrite existing wallet? (yes/no): ").strip().lower()
                if overwrite not in ["yes", "y"]:
                    print("Operation cancelled")
                    continue
            
            print(f"\nCreating new wallet...")
            wallet = BitcoinWallet()
            address, private_key = wallet.create_wallet()
            
            if wallet.save_wallet_to_file():
                print(f"Wallet saved to file {WALLET_FILENAME}")
                print(f"Address: {wallet.address}")
                print(f"Network: {'Testnet' if wallet.testnet else 'Mainnet'}")
            else:
                print(f"Error saving wallet to file")
            break
        else:
            print("Invalid choice! Enter 1 or 2")
    
    if wallet is None:
        print("Wallet was not initialized. Exiting program.")
        return
    
    print()
    
    result = wallet.get_all_balances()
    balances = result["balances"]
    errors = result["errors"]
    
    print("Balance:")
    for token, balance in balances.items():
        if token in errors:
            print(f"  {token}: {balance} (Error: {errors[token]})")
        else:
            print(f"  {token}: {balance}")
    
    print("\n=============================================")
    print("Available commands:")
    print("/info - show wallet address")
    print("/balance - show balance")
    print("/send - send cryptocurrency")
    print("=============================================")

    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "/info":
                print(f"\nYour wallet address: {wallet.address}")
                print(f"Network: {'Testnet' if wallet.testnet else 'Mainnet'}")
                
            elif command == "/balance":
                result = wallet.get_all_balances()
                balances = result["balances"]
                errors = result["errors"]
                
                print("\nBalance:")
                for token, balance in balances.items():
                    if token in errors:
                        print(f"  {token}: {balance} (Error: {errors[token]})")
                    else:
                        print(f"  {token}: {balance}")
                    
            elif command == "/send":
                print("\n=== SEND BITCOIN ===")
                
                to_address = input("Enter recipient address: ").strip()
                
                try:
                    amount = float(input("Enter BTC amount to send: ").strip())
                except ValueError:
                    print("Invalid amount")
                    continue
                
                print(f"\nConfirm sending:")
                print(f"Token: BTC")
                print(f"Amount: {amount}")
                print(f"Recipient: {to_address}")
                print(f"Network: {'Testnet' if wallet.testnet else 'Mainnet'}")
                
                confirm = input("Send? (yes/no): ").strip().lower()
                if confirm not in ["yes", "y"]:
                    print("Sending cancelled")
                    continue
                
                print(f"\nSending {amount} BTC...")
                result = wallet.send_token(to_address, amount, "BTC")
                
                if result["success"]:
                    print(f"Sent successfully!")
                    print(f"TXID: {result['txid']}")
                    print(f"Amount: {result['amount']} {result['token']}")
                    print(f"Recipient: {result['to_address']}")
                else:
                    print(f"Sending error: {result['error']}")
                
            else:
                print(f"\nUnknown command: {command}")
                print("Available commands: /info, /balance, /send")
                
        except KeyboardInterrupt:
            print("\n\nExiting wallet...")
            print(f"⚠️  Private key is in file {WALLET_FILENAME}")
            print("⚠️  Keep this file in a safe place!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
