import json
from pyfiglet import Figlet
import inquirer
import datetime

result = {}
report = {}
dish_list = []

def fetch_prices(result):
     total_bill = 0.0
     with open("menu/menu.json", "r") as f:
          menu = json.load(f)
     
     for heading in menu:

          for item in menu[heading]:

               if menu[heading][item] == "Ordinary & Happy":
                    continue

               else:
                    for dishes in menu[heading][item]:
                    
                         for order in result.values():
                              if order == dishes['name']:
                                   total_bill += dishes['Price']
                              else:
                                   continue


     return total_bill
                    

def heading_display(text):
     return Figlet(font='larry3d').renderText(text)

def result_update(dict):
     return result.update(dict)

def menu_category():
     menu_categories = []

     with open('menu/menu.json', 'r') as f:
          menu = json.load(f)

     for heading in menu:

          for item in menu[heading]:

               menu_categories = list(menu[heading].keys())
     
     return menu_categories

 
def menu_order_options(menu_categories= menu_category()): 
     menu_items = {}
     add_on = 0
     once = 0

     with open('menu/menu.json', 'r') as f:
          menu = json.load(f)

     for heading in menu:

          for item in menu[heading]:

               if menu[heading][item] == "Ordinary & Happy":
                    print(heading_display(menu[heading][item]))
                    
               else:
                    for dishes in menu[heading][item]:
                         dish_list.append(f"{dishes['name']} - ${dishes['Price']}")

                    menu_items.update({menu_categories[add_on]: dish_list})
                    add_on += 1


               dish_list = []

     return menu_items


def order_report(menu_categories= menu_category(), menu_items= menu_order_options()):
     session_id = 1
     order_id = 1

     question1 = [
          inquirer.Text(
               "name",
               message= "Please enter your name"
          ),
     ]

     info1 = inquirer.prompt(question1)
     result_update(info1)

     phone = [
          inquirer.Text(
               "phone",
               message= "Please enter your phone number"
          ),
     ]

     phone_no = inquirer.prompt(phone)
     result_update(phone_no)

     question2 = [
          inquirer.List(
               f"category{order_id}",
               message= "What would you like to eat",
               choices= menu_categories
          )
     ]

     info2 = inquirer.prompt(question2)
     result_update(info2)


     question3 = [
          inquirer.List(
               f"order{order_id}",
               message= "What would you like to order",
               choices= menu_items[result[f"category{order_id}"]]
          )
     ]

     info3 = inquirer.prompt(question3)
     info3[f"order{order_id}"] = info3[f"order{order_id}"].split(" - ")[0]
     result_update(info3)

     confirm_question = [
          inquirer.Confirm(
               "confirm",
               message= "Would you like to order again?"
          )
     ]

     info4 = inquirer.prompt(confirm_question)
     result_update(info4)

     while result["confirm"] == True:
          order_id += 1

          question2 = [
               inquirer.List(
                    f"category{order_id}",
                    message= "What would you like to eat",
                    choices= menu_categories
               )
          ]

          info2 = inquirer.prompt(question2)
          result_update(info2)

          question3 = [
               inquirer.List(
                    f"order{order_id}",
                    message= "What would you like to order",
                    choices= menu_items[result[f"category{order_id}"]]
               )
          ]

          info3 = inquirer.prompt(question3)
          info3[f"order{order_id}"] = info3[f"order{order_id}"].split(" - ")[0]
          result_update(info3)

          confirm_question = [
               inquirer.Confirm(
                    "confirm",
                    message= "Would you like to order more?"
               )
          ]

          info4 = inquirer.prompt(confirm_question)
          result_update(info4)

     order_date = datetime.date.today()
     order_time = datetime.datetime.now().time()

     result.update({"order_date": str(order_date)})
     result.update({"order_time": str(order_time)})

     total_bill = fetch_prices(result)
     result.update({"Total Bill": total_bill})
     
     return result

