########################################### ACCOUNT CLASS #######################################################

class Account:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount cannot be negative")
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError('Not enough money!')
        else:
            self.balance -= amount

    def get_balance(self):
        return self.balance

    def display_Account(self):
        print('Account Number: ', self.account_number)
        print('Account Holder: ', self.account_holder)
        print('Balance: ', self.balance)

############################################## BANK CLASS ####################################################
class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, account_number, account_holder, balance = 0):
        if account_number not in self.accounts:
            new__acc = Account(account_number, account_holder, balance)
            self.accounts[account_number] = new__acc

        else:
            raise ValueError('Account number already exists')

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
            return self.accounts[account_number].get_balance()
        else:
            raise ValueError("Account number does not exist")

    def transfer(self,from_accNum, to_accNum,amount):
        if from_accNum not in self.accounts or to_accNum not in self.accounts:
            raise ValueError("Account number does not exist")
        else:
            from_acc = self.get_account(from_accNum)
            to_acc = self.get_account(to_accNum)
            from_acc.withdraw(amount)
            to_acc.deposit(amount)

    def display_all(self):
        print(f"############### {self.name} ################")
        for acc in self.accounts.values():
            acc.display_Account()
            print("_____________________________________________")

########################################### MAIN #######################################################

# main
MCB = Bank('MCB')
HBL = Bank("HBL")

MCB.create_account('111', 'Asad', 100000)
MCB.create_account('222', 'Ahmad', 100000)
HBL.create_account('333', 'Khubaib', 100000)

MCB.display_all()
HBL.display_all()
