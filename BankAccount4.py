#Bank account management system
class BankAccount:
    interest_rate = 0.01  # Base interest rate
    

    def __init__(self, account_number, firstname,surname, telephoneno, email, balance=0.0, address=None):
        self.account_number = account_number
        self.firstname = firstname
        self.surname = surname
        self.telephoneno = telephoneno
        self.email = email
        self.balance = balance
        self.address = address  # Instance of CustAdress or None
        self.transactions = []  # List to store transaction history

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._record_transaction('Deposit', amount)

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._record_transaction('Withdraw', -amount)
            
    
            
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
        transaction.update(kwargs) #Update the transaction dictionary with any additional keyword arguments
                                    #Update is a method of dictionaries that adds key-value pairs from another dictionary
        self.transactions.append(transaction) #Append is a built in method for lists that adds an item to the end of the list
        
        """Return all transactions"""
    def get_all_transactions(self): #This can be called  by wa view transactions method on the menu
        return self.transactions
    
   
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
        
class CustAddress:
    def __init__(self, street_number, street_name, city, postcode, country):
        self.street_number = street_number
        self.street_name = street_name
        self.city = city
        self.postcode = postcode
        self.country = country

    def __str__(self):
        return f"{self.street_number}, {self.street_name}, {self.city} {self.postcode}, {self.country}"  
    
    
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


#Unique account ID generator    
class AccountIDGenerator:
    def __init__(self, prefix="A"):
        self.prefix = prefix
        self.counter = 1

    def next_id(self):
        account_id = f"{self.prefix}{self.counter}"
        self.counter += 1
        return account_id
    
#Gets user input
class getuserinfo:
    def get_user_details(self):
        account_number = input("Enter your account number or -1 to return to main menu: ")
        if account_number=="-1":
            return "-1","","","","","","","","",""
        firstname = input("Enter your first name: ")
        surname = input("Enter your surname: ")
        telephoneno = input("Enter your telephone number: ")
        email = input("Enter your email address: ")
        #Now add address inputs here.
        
        street_number = input("Enter your street number: ")
        street_name = input("Enter your street name: ")         
        city = input("Enter your city: ")
        postcode = input("Enter your postcode: ")
        country = input("Enter your country: ") 
        
        return account_number,firstname, surname, telephoneno, email, street_number, street_name, city, postcode, country

