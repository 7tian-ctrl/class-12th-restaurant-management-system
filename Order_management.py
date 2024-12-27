from menu.order import order_report, menu_category, menu_order_options, fetch_prices
from payment_system.mock_payment_system import payment
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
                    total_bill INT DEFAULT NULL,
                    phone_number TEXT DEFAULT NULL
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

    def update_Custormers(key, name, bill, phone):
        cursor.execute("INSERT INTO Customers(customer_id, Name, total_bill, phone_number) VALUES (%s, %s, %s, %s)", [key, name, bill, phone])
        my_db.commit()

    with open("order.json", "r") as f:
        data = json.load(f)

    records_values = data.values()
    records = list(records_values)[0]
        
    order_list = list(map(lambda i: f"order{i}", range(1, ((len(list(records.keys())) - 4))//2)))

    key = hashlib.sha256(Fernet.generate_key()).hexdigest()

    update_Custormers(key, records["name"], records["Total Bill"], records["phone"])

    order_details = list(records.keys())

    for orders in order_list:

        order_name = records[orders]
        customer_name = records["name"]
        phone_number = records["phone"]

        order_date = datetime.strptime(records["order_date"], "%Y-%m-%d").strftime("%Y-%m-%d")
        order_time = datetime.strptime(records["order_time"], "%H:%M:%S.%f").strftime("%H:%M:%S.%f")

        query = """INSERT INTO Orders(customer_id, order_name, order_date, order_time, order_id, menu_item_id) 
               VALUES (%s, %s, %s, %s, %s, 
               (SELECT menu_item_id FROM Menu WHERE Name = %s))"""

        try:
            cursor.execute(query, [key, order_name, order_date, order_time, hashlib.sha256(Fernet.generate_key()).hexdigest(), order_name])
            my_db.commit()
        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    os.remove("order.json")

    order_proceed = payment()
    if order_proceed == True:
        print("Order placed successfully!")

    else:
        print("Order cancelled!")
        cursor.execute("SELECT customer_id FROM Customers")
        customers = cursor.fetchall()
        for customer in customers:
            cursor.execute("DELETE FROM Orders WHERE customer_id = %s", [customer[0]])
            my_db.commit()

    cursor.close()
    my_db.close()
