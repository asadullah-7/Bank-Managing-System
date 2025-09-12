import datetime
import os

# ================= FUNCTIONS =================

def clear_screen():
    os.system('cls')
def pin_protected_action(pin, action, *args, **kwargs):
    """
    pin: correct pin
    action: function to execute after correct pin
    *args, **kwargs: arguments for that function
    """
    attempts = 0
    while attempts < 3:
        try:
            user = int(input("Enter your PIN: "))
            if user == pin:
                print("Access Granted!")
                action(*args, **kwargs)   # call function with arguments
                return
            else:
                raise ValueError("PIN is incorrect!")
        except ValueError as e:
            print(e)
            attempts += 1
            print("Please try again...\n")
    print("TOO MANY ATTEMPTS!! ACCESS DENIED")


########################################### TRANSACTION HISTORY CLASS #######################################################
class Transaction_History:
    transaction_counter = 1
    def __init__(self, account_number,trans_type,amount):
        self.transaction_id = Transaction_History.transaction_counter
        Transaction_History.transaction_counter += 1
        self.account_number = account_number
        self.trans_type = trans_type
        self.amount = amount
        self.timestamp = datetime.datetime.now()

    def display_transaction(self):
        print(f"ID: {self.transaction_id} | "
              f"Account: {self.account_number} | "
              f"Type: {self.trans_type} | "
              f"Amount: {self.amount} | "
              f"Time: {self.timestamp.strftime('%d-%b-%Y | %I:%M:%S %p')} ")

########################################### ACCOUNT CLASS #######################################################

class Account:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.transactions =[]


    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount cannot be negative")
        self.balance += amount
        self.transactions.append(Transaction_History(self.account_number, "deposit", amount))

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError('Not enough money!')
        else:
            self.balance -= amount
        self.transactions.append(Transaction_History(self.account_number, "withdraw", amount))

    def get_balance(self):
        return self.balance

    def display_account(self):
        print('Account Number: ', self.account_number)
        print('Account Holder: ', self.account_holder)
        print('Balance: ', self.balance)

    def show_transaction(self):
        print(f"--------- TRANSACTION FOR {self.account_number} ---------")
        for t in self.transactions:
            t.display_transaction()






########################################### CUSTOMER CLASS #######################################################
class Customer:
    customer_counter = 1
    def __init__(self,customer_name, address , phone , gender):
        self.customer_id = f"C{Customer.customer_counter:03d}"
        Customer.customer_counter += 1

        self.customer_name = customer_name
        self.address = address
        self.phone = phone
        self.gender = gender
        self.accounts = []

    def add_account(self,account):
        self.accounts.append(account)

    def display_customer(self):
        print(f"Customer ID: {self.customer_id}    | Name: {self.customer_name}")
        print(f"Address: {self.address}")
        print(f"Phone # {self.phone} | GENDER {self.gender}")
        print(f"Accounts:")
        for acc in self.accounts:
            acc.display_account()
            print("--------------------------------")

