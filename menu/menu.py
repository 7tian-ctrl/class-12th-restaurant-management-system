import mysql.connector
import json

my_db = mysql.connector.connect(
    user="root",
    password="",
    host="127.0.0.1",
    database="restaurant_management"
)

cursor = my_db.cursor()

query = """CREATE TABLE IF NOT EXISTS Menu(
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    Category VARCHAR(255),
    Name VARCHAR(255),
    Description VARCHAR(255),
    Price INT
)"""

try:
    cursor.execute(query)
    print("Table created successfully")
except mysql.connector.Error as err:
    print("Error creating table: {}".format(err))

key_mover = 0

query = "INSERT INTO Menu (Category, Name, Description, Price) VALUES (%s, %s, %s, %s)"
try:
    with open("menu/menu.json", "r") as f:
        data = json.load(f)
    for heading in data:
        if heading == "restaurant":
            continue
        else:
            for item in data[heading]:
                keys = list(data[heading].keys())
                if item != "Ordinary & Happy":
                    for dishes in data[heading][item]:

                        cursor.execute(query, (keys[key_mover],dishes["name"], dishes["description"], dishes["Price"]))

                key_mover += 1
    
    my_db.commit()
    print("Data inserted successfully")
except mysql.connector.Error as err:
    print("Error inserting data: {}".format(err))

query = "SELECT * FROM Menu"
try:
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        print("Results:")
        for row in result:
            print(row)
    else:
        print("No results found")
except mysql.connector.Error as err:
    print("Error retrieving data: {}".format(err))


cursor.close()
my_db.close()