class BankingSystemManager:
    def __init__(self):
        self.accounts = {} #Dedfines thwe dictionary that will hold the bank accounts
        self.id_gen = AccountIDGenerator() #create an instance of the ID generator
    
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
        print("6. Check Balance and accountt details")
        print("7. Mini Statement")
        print("8. Print out all accounts records")
        print("9. Load bank accounts from database")
        print("P. Print out address book of all accounts.")
        print("S. Save bank accounts to database")
        print("D. Delete an account" )
        print("E. Erase all accounts.")
        print("0. Exit")
        print("="*50)
        self.display_options()
        
    def display_options(self):
        choice = input("Select an option: ")
        if choice == '1':
            self.createBankAccount()
            
        elif choice == '2':
            self.createSavingsAccount()  # You can modify to create SavingsAccount
            
        elif choice == '3':
            self.deposit_menu()
            
        elif choice == '4':
            self.withdraw_menu()
            
        elif choice == '5':
            self.transfer_menu()
        elif choice == '6':
            self.check_balance_menu()
            
        elif choice == '7':
            self.ministatement_menu()
        elif choice == '8':
            self.printallaccounts()
        elif choice == 'p' or choice == 'P':
            self.printaddressbook()
        
        elif choice =='D' or choice =='d':
            self.deleterecord()
            
        elif choice == "E" or choice == 'e':
            self.eraseaccounts()
            
        elif choice == '0':
            print("Exiting the banking system. Goodbye!")
            exit()
        else:
            print("Option not implemented yet. Please choose another option.")
            self.display_menu()
        
    def deposit_menu(self):
        """Deposit interface"""
        print("\n--- DEPOSIT MONEY ---")
        acc_num = (input("Enter account number: ")).strip().upper()
        amount = float(input("Enter amount to deposit: $"))
        
        for account in self.accounts.values():
            if account.account_number == acc_num:
                account.deposit(amount)
                print(f"\n✓ Deposit successful!")
                print(f"New balance: £{account.balance:.2f}")
                break
        else:
            print(f"✗ No account found with account number '{acc_num}'.")

    def withdraw_menu(self):                                
        """Withdraw interface"""
        print("\n--- WITHDRAW MONEY ---")
        acc_num = input("Enter account number: ").strip().upper()
        amount = float(input("Enter amount to withdraw: $"))
        
        for account in self.accounts.values():
            if account.account_number == acc_num:
                account.withdraw(amount)
                print(f"\n✓ withdraw successful!")
                print(f"New balance: £{account.balance:.2f}")
                break
        else:
            print(f"✗ No account found with account number '{acc_num}'.")
            
    def printallaccounts(self):
        """Print all accounts"""
        print("\n--- ALL BANK ACCOUNTS ---")
        if not self.accounts:
            print("No accounts found.")
            return
        
        for acc_num, account in self.accounts.items():
            print(f"{acc_num}: {account}")
            
    def printaddressbook(self):
        """Print all account addresses"""
        print("\n--- ADDRESS BOOK ---")
        for acc_num, account in self.accounts.items():
            
            print(f"{account.firstname} {account.surname} {account.address}")
           # print(f"First Name: {account.firstname} Surname: {account.surname}")
            
           # print(str(self.address))
            
         
    def transfer_menu(self):
        """Transfer money interface"""
        print("\n--- TRANSFER MONEY ---")
        from_acc_num = input("Enter your account number: ").strip().upper()
        to_acc_num = input("Enter recipient's account number: ").strip().upper()
        amount = float(input("Enter amount to transfer: $"))
        
       # from_account = None
       # to_account = None
    
        
        for account in self.accounts.values():
            if account.account_number == from_acc_num:
                from_account = account
            if account.account_number == to_acc_num:
                to_account = account
        
        if not from_account:
            print(f"✗ No account found with account number '{from_acc_num}'.")
            return
        if not to_account:
            print(f"✗ No account found with account number '{to_acc_num}'.")
            return
        
        try:
            from_account.transfer_to(to_account, amount)
            print(f"\n✓ Transfer successful!")
            print(f"Your new balance: £{from_account.balance:.2f}")
        except ValueError as e:
            print(f"✗ Transfer failed: {e}")
        
    def ministatement_menu(self):
        """Mini statement interface"""
        print("\n--- MINI STATEMENT ---")
        acc_num = input("Enter account number: ")
        
        print(f"Total accounts loaded: {len(self.accounts)}")


        for account in self.accounts.values():
            print(f"Checking: {account.account_number}")


            if account.account_number == acc_num:
                print(f"New balance: £{account.balance:.2f}")
                print(f"\n{'='*70}")
                print(f"Account Number: {account.account_number}")
                print(f"Account Holder: {account.firstname} {account.surname}")
                print(f"Current Balance: ${account.balance:,.2f}")
                print(f"Total Transactions: {len(account.transactions)}")
                print(f"{'='*70}")
                #Display mini statement by calling get_all_transactions methdod perhaps?
                transactions = account.get_all_transactions()
                if not transactions:
                    print("No transactions found for this account.")
                    return

                print(f"\nTransaction history for account {acc_num}:")
                for tx in transactions:
                    print(f"{tx['timestamp']} | {tx['type']} | £{tx['amount']:.2f} | Balance: £{tx['balance']:.2f}", end="")
                    if 'to' in tx:
                        print(f" → To: {tx['to']}", end="")
                    if 'from_acc' in tx:
                        print(f" ← From: {tx['from_acc']}", end="")
                    print()


                break  # Optional: stop after finding the match
    
    
    #Erase all accounts
    def eraseaccounts(self):
        confirm = input("Are you sure you want to delete ALL accounts? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.accounts.clear()
            print("✓ All accounts have been deleted.")
        else:
            print("✗ Operation cancelled.")


    #Delete individual record.       
    def deleterecord(self):
        acc_num = input("Enter the account number to delete: ").strip().upper()
        for key, account in list(self.accounts.items()): # We need to loop through self.accounts.items  to get both the key and the account object:
            if account.account_number8==acc_num:
                del self.accounts[key]
                print(f"Account {acc_num} deleted")
                return
        print("No account found with account number. ")
        
        
    def check_balance_menu(self):
        """Check balance and account details interface"""
        print("\n--- CHECK BALANCE AND ACCOUNT DETAILS ---")
        acc_num = input("Enter account number: ").strip().upper()
        
        for account in self.accounts.values():
            if account.account_number == acc_num:
                print(f"\nAccount Details:\n{account}")
                break
        else:
            print(f"✗ No account found with account number '{acc_num}'.")
    
    
    def createBankAccount(self): #Creates a bank accountg
       
        
        # Example usage. Put in a class or function as needed.
        while True:
            
            user_input = getuserinfo()

            account_number, firstname, surname, telephoneno, email, street_number, street_name,city,postcode,country = user_input.get_user_details()
            


            if (account_number=='-1'):
                print("Exiting account entry.")
                break
                
            self.accounts[self.id_gen.next_id()] = BankAccount(account_number, firstname, surname, telephoneno, email, address=CustAddress(street_number, street_name, city, postcode, country))

           
    def createSavingsAccount(self): #Creates a savings bank account
        self.id_gen = AccountIDGenerator("B")
        while True:
            
            user_input = getuserinfo()
            

            account_number, firstname, surname, telephoneno, email, street_number, street_name,city,postcode,country = user_input.get_user_details()
            
            
            if (account_number=='-1'):
                print("Exiting account entry.")
                break
                
            new_id = self.id_gen.next_id()
            self.accounts[new_id] = SavingsAccount(account_number, firstname, surname, telephoneno, email, address=CustAddress(street_number, street_name, city, postcode, country))

           # self.address = CustAddress(street_number, street_name, city, postcode, country)
           # print(str(self.address))
        
        
                     
# Example usage with the BankingSystemManager
if __name__ == "__main__":
    manager = BankingSystemManager()
    manager.run()