############################################## BANK CLASS ####################################################
class Bank:
    account_counter = 1000
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.customers = {}
    # ================================= CUSTOMER METHODS ==============================

    def add_customer(self, customer_name, address, phone, gender):
        new_customer = Customer(customer_name, address, phone, gender)
        self.customers[new_customer.customer_id] = new_customer
        return new_customer

    #================================= ACCOUNTS METHODS ==============================
    def create_account(self, customer_id, balance = 0):
        account_number = f"A{Bank.account_counter}"
        Bank.account_counter += 1
        if customer_id not in self.customers:
            raise  ValueError("Customer ID does not exists")

        customer = self.customers[customer_id]
        new_acc = Account(account_number, customer.customer_name,balance)

        self.accounts[account_number] = new_acc
        customer.add_account(new_acc)
        return new_acc

    def get_account(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            raise ValueError('Account number does not exist')

    def bank_deposit(self, amount,account_number):
        acc = self.get_account(account_number)
        acc.deposit(amount)

    def bank_withdraw(self, amount, account_number):
        acc = self.get_account(account_number)
        acc.withdraw(amount)

    def bank_balance(self, account_number):

        if account_number in self.accounts:
            print(f"Name: {self.accounts[account_number].account_holder}, BALANCE Rs {self.accounts[account_number].get_balance()}")
        else:
            raise ValueError("Account number does not exist")

    def display_transactions(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account number does not exist!")
        acc = self.accounts[account_number]
        acc.show_transaction()

    def transfer(self,from_accNum, to_accNum,amount):
        if from_accNum not in self.accounts or to_accNum not in self.accounts:
            raise ValueError("Account number does not exist")
        else:
            from_acc = self.get_account(from_accNum)
            to_acc = self.get_account(to_accNum)

            from_acc.withdraw(amount)
            to_acc.deposit(amount)

    def delete_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("INVALID ACCOUNT NUMBER!!!")
        acc = self.accounts[account_number]

        customer = None
        for cust in self.customers.values():
            if acc in cust.accounts:
                customer = cust
                break
        if customer:
            customer.accounts.remove(acc)

        del self.accounts[account_number]
        print(f"Account # {account_number} has been deleted successfully!")


    def display_individual(self,customer_id):
        print("=========================================================================================")

        if customer_id in self.customers:
            self.customers[customer_id].display_customer()
            print("=========================================================================================")

    def display_all(self):
        print(f"############### {self.name} ################")
        for acc in self.accounts.values():
            acc.display_account()
            print("_____________________________________________")

    def display_customers(self):
        print(f"############### Customers of {self.name} ################")
        for customer in self.customers.values():
            customer.display_customer()
            print("============================================================================")


########################################### MAIN #######################################################

# MCB = Bank("MCB")
# print ("**************************** WELCOME TO THE BANK MANAGING SYSTEM ************************")
#
# while True:
#     choice = int(input(
#         "1. Make an account\n"
#         "2. Check the balance\n"
#         "3. Deposit\n"
#         "4. Withdraw\n"
#         "5. Transfer money to another account\n"
#         "6. Transaction history\n"
#         "7. Show all Customers:\n"
#         "8. Quit \nCHOICE --> "))
#     clear_screen()
#     if choice == 1:
#         print("-------- ACCOUNT CREATION --------")
#         name = str(input("Enter your name: "))
#         address = str(input("Enter your address: "))
#         phone = str(input("Enter your phone # "))
#         g_num = int(input("Enter your gender\n 1.M\n 2.F \n Press 1/2: "))
#         gender = ''
#
#         if g_num == 1:
#             gender = 'M'
#         else:
#             gender = 'F'
#         new_customer = MCB.add_customer(name,address,phone,gender)
#         while True:
#             try:
#                  balance = int(input("Enter balance of minimum Rs 5000: "))
#                  if balance < 5000:
#                      raise  ValueError("Enter balance of minimum 5000!: ")
#                  break
#             except ValueError as e:
#                  print(e)
#                  print("Please try again....\n")
#         new_acc = MCB.create_account(new_customer.customer_id,balance)
#         new_customer.add_account(new_acc)
#         clear_screen()
#         print("ACCOUNT CREATED SUCCESSFULLY: ")
#         MCB.display_individual(new_customer.customer_id)
#
#
#
#     elif choice == 2:
#         account_number = str(input("Enter the account number: "))
#         try:
#             balance = MCB.bank_balance(account_number)
#
#         except ValueError as e:
#             print("INCORRECT ACCOUNT NUMBER",e)
#
#     elif choice == 3:
#         account_number = str(input("Enter the account number you want to deposit in: "))
#         try:
#             amount = int(input("Enter the amount you want to deposit: "))
#             MCB.bank_deposit(amount,account_number)
#             print(f"Rs.{amount} has been deposited to account # {account_number} successfully")
#         except ValueError as e:
#             print("INCORRECT ACCOUNT NUMBER",e)
#
#     elif choice == 4:
#         account_number = str(input("Enter the account number you want to withdraw from: "))
#         try:
#             amount = int(input("Enter the amount you want to withdraw: "))
#             MCB.bank_withdraw(amount,account_number)
#             print(f"Rs.{amount} has been withdrawn from account # {account_number} successfully")
#         except ValueError as e:
#             print("INCORRECT ACCOUNT NUMBER", e)
#
#     elif choice == 5:
#         sender = str(input("Enter the sender account number: "))
#         reciver = str(input("Enter the reciver account number: "))
#         amount = int(input("Enter the amount to be transfer: "))
#         try:
#             MCB.transfer(sender,reciver,amount)
#             print(f"Rs.{amount} has been transfer from acc # {sender} to acc # {reciver} successfully!")
#         except ValueError as e:
#             print("INCORRECT ACCOUNT NUMBER", e)
#
#     elif choice == 6:
#         print("For check transaction history ENTER THE PIN *******")
#         account_number = str(input("Enter the account number: "))
#         pin_protected_action(123,MCB.display_transactions,account_number)
#
#     elif choice == 7:
#         print("For check all Customers ENTER THE PIN ****** ")
#         pin_protected_action(123, MCB.display_customers)
#
#     elif choice == 8:
#         print("Good bye!\n Exiting....")
#         break

def customer_menu():
    while True:
        print("----------- CUSTOMER HORIZON ------------\n"
              "1. Check balance\n"
              "2. Deposit\n"
              "3. Withdraw\n"
              "4. Transfer to another account\n"
              "5. Transaction history\n"
              "6. Create new account\n"
              "7. Find account by CNIC\n"
              "8. Logout\n")
        try:
            choice = int(input("CHOICE -> "))
        except ValueError:
            print("PLEASE ENTER VALID OPTION !!!")
            continue
        clear_screen()
        if choice == 1:
            print("Check balance logic...")
        elif choice == 2:
            print("Deposit logic...")
        elif choice == 3:
            print("Withdraw logic...")
        elif choice == 4:
            print("transfer money logic...")
        elif choice == 5:
            print("transaction history logic...")
        elif choice == 6:
            print("create account logic...")
        elif choice == 7:
            print("find account logic...")
        elif choice == 8:
            print("RETURNING TO MAIN MENU")
            return  #  Back to MAIN MENU
        else:
            print("INVALID CHOICE!")

def admin_menu():
    while True:
        print("----------- ADMIN HORIZON ------------\n"
              "1. Create new customer\n"
              "2. Create new account of existing customer\n"
              "3. View all customers\n"
              "4. View all accounts\n"
              "5. Delete an account\n"
              "6. Find customer by CNIC\n"
              "7. Logout\n")
        try:
            choice = int(input("CHOICE -> "))
        except ValueError:
            print("PLEASE ENTER VALID OPTION!")
            continue
        clear_screen()
        if choice == 1:
            print("Create new customer logic...")
        elif choice == 2:
            print("Create new account logic...")
        elif choice == 3:
            print("View all customer logic...")
        elif choice == 4:
            print("View all accounts logic...")
        elif choice == 5:
            print("delete an account logic...")
        elif choice == 6:
            print("find customer by CNIC logic...")
        elif choice == 7:
            print("RETURNING TO MAIN MENU")
            return  # Back to MAIN MENU
        else:
            print("INVALID CHOICE!")




print("=============================== WELCOME TO BANKING SOFTWARE =================================")
while True:
    print("---------- MAIN MENU ----------")
    print("1. Login as Customer\n"
          "2. Login as Admin\n"
          "3. Exit")
    choice = str(input("CHOICE -> "))
    clear_screen()
    if choice == '1':
        # CUSTOMER HORIZON
        customer_menu()
    elif choice == '2':
        # ADMIN HORIZON
        admin_menu()
    elif choice == '3':
        print("------------ GOOD BYE -----------\n"
              "EXITING........")
        break
    else:
        print("PLEASE ENTER VALID OPTION")


