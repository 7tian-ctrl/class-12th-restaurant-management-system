from menu.order import order_report, menu_category, menu_order_options, fetch_prices
import mysql.connector
from cryptography.fernet import Fernet
import json
import inquirer
from datetime import datetime
import os
import hashlib

def order_management():
    order_log = {}
    session_storage = []
    copy_log = {}

    result = order_report()
    copy_log = dict(result)

    session_storage.append(dict(copy_log))

    question = [
        inquirer.Confirm(
            "confirmation",
            message="Do you want to place a new order"
        )
    ]

    confirmation = inquirer.prompt(question)

    while confirmation["confirmation"] != False:

        result = order_report()
        copy_log = dict(result)

        session_storage.append(copy_log)

        confirmation = inquirer.prompt(question)


    order_log = {f"'{Fernet.generate_key().hex()}'": d for i, d in enumerate(session_storage)}

    with open("order.json", "a") as f:
        json.dump(order_log, f, indent=4)

    my_db = mysql.connector.connect(
        user="root",
        host="127.0.0.1",
        password="o89h^h7r^Jr*bL1",
        database="restaurant_management"
    )

    cursor = my_db.cursor()


    cursor.execute("""CREATE TABLE IF NOT EXISTS Customers(
                    customer_id VARCHAR(64) PRIMARY KEY,
                    Name VARCHAR(255) NOT NULL,
                    total_bill INT DEFAULT NULL
                    )""")


    cursor.execute("""CREATE TABLE IF NOT EXISTS Orders(
                    order_id VARCHAR(64) PRIMARY KEY,
                    menu_item_id INT DEFAULT NULL,
                    customer_id VARCHAR(64) DEFAULT NULL,
                    order_name VARCHAR(255) DEFAULT NULL,
                    order_date DATE DEFAULT NULL,
                    order_time TIME DEFAULT NULL,
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                    FOREIGN KEY (menu_item_id) REFERENCES Menu(menu_item_id)
                    )""")

    def update_Custormers(name, bill):
        cursor.execute("INSERT INTO Customers(customer_id, Name, total_bill) VALUES (%s, %s, %s)", [hashlib.sha256(Fernet.generate_key()).hexdigest(), name, bill])
        my_db.commit()

    with open("order.json", "r") as f:
        data = json.load(f)

    for records in data.values():
        order_list = list(map(lambda i: f"order{i}", range(1, ((len(list(records.keys())) - 3))//2)))

        update_Custormers(records["name"], records["Total Bill"])

        for order_details in list(records.keys()):

            for orders in order_list:
                order_name = records[orders]
                customer_name = records["name"]

                order_date = datetime.strptime(records["order_date"], "%Y-%m-%d")

                order_time = datetime.strptime(records["order_time"], "%H:%M:%S.%f")

                query = """INSERT INTO Orders (customer_id, order_name, order_date, order_time, order_id, menu_item_id) 
                           VALUES ((SELECT customer_id FROM Customers WHERE Name = %s), %s, %s, %s, %s, 
                                   (SELECT menu_item_id FROM Menu WHERE Name = %s))"""
            
                cursor.execute(query, [customer_name, order_name, order_date, order_time, hashlib.sha256(Fernet.generate_key()).hexdigest(), order_name])

                my_db.commit()

            order_list = []


    os.remove("order.json")

    cursor.close()
    my_db.close()

order_management()