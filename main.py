from Order_management import order_management
import inquirer
import os
from pyfiglet import Figlet

if __name__ == "__main__":
    order_management()

    question = [
        inquirer.List(
            'action',
            message="What would you like to do?",
            choices=[
                'Place an Order',
                'Exit'
            ]
        )
    ]

    print("\n")
    answer = inquirer.prompt(question)

    if answer['action'] == 'Place an Order':
        while answer["action"] == "Place an Order":
            order_management()

            print("\n")
            answer = inquirer.prompt(question)

    else:
        print(Figlet(font= "smisome1").renderText("Goodbye!"))
        os._exit(0)
