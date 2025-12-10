from datetime import datetime

class BankAccount:
    """Represents a bank account with full transaction recording"""
    
    def __init__(self, account_number, name, initial_balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = initial_balance
        self.transactions = []
        # Record the account opening transaction
        self._record_transaction('Account Opening', initial_balance)
    
    def deposit(self, amount):
        """Deposit money and record transaction"""
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        
        self.balance += amount
        self._record_transaction('Deposit', amount)
    
    def withdraw(self, amount):
        """Withdraw money and record transaction"""
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        if amount > self.balance:
            raise ValueError("Insufficient balance!")
        
        self.balance -= amount
        self._record_transaction('Withdrawal', -amount)
    
    def transfer_to(self, recipient, amount):
        """Transfer money to another account and record for both accounts"""
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        if amount > self.balance:
            raise ValueError("Insufficient balance!")
        if self.account_number == recipient.account_number:
            raise ValueError("Cannot transfer to same account!")
        
        # Update balances
        self.balance -= amount
        recipient.balance += amount
        
        # Record transaction for sender (this account)
        self._record_transaction('Transfer Out', -amount, to=recipient.account_number)
        
        # Record transaction for recipient
        recipient._record_transaction('Transfer In', amount, from_acc=self.account_number)
    
    def _record_transaction(self, trans_type, amount, **kwargs):
        """Private method to record all transactions"""
        transaction = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': trans_type,
            'amount': amount,
            'balance': self.balance
        }
        # Add any additional info (like 'to' or 'from_acc')
        transaction.update(kwargs)
        self.transactions.append(transaction)
    
    def mini_statement(self, num=5):
        """Display mini statement showing recent transactions"""
        if not self.transactions:
            print("\nNo transactions found!")
            return
        
        print("\n" + "="*70)
        print(f"{'MINI STATEMENT':^70}")
        print("="*70)
        print(f"Account Number: {self.account_number}")
        print(f"Account Holder: {self.name}")
        print(f"Current Balance: ${self.balance:,.2f}")
        print("="*70)
        
        recent = self.transactions[-num:]
        print(f"\nShowing last {len(recent)} transaction(s):\n")
        
        for i, trans in enumerate(recent, 1):
            print(f"{i}. {trans['type']}")
            print(f"   Date: {trans['timestamp']}")
            print(f"   Amount: ${abs(trans['amount']):,.2f}")
            
            # Show transfer details if available
            if 'to' in trans:
                print(f"   To Account: {trans['to']}")
            if 'from_acc' in trans:
                print(f"   From Account: {trans['from_acc']}")
            
            print(f"   Balance After: ${trans['balance']:,.2f}\n")
        
        print("="*70 + "\n")
    
    def get_all_transactions(self):
        """Return all transactions"""
        return self.transactions
    
    def __str__(self):
        return f"BankAccount({self.account_number}, {self.name}, ${self.balance:.2f})"


class Bank:
    """Manages all bank accounts"""
    
    def __init__(self, name):
        self.name = name
        self.accounts = {}
    
    def create_account(self, acc_num, name, initial_balance):
        """Create new account"""
        if acc_num in self.accounts:
            raise ValueError("Account already exists!")
        
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative!")
        
        account = BankAccount(acc_num, name, initial_balance)
        self.accounts[acc_num] = account
        return account
    
    def get_account(self, acc_num):
        """Get account by number"""
        if acc_num not in self.accounts:
            raise ValueError("Account not found!")
        return self.accounts[acc_num]
    
    def account_exists(self, acc_num):
        """Check if account exists"""
        return acc_num in self.accounts
    
    def transfer(self, from_num, to_num, amount):
        """
        Transfer money between accounts
        This calls transfer_to which handles transaction recording
        """
        if from_num == to_num:
            raise ValueError("Cannot transfer to the same account!")
        
        from_account = self.get_account(from_num)
        to_account = self.get_account(to_num)
        
        # The transfer_to method handles all transaction recording
        from_account.transfer_to(to_account, amount)
    
    def list_all_accounts(self):
        """List all accounts"""
        if not self.accounts:
            print("\nNo accounts in the bank.")
            return
        
        print(f"\n{'='*70}")
        print(f"ALL ACCOUNTS IN {self.name.upper()}")
        print(f"{'='*70}")
        print(f"{'Account':<15} {'Holder':<25} {'Balance':>15}")
        print("-"*70)
        
        for acc_num, account in self.accounts.items():
            print(f"{acc_num:<15} {account.name:<25} ${account.balance:>14,.2f}")
        
        print(f"{'='*70}\n")


