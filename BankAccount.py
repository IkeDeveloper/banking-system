#Bank account management system
class BankAccount:
    interest_rate = 0.01  # Base interest rate

    def __init__(self, account_number, firstname,surname, telephoneno, email, balance=0.0):
        self.account_number = account_number
        self.firstname = firstname
        self.surname = surname
        self.telephoneno = telephoneno
        self.email = email
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount

    def apply_interest(self):
        self.balance += self.balance * BankAccount.interest_rate

    #Check balance and account details
    def __str__(self):
        return f"{self.firstname} ({self.surname}) ({self.telephoneno}) ({self.email}) ({self.account_number}): £{self.balance:.2f}"
    
    
    def transfer_to(self, recipient_account, amount):
        """Transfer money to another account"""
        if amount <= 0:
            raise ValueError("Amount must be positive!")
        
        if amount > self.balance:
            raise ValueError("Insufficient balance!")
        
        if not isinstance(recipient_account, BankAccount):
            raise ValueError("Recipient must be a BankAccount object!")
        
        # Perform transfer
        self.balance -= amount
        recipient_account.balance += amount
        
        # Record transactions for both accounts
        self._record_transaction('Transfer Out', -amount, to=recipient_account.account_number)
        recipient_account._record_transaction('Transfer In', amount, from_acc=self.account_number)
        
        return True
    
    def _record_transaction(self, trans_type, amount, **kwargs):
        """Private method to record transactions"""
        from datetime import datetime
        
        transaction = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': trans_type,
            'amount': amount,
            'balance': self.balance
        }
        
        # Add optional fields (like 'to' or 'from')
        transaction.update(kwargs)
        
        self.transactions.append(transaction)
    
    def mini_statement(self, num_transactions=5):
        """Display mini statement"""
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
        
        recent = self.transactions[-num_transactions:]
        print(f"\nShowing last {len(recent)} transaction(s):\n")
        
        for i, trans in enumerate(recent, 1):
            print(f"{i}. {trans['type']}")
            print(f"   Date: {trans['timestamp']}")
            print(f"   Amount: ${abs(trans['amount']):,.2f}")
            
            if 'to' in trans:
                print(f"   To Account: {trans['to']}")
            if 'from_acc' in trans:
                print(f"   From Account: {trans['from_acc']}")
            
            print(f"   Balance After: ${trans['balance']:,.2f}\n")
        
        print("="*70 + "\n")
    
#Unique account ID generator    
class AccountIDGenerator:
    def __init__(self, prefix="A"):
        self.prefix = prefix
        self.counter = 1

    def next_id(self):
        account_id = f"{self.prefix}{self.counter}"
        self.counter += 1
        return account_id
    
class getuserinfo:
    def get_user_details(self):
        account_number = input("Enter your account number: ")
        if account_number=="-1":
            return "-1","","","",""
        firstname = input("Enter your first name: ")
        surname = input("Enter your surname: ")
        telephoneno = input("Enter your telephone number: ")
        email = input("Enter your email address: ")
        return account_number,firstname, surname, telephoneno, email

# 🏦 Subclass: SavingsAccount
class SavingsAccount(BankAccount):
    interest_rate = 0.03  # Higher interest for savings

    def apply_interest(self):
        self.balance += self.balance * SavingsAccount.interest_rate

    def withdraw(self, amount):
        # Optional: restrict withdrawals or add penalty
        if amount > self.balance:
            print("Insufficient funds for savings withdrawal.")
        else:
            super().withdraw(amount)

class BankingSystemManager:
    def __init__(self):
        pass
    
    bank = BankAccount()
    
    def run(self):
        while True:
            self.display_menu()


    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print(f"{'BANKING SYSTEM':^50}")
        print("="*50)
        print("1. Create Account")
        print("2. Create Savings Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Check Balance")
        print("7. Mini Statement")
        print("8. Save bank accounts to database")
        print("9. Load bank accounts from database")
        print("0. Exit")
        print("="*50)
        self.display_options()
        
    def display_options(self):
        choice = input("Select an option (1-8): ")
        if choice == '1':
            self.createBankAccount()
        elif choice == '2':
            self.createBankAccount()  # You can modify to create SavingsAccount
        elif choice == '3':
            self.deposit_menu()
        elif choice == '4':
            self.withdraw_menu()
        elif choice == '6':
            self.check_balance_menu()
        elif choice == '0':
            print("Exiting the banking system. Goodbye!")
            exit()
        else:
            print("Option not implemented yet. Please choose another option.")
            self.display_menu()
        
    def deposit_menu(self):
        """Deposit interface"""
        print("\n--- DEPOSIT MONEY ---")
        acc_num = input("Enter account number or -1 to exit: ")
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
        
    def check_balance_menu(self):
        """Check balance interface"""
        print("\n--- CHECK BALANCE ---")
        acc_num = input("Enter account number: ")
        account = self.bank(acc_num)                                        # This line is the problem
        
        print(f"\n{'='*70}")
        print(f"Account Number: {account.account_number}")
        print(f"Account Holder: {account.name}")
        print(f"Current Balance: ${account.balance:,.2f}")
        print(f"Total Transactions: {len(account.transactions)}")
        print(f"{'='*70}")
        
    def createBankAccount(self):
        accounts = {}  # Dictionary to hold accounts
        id_gen = AccountIDGenerator() #create an instance of the ID generator

        # Example usage. Put in a class or function as needed.
        while True:
    
            user_input = getuserinfo()

            account_number, firstname, surname, telephoneno, email = user_input.get_user_details()
            
            #accounts[id_gen.next_id()] = SavingsAccount(account_number, firstname, surname, telephoneno, email)


            if (account_number=='-1'):
                print("Exiting account entry.")
                # Print all accounts stored in the dictionary/Store dictionary conent into a sql database.
                for key, acc in accounts.items():
                    print(f"{key}: {acc}")
                return
            
            accounts[id_gen.next_id()] = BankAccount(account_number, firstname, surname, telephoneno, email)
            print(f"Account created successfully! Account Number: {account_number}")
            
       
            
    
                
# Example usage with the BankingSystemManager
if __name__ == "__main__":
    manager = BankingSystemManager()
    manager.run()


# Access and use by usin a dictionary
#accounts["A2"].apply_interest()  # Uses SavingsAccount's higher interest
#print(accounts["A2"])

#accounts["A1"].withdraw(150)
#print(accounts["A1"])
#Now apply interest to the regular account

#accounts["A1"].apply_interest() 
#print(accounts["A1"])

#now deposit into savings account
#accounts["A2"].deposit(500)    
#print(accounts["A2"])  
