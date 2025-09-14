import datetime
import os
import json


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
            user = str(input("\nEnter your PIN: "))
            if user == pin:
                clear_screen()
                print("\nAccess Granted!")
                action(*args, **kwargs)   # call function with arguments
                return
            else:
                raise ValueError("\nPIN is incorrect!\n")
        except ValueError as e:
            print(e)
            attempts += 1
            print("\nPlease try again...\n")
    print("\n                      TOO MANY ATTEMPTS!! ACCESS DENIED\n ")

def confirmation (user_choice):
    if user_choice == 1:
        return True
    elif user_choice == 2:
        return False
    else:
        print("\n\n INVALID CHOICE !!\n")
        return False


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
        if not self.transactions:
            print("No Transactions found for this account yet.")
            return
        print(f"--------- TRANSACTION FOR {self.account_number} ---------")
        for t in self.transactions:
            t.display_transaction()






########################################### CUSTOMER CLASS #######################################################
class Customer:
    customer_counter = 1
    def __init__(self,customer_name, cnic, address , phone , gender):
        self.customer_id = f"C{Customer.customer_counter:03d}"
        Customer.customer_counter += 1

        self.customer_name = customer_name
        self.cnic = cnic
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


############################################## BANK CLASS ####################################################
class Bank:
    account_counter = 1000
    DATA_FILE = "bank_data.json"

    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.customers = {}
        self.load_data()
    # ================================= CUSTOMER METHODS ==============================

    def add_customer(self, customer_name,cnic, address, phone, gender):
        # handeling duplication in cnic:
        for cust in self.customers.values():
            if cust.cnic == cnic:
                raise ValueError("CNIC already exist! Cannot create duplicate customer.")
        new_customer = Customer(customer_name,cnic, address, phone, gender)
        self.customers[new_customer.customer_id] = new_customer
        return new_customer

    def customer_id_match(self,customer_id):
        return customer_id in self.customers

    def get_name(self,customer_id):
        for cust in self.customers.values():
            if cust.customer_id == customer_id:
                return cust.customer_name

    def find_customer_by_cnic(self, cnic):
        for cust in self.customers.values():
            if cust.cnic == cnic:
                title = "Mr." if cust.gender == "M" else "Miss."
                clear_screen()
                print(f"Customer, {title}{cust.customer_name} found successfully....\n"
                      f"------------ CUSTOMER DETAILS ----------\n"
                      f"Customer ID: {cust.customer_id}\n"
                      f"Name: {cust.customer_name} | Gender: {cust.gender}\n"
                      f"Address: {cust.address}\n"
                      f"Contact # {cust.phone}\n")


                if cust.accounts:
                    print(f"--------------- ACCOUNTS DETAILS ----------------\n")
                    for acc in cust.accounts:
                        print(f"  -> Account Number: {acc.account_number}\n"
                              f"Balance: {acc.get_balance()}\n"
                              f"-----------------------------------------------------------")
                else:
                    print("\nTHIS CUSTOMER HAS NO ACCOUNTS YET.\n")

                return cust  # customer mil gaya, return kar do

        print("\nCNIC NOT FOUND!!!!!\n")
        return None

    def check_if_cnic_exist(self,cnic):
        for cust in self.customers.values():
            if cust.cnic == cnic:
                return True
        return False

    def customer_id_by_cnic(self,cnic):
        for cust in self.customers.values():
            if cust.cnic == cnic:
                return cust.customer_id
        return None

    def delete_customer(self,customer_id):
        if customer_id not in self.customers:
            raise ValueError("INVALID CUSTOMER ID!!")
        customer_to_delete = self.customers[customer_id]

        for acc in list(customer_to_delete.accounts):
            if acc.account_number in self.accounts:
                del self.accounts[acc.account_number]

        del self.customers[customer_id]


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
            print(f"\nName: {self.accounts[account_number].account_holder}, BALANCE Rs {self.accounts[account_number].get_balance()}\n")
            return self.accounts[account_number].get_balance()
        else:
            raise ValueError("Account number does not exist")

    def display_transactions(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account number does not exist!")
        acc = self.accounts[account_number]
        acc.show_transaction()


    def transfer(self, from_accNum, to_accNum, amount):
        if from_accNum not in self.accounts or to_accNum not in self.accounts:
            print("\nOne of the account numbers does not exist!\n")
            return

        from_acc = self.get_account(from_accNum)
        to_acc = self.get_account(to_accNum)

        try:
            from_acc.withdraw(amount)  # yaha exception aa sakta hai
            to_acc.deposit(amount)
            print(f"\nRs.{amount} transferred successfully from {from_accNum} to {to_accNum}\n")
        except ValueError as e:
            print(f"\nTransfer failed: {e}\n")

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

    def match_account_number(self,account_number):
        for acc in self.accounts.values():
           if account_number == acc.account_number:
             return True
        return False






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


    ################################### FILE HANDLING METHODS ############################################

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as f:
                data = json.load(f)

                # Reset first
                self.customers = {}
                self.accounts = {}

                # Restore Customers
                for cust_id, cust_data in data.get("customers", {}).items():
                    customer = Customer(
                        cust_data["customer_name"],
                        cust_data["cnic"],
                        cust_data["address"],
                        cust_data["phone"],
                        cust_data["gender"]
                    )
                    customer.customer_id = cust_id
                    self.customers[cust_id] = customer

                # Restore Accounts
                for acc_num, acc_data in data.get("accounts", {}).items():
                    account = Account(
                        acc_num,
                        acc_data["account_holder"],
                        acc_data["balance"]
                    )

                    # Restore transactions
                    for t in acc_data.get("transactions", []):
                        tr = Transaction_History(
                            account_number=acc_num,
                            trans_type=t["trans_type"],
                            amount=t["amount"]
                        )
                        tr.transaction_id = t["transaction_id"]
                        tr.timestamp = datetime.datetime.fromisoformat(t["timestamp"])
                        account.transactions.append(tr)

                        # transaction counter update
                        Transaction_History.transaction_counter = max(
                            Transaction_History.transaction_counter, tr.transaction_id + 1
                        )

                    self.accounts[acc_num] = account

                    # Link with customer
                    cust_id = acc_data["customer_id"]
                    if cust_id in self.customers:
                        self.customers[cust_id].add_account(account)

                # Update account counter
                Bank.account_counter = data.get("account_counter", Bank.account_counter)

                # Update customer counter
                if self.customers:
                    last_cust_num = max(int(cid[1:]) for cid in self.customers.keys())
                    Customer.customer_counter = last_cust_num + 1

        except (FileNotFoundError, json.JSONDecodeError):
            # First time run
            self.customers = {}
            self.accounts = {}

    def save_data(self):
        data = {
            "customers": {
                cust_id: {
                    "customer_name": cust.customer_name,
                    "cnic": cust.cnic,
                    "address": cust.address,
                    "phone": cust.phone,
                    "gender": cust.gender,
                    "accounts": [acc.account_number for acc in cust.accounts]
                }
                for cust_id, cust in self.customers.items()
            },
            "accounts": {
                acc_num: {
                    "account_holder": acc.account_holder,
                    "balance": acc.get_balance(),
                    "customer_id": cust_id,
                    "transactions": [
                        {
                            "transaction_id": t.transaction_id,
                            "account_number": t.account_number,
                            "trans_type": t.trans_type,
                            "amount": t.amount,
                            "timestamp": t.timestamp.isoformat()
                        }
                        for t in acc.transactions
                    ]
                }
                for cust_id, cust in self.customers.items()
                for acc in cust.accounts
                for acc_num, a in self.accounts.items() if a == acc
            },
            "account_counter": Bank.account_counter
        }

        with open(self.DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)


########################################### MAIN #######################################################

MCB = Bank("MCB")
MCB.load_data()


def customer_menu(acc_number):

    while True:
        print("----------- CUSTOMER HORIZON ------------\n"
              "1. Check balance\n"
              "2. Deposit\n"
              "3. Withdraw\n"
              "4. Transfer to another account\n"
              "5. Transaction history\n"
              "6. Logout\n")
        try:
            choice = int(input("CHOICE -> "))

        except ValueError:
            print("\nPLEASE ENTER VALID OPTION !!!\n")
            continue
        clear_screen()
        if choice == 1:
            # FOR CHECK BALANCE


            MCB.bank_balance(acc_number)
        elif choice == 2:
            # FOR DEPOSIT
            amount = int(input("\nEnter the amount you want to deposit: "))
            MCB.bank_deposit(amount,acc_number)
            print(f"\nRs.{amount} has been deposited to account # {acc_number} successfully\n")
        elif choice == 3:
            # FOR WITHDRAW
            if MCB.bank_balance(acc_number) == 0:
                print("\nACCOUNT IS EMPTY!! Rs.0.00\n")
                continue

            amount = int(input("\nEnter the amount you want to withdraw: "))
            if amount > MCB.bank_balance(acc_number):
                print("\nBALANCE IS LESS THAN YOUR ENTERED AMOUNT!!\n")
                continue
            elif amount == 0:
                print("\nPLEASE ENTER SOME AMOUNT\n")
                continue
            clear_screen()
            confir = int(input("\nARE YOU SURE TO WITHDRAW MONEY? \nPRESS 1 OR 2\n \n1. YES\n2. NO\n CHOICE -> "))
            if confirmation(confir):
                MCB.bank_withdraw(amount,acc_number)
                print(f"\nRs.{amount} has been withdrawn from account # {acc_number} successfully\n")
            else:
                continue
        elif choice == 4:
            # FOR TRANSFER
            reciver = str(input("\nEnter the account number you want to transfer in: "))
            if MCB.match_account_number(reciver):
                if acc_number == reciver:
                    print("\nERROR: YOU TRYING TO TRANSFER MONEY IN SAME ACCOUNT!!\n")
                    continue
                else:
                    amount = int(input("\nEnter the amount to be transfer: \n"))
                    if amount <= 0:
                        print("\nYOUR ENTERED AMOUNT IS INVALID!!\n")
                        continue
                    elif amount > MCB.bank_balance(acc_number):
                        print("\nYOUR ENTERED AMOUNT IS MORE THAN YOUR BALANCE!!")
                        continue
                    else:
                        try:
                            MCB.transfer(acc_number, reciver, amount)
                            print(f"\nRs.{amount} has been transfer from acc # {acc_number} to acc # {reciver} successfully!\n")
                        except ValueError as e:
                            print(f"\nTRANSFER FAILED: {e}\n")

            else:
                print("\nACCOUNT NUMBER NOT FOUND!!\n")

        elif choice == 5:
            # FOR TRANSACTION HISTORY
            MCB.display_transactions(acc_number)

        elif choice == 6:
            # FOR RETURNING TO MAIN MENU
            print("\nRETURNING TO MAIN MENU\n")
            return  #  Back to MAIN MENU
        else:
            print("\nINVALID CHOICE!\n")
#########################################################################################################################
def admin_menu():
    while True:
        print("----------- ADMIN HORIZON ------------\n"
              "1. Create new customer\n"
              "2. Create new account of existing customer\n"
              "3. View all customers\n"
              "4. View all accounts\n"
              "5. Delete an account\n"
              "6. Delete a customer\n"
              "7. Find customer by CNIC\n"
              "8. Logout\n")
        try:
            choice = int(input("CHOICE -> "))
        except ValueError:
            print("\nPLEASE ENTER VALID OPTION!\n")
            continue
        clear_screen()
        if choice == 1:
            # CREATE NEW CUSTOMER
            print("\n-------- CUSTOMER CREATION --------")
            name = str(input("\nEnter your name: "))
            cnic = str(input("Enter your CNIC # "))
            if MCB.check_if_cnic_exist(cnic):
                print("\n\nCNIC Exist !!\n\n")
                continue

            else:
                address = str(input("Enter your address: "))
                phone = str(input("Enter your phone # "))
                g_num = int(input("Enter your gender\n 1.M\n 2.F \n Press 1/2: "))
                gender = ''

                if g_num == 1:
                    gender = 'M'
                else:
                    gender = 'F'
                new_customer = MCB.add_customer(name, cnic, address, phone, gender)
                default_account = MCB.create_account(new_customer.customer_id, 0)
                print(f"\nCUSTOMER AND DEFAULT ACCOUNT CREATED SUCCESSFULLY\n"
                      f"YOUR CUSTOMER ID IS: {new_customer.customer_id}\n"
                      f"YOUR ACCOUNT NUMBER IS: {default_account.account_number}\n")

        elif choice == 2:
            # CREATE NEW ACCOUNT
            cnic = str(input("\nEnter your cninc: "))
            if MCB.check_if_cnic_exist(cnic):
                confir = int(input("\nYou already have an account did you want to make another? \n1. YES\n2. NO\n CHOICE -> "))
                if confirmation(confir):
                    customer_id = MCB.customer_id_by_cnic(cnic)
                    new_account = MCB.create_account(customer_id, 0)
                    print(f'\nYOUR ACCOUNT HAS BEEN CREATED SUCCESSFULLY!!\n'
                          f'NEW ACCOUNT NUMBER IS: {new_account.account_number}\n')
                else:
                    continue
            else:
                clear_screen()
                print("\nERROR!! CUSTOMER IS NOT REGISTERED!! \n")
                continue

        elif choice == 3:
            # VIEW ALL CUSTOMER
            MCB.display_customers()
        elif choice == 4:
            # VIEW ALL ACCOUNTS
            MCB.display_all()

        elif choice == 5:
            # DELETE AN ACCOUNT
            account_number = str(input("\nEnter the account number you want to delete: "))
            confir = int(input("\nDID YOU WANT TO DELETE YOUR ACCOUNT PERMANENTLY?\n1.YES\n2. NO \nCHOICE -> "))
            if confirmation(confir):
                MCB.delete_account(account_number)
                print("\nACCOUNT DELETED SUCCESSFULLY!\n")
            else:
                continue


        elif choice == 6:
            # DELETE A CUSTOMER
            choice = str(input("\nEnter customer ID to delete customer, PRESS f IN CASE OF FORGET\nCUSTOMER ID -> "))
            if choice.lower() == 'f':
                cnic = str(input("Enter your CNIC: "))
                customer_id = MCB.customer_id_by_cnic(cnic)
                if not customer_id:
                    print("\nNO CUSTOMER FOUND WITH THIS CNIC!\n")
                    continue
            else:
                customer_id = choice

            if MCB.customer_id_match(customer_id):
                name = MCB.get_name(customer_id)
                confir = int(input(f"\nDO YOU WANT TO DELETE \"{name}\'s Account\" PERMANENTLY? \n1. YES\n2. NO\nCHOICE -> "))
                if confirmation(confir):
                    MCB.delete_customer(customer_id)
                    print("\nCUSTOMER DELETED SUCCESSFULLY!!")
                else:
                    continue
            else:
                print("\nINVALID CUSTOMER ID!!\n")
                continue

        elif choice == 7:
            # FIND CUSTOMER BY CNIC
            cnic = str(input("\nTO FIND YOUR ACCOUNT NUMBER ENTER YOUR CNIC (without dashes) : "))
            MCB.find_customer_by_cnic(cnic)
        elif choice == 8:
            # RETURNING TO THE MAIN MENU
            print("\nRETURNING TO MAIN MENU\n")
            return  # Back to MAIN MENU
        else:
            print("\nINVALID CHOICE!\n")




print("=============================== WELCOME TO BANKING SOFTWARE =================================")
while True:
    print("---------- MAIN MENU ----------")
    print("1. Login as Customer\n"
          "2. Login as Admin\n"
          "3. Exit"
          "ENTER IN NUMBERS e.g 1,2,3")
    choice = str(input("\n   CHOICE -> "))
    input("\nPress Enter to continue...")
    clear_screen()

    if choice == '1':
        # CUSTOMER HORIZON
        acc_number = str(input("\nEnter your account NUMBER or press f if you forget: "))
        if acc_number.lower() == 'f':
            cnic = str(input("\nTO FIND YOUR ACCOUNT NUMBER ENTER YOUR CNIC (without dashes) : "))
            MCB.find_customer_by_cnic(cnic)
        else:
            if MCB.match_account_number(acc_number):
                customer_menu(acc_number)
            else:
                print("\n\n!!NOT FOUND!!\n\n")

    elif choice == '2':
        # ADMIN HORIZON
        pin_protected_action("123",admin_menu)
    elif choice == '3':
        print("\n\n------------ GOOD BYE -----------\n"
              "EXITING........")
        MCB.save_data()
        print("Data has been save in file!\n\n")
        break
    else:
        print("\n\n  !!PLEASE ENTER VALID OPTION!! \n\n")