class BankingSystem:
    """User interface / Controller"""
    
    def __init__(self):
        self.bank = Bank("Python Bank")
    
    def run(self):
        """Main application loop"""
        print(f"\n{'='*70}")
        print(f"WELCOME TO {self.bank.name.upper()}")
        print(f"{'='*70}")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            try:
                if choice == '1':
                    self.create_account_menu()
                elif choice == '2':
                    self.deposit_menu()
                elif choice == '3':
                    self.withdraw_menu()
                elif choice == '4':
                    self.transfer_menu()
                elif choice == '5':
                    self.check_balance_menu()
                elif choice == '6':
                    self.mini_statement_menu()
                elif choice == '7':
                    self.bank.list_all_accounts()
                elif choice == '8':
                    print(f"\n{'='*70}")
                    print(f"Thank you for banking with {self.bank.name}!")
                    print(f"{'='*70}\n")
                    break
                else:
                    print("\n✗ Invalid choice! Please enter 1-8.")
            
            except ValueError as e:
                print(f"\n✗ Error: {e}")
            except Exception as e:
                print(f"\n✗ Unexpected error: {e}")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print(f"{self.bank.name.upper() + ' - MAIN MENU':^70}")
        print("="*70)
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Check Balance")
        print("6. Mini Statement")
        print("7. List All Accounts")
        print("8. Exit")
        print("="*70)
    
    def create_account_menu(self):
        """Create account interface"""
        print("\n--- CREATE NEW ACCOUNT ---")
        name = input("Enter account holder name: ")
        acc_num = input("Enter account number: ")
        initial = float(input("Enter initial deposit: $"))
        
        # Bank.create_account will create the BankAccount object
        # BankAccount.__init__ will record the opening transaction
        account = self.bank.create_account(acc_num, name, initial)
        
        print(f"\n✓ Account created successfully!")
        print(f"Account Number: {acc_num}")
        print(f"Holder: {name}")
        print(f"Initial Balance: ${initial:.2f}")
        print(f"Transaction recorded: Account Opening")
    
    def deposit_menu(self):
        """Deposit interface"""
        print("\n--- DEPOSIT MONEY ---")
        acc_num = input("Enter account number: ")
        amount = float(input("Enter amount to deposit: $"))
        
        # get_account returns the BankAccount object
        # deposit() method records the transaction
        account = self.bank.get_account(acc_num)
        account.deposit(amount)
        
        print(f"\n✓ Deposit successful!")
        print(f"New balance: ${account.balance:.2f}")
        print(f"Transaction recorded: Deposit of ${amount:.2f}")
    
    def withdraw_menu(self):
        """Withdraw interface"""
        print("\n--- WITHDRAW MONEY ---")
        acc_num = input("Enter account number: ")
        amount = float(input("Enter amount to withdraw: $"))
        
        # withdraw() method records the transaction
        account = self.bank.get_account(acc_num)
        account.withdraw(amount)
        
        print(f"\n✓ Withdrawal successful!")
        print(f"New balance: ${account.balance:.2f}")
        print(f"Transaction recorded: Withdrawal of ${amount:.2f}")
    
    def transfer_menu(self):
        """Transfer interface"""
        print("\n--- TRANSFER MONEY ---")
        from_num = input("Enter your account number: ")
        to_num = input("Enter recipient account number: ")
        amount = float(input("Enter amount to transfer: $"))
        
        # bank.transfer() calls transfer_to() which records transactions
        # for BOTH sender and recipient
        self.bank.transfer(from_num, to_num, amount)
        
        from_account = self.bank.get_account(from_num)
        to_account = self.bank.get_account(to_num)
        
        print(f"\n✓ Transfer successful!")
        print(f"Transferred ${amount:.2f} to {to_account.name} ({to_num})")
        print(f"Your new balance: ${from_account.balance:.2f}")
        print(f"Transactions recorded for both accounts")
    
    def check_balance_menu(self):
        """Check balance interface"""
        print("\n--- CHECK BALANCE ---")
        acc_num = input("Enter account number: ")
        account = self.bank.get_account(acc_num)
        
        print(f"\n{'='*70}")
        print(f"Account Number: {account.account_number}")
        print(f"Account Holder: {account.name}")
        print(f"Current Balance: ${account.balance:,.2f}")
        print(f"Total Transactions: {len(account.transactions)}")
        print(f"{'='*70}")
    
    def mini_statement_menu(self):
        """Mini statement interface"""
        print("\n--- MINI STATEMENT ---")
        acc_num = input("Enter account number: ")
        
        account = self.bank.get_account(acc_num)
        
        # Ask how many transactions to show
        try:
            num = int(input(f"How many recent transactions? (1-{len(account.transactions)}): "))
            if num < 1:
                num = 5
            account.mini_statement(num)
        except ValueError:
            # Default to 5 if invalid input
            account.mini_statement(5)


# Run the application
if __name__ == "__main__":
    # Create and run the banking system
    app = BankingSystem()
    app.run()