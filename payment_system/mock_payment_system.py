import mysql.connector
import inquirer
import random
import os
import hashlib
from cryptography.fernet import Fernet
import pickle

def payment():
    my_db = mysql.connector.connect(
        user = "root",
        host = "127.0.0.1",
        password = "",
        database = "restaurant_management"
    )

    cursor = my_db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Wallets(
                    wallet_id VARCHAR(64) PRIMARY KEY,
                    customer_id VARCHAR(64) NOT NULL,
                    balance SMALLINT NOT NULL,
                    total_bill INT DEFAULT NULL,
                    paid BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
                    )""")

    class Currency:
        def __init__(self, name, symbol, exchange_rate):
            self.name = name
            self.symbol = symbol
            self.excange_rate = 1.0

        def convert(self, amount):
            return amount * self.excange_rate
    
    class Wallet:
        def __init__(self, currency, balance, broke):
            self.currency = currency
            self.balance = balance
            self.broke = broke

        def deposit(self, amount):
            self.balance += amount

        def withdraw(self, amount):
            if amount > self.balance:
                self.broke = True
                raise ValueError("Insufficient balance")
            else:
                self.balance -= amount
        
        def check_balance(self):
            return self.balance
    
    class User:
        def __init__(self, name, wallet, initial_balance):
            self.name = name
            self.wallet = Wallet(Currency("USD", "$", 1.0), initial_balance, False)

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
            
    cursor.execute("SELECT Name, customer_id, total_bill FROM Customers")

    info = cursor.fetchall()
    customer_info = info[-1]

    customer_name = customer_info[0]
    customer_id = customer_info[1]

    total_bill = customer_info[2]

    user_object = User(customer_name, Wallet(Currency("USD", "$", 1.0), random.randint(30, 100), False), random.randint(30, 100))
    user = [user_object.name, user_object.wallet.check_balance(), total_bill]


    with open("store\\wallet.dat", "ab") as w:
        user_info = {
            "name": user_object.name,
            "customer_id": customer_id,
            "balance": user_object.wallet.check_balance(),
            "total_bill": total_bill
        }

        key = Fernet.generate_key()
        cipher = Fernet(key)
        serialiser = pickle.Pickler(w)

        encrypted_data = cipher.encrypt(pickle.dumps(user_info))

        serialiser.dump(encrypted_data)

    question1 = [
        inquirer.List(
            "pay",
            message = "Would you like to pay for your orders",
            choices= ["Yes", "No"]
        )
    ]

    info1 = inquirer.prompt(question1)

    if info1["pay"] == "Yes": 
        user_object.withdraw(user[2])
        if user_object.wallet.broke == True:
            print("Insufficient balance, your order will not be proceed")
        else:
            cursor.execute("INSERT INTO Wallets(wallet_id, customer_id, balance, total_bill, paid) VALUES (%s, %s, %s, %s, %s)", [hashlib.sha256(Fernet.generate_key()).hexdigest(), customer_id, user[1], user[2], True])

            my_db.commit()

    else:
        print("Your order will not proceed")
        os._exit(0)

    cursor.execute("SELECT paid FROM Wallets")

    info = cursor.fetchall()

    for paid in info:
        last_paid = paid[0]

    cursor.close()
    my_db.close()

    return last_paid
