import mysql.connector
import inquirer

my_db = mysql.connector.connect(
    user= "root",
    password= "o89h^h7r^Jr*bL1",
    host= "127.0.0.1",
    database= "restaurant_management"
)

cursor = my_db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Wallets(
                wallet_id VARCHAR(32) PRIMARY KEY,
                customer_id VARCHAR(64) NOT NULL,
                balance DECIMAL(10, 2) NOT NULL,
                toatal_bill INT DEFAULT NULL,
                FOREIGN KEY (customer_id) REFRENCES Customers(customer_id)
                )""")

class Currency:
    def __init__(self, name, symbol, exchange_rate):
        self.name = name
        self.symbol = symbol
        self.excange_rate = 1.0

    def convert(self, amount):
        return amount * self.excange_rate
    
class Wallet:
    def __init__(self, currency, balance):
        self.currency = currency
        self.balance = 0.0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        else:
            self.balance -= amount
        
    def check_balance(self):
        return self.balance
    
class User:
    def __init__(self, name, wallet):
        self.name = name
        self.wallet = Wallet(Currency("USD", "$", 1.0), 0.0)

    def deposit(self, amount):
        self.wallet.deposit(amount)

    def withdraw(self, amount):
        self.wallet.withdraw(amount)

    def check_balance(self):
        return self.wallet.check_balance()
    
class PaymentSystem:
    def __init__(self, user):
        self.user = user

    def make_payment(self, amount):
        self.user.withdraw(amount)

def Interface():
    question1 = [
        inquirer.List(
            "pay",
            message = "Would you like to pay for your orders",
            choices= ["Yes", "No"]
        )
    ]

    info1 = inquirer.prompt(question1)

    if info1["pay"] == "Yes":
        question2 = [
            inquirer.Text(
                "amount",
                message= "Please enter the amount you would like to pay"
            )
        ]

        info2 = inquirer.prompt(question2)

        payment = PaymentSystem(User("John Doe", Wallet(Currency("USD", "$", 1.0), 0.0)))


