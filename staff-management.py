import inquirer
from tabulate import tabulate

# Sample restaurant staff data
staff_list = [
    {"id": 1, "name": "Alice", "role": "Manager", "shift": "Morning"},
    {"id": 2, "name": "Bob", "role": "Chef", "shift": "Evening"},
    {"id": 3, "name": "Charlie", "role": "Server", "shift": "Morning"},
    {"id": 4, "name": "David", "role": "Dishwasher", "shift": "Night"},
]

# Function to display the staff list in a tabular format
def display_staff():
    print("\n--- Restaurant Staff ---")
    headers = ["ID", "Name", "Role", "Shift"]
    table = [[staff["id"], staff["name"], staff["role"], staff["shift"]] for staff in staff_list]
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print("\n")

# Function to add a new staff member
def add_staff():
    questions = [
        inquirer.Text('name', message="Enter the staff's name"),
        inquirer.List('role', message="Select the staff's role", choices=["Manager", "Chef", "Server", "Dishwasher"]),
        inquirer.List('shift', message="Select the staff's shift", choices=["Morning", "Evening", "Night"]),
    ]
    answers = inquirer.prompt(questions)

    # Generate a new ID based on the current staff list
    new_id = max([staff["id"] for staff in staff_list]) + 1 if staff_list else 1
    staff_list.append({"id": new_id, "name": answers['name'], "role": answers['role'], "shift": answers['shift']})

    print(f"\nStaff {answers['name']} added successfully!\n")

# Function to update an existing staff member
def update_staff():
    staff_ids = [str(staff["id"]) for staff in staff_list]
    questions = [
        inquirer.List('id', message="Select a staff member to update", choices=staff_ids),
    ]
    answers = inquirer.prompt(questions)
    selected_id = int(answers['id'])
    
    # Find the selected staff member
    staff_member = next(staff for staff in staff_list if staff['id'] == selected_id)

    update_questions = [
        inquirer.Text('name', message="Enter the new name", default=staff_member['name']),
        inquirer.List('role', message="Select the new role", choices=["Manager", "Chef", "Server", "Dishwasher"], default=staff_member['role']),
        inquirer.List('shift', message="Select the new shift", choices=["Morning", "Evening", "Night"], default=staff_member['shift']),
    ]
    updated_answers = inquirer.prompt(update_questions)

    # Update staff member details
    staff_member['name'] = updated_answers['name']
    staff_member['role'] = updated_answers['role']
    staff_member['shift'] = updated_answers['shift']

    print(f"\nStaff member with ID {selected_id} updated successfully!\n")

# Main menu function
def main():
    while True:
        # Display options to the user
        questions = [
            inquirer.List('action', message="Choose an action", choices=[
                'Display Staff',
                'Add New Staff',
                'Update Existing Staff',
                'Exit'
            ]),
        ]
        action = inquirer.prompt(questions)

        if action['action'] == 'Display Staff':
            display_staff()
        elif action['action'] == 'Add New Staff':
            add_staff()
        elif action['action'] == 'Update Existing Staff':
            update_staff()
        elif action['action'] == 'Exit':
            print("Exiting the restaurant staff management system.")
            break
        else:
            print("Invalid choice! Please select again.")


main()