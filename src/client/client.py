# Client User Interface
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: python client.py

from PyInquirer import prompt
from examples import custom_style_2
from datetime import date
import six
from pyfiglet import figlet_format
from termcolor import colored

from helpers.check_user_input import *
from helpers.get_user_input import *
from helpers.reservation_api_calls import *
from helpers.user_api_calls import *
from enum import Enum

import requests

BASE_URL = "http://127.0.0.1:8000"

class Action(Enum):
    BOOK = "Make a booking"
    HOLD = "Make a hold"
    MANAGE = "Manage Users"
    CANCEL = "Cancel a booking/hold and process refund"
    LISTALLCLIENTS = "List all clients"
    VIEWRESDATE = "View all reservations on a date range"
    VIEWRESCLIENT = "View all reservations on a date range for a specific client"
    CREATECLIENT = "Create a new client"
    ADDFUNDS = "Add funds to account"
    VIEWTRANS = "View all financial transactions"
    VIEWTRANSCLIENT = "View all financial transactions for a specific client"
    EDITPROFILE = "Edit profile"
    VIEWMYRES = "View all my reservations"
    VIEWMYTRANS = "View all my financial transactions"
    BALANCE = "View account balance"
    VIEWHOLD = "View holds for other remote facilities"
    EXIT = "Exit"
    

PRIVILEGES = {
    'scheduler': [
        Action.BOOK.value,
        Action.CANCEL.value,
        Action.MANAGE.value,
        Action.VIEWRESCLIENT.value,
        Action.VIEWRESDATE.value,
        Action.ADDFUNDS.value,
        Action.VIEWTRANS.value,
        Action.VIEWTRANSCLIENT.value,
        Action.VIEWHOLD.value,
        Action.EXIT.value
        ],
    'admin': [
        Action.MANAGE.value,
        Action.EXIT.value
        ],
    'client': [
        Action.BOOK.value,
        Action.CANCEL.value,
        Action.VIEWMYRES.value,
        Action.VIEWMYTRANS.value,
        Action.EDITPROFILE.value,
        Action.ADDFUNDS.value,
        Action.BALANCE.value,
        Action.EXIT.value
        ],
    'remote': [
        # SHOULD MAYBE MAKE SEPARATE HOLD ACTION FOR REMOTE ROLE INSTEAD OF BOOK???
        Action.HOLD.value,
        Action.EXIT.value
        ]
}

def prompt_user(message: str, choices: list):
    answers = prompt({
        'type': 'list',
        'name': 'choice',
        'message': message,
        'choices': choices
    }, style=custom_style_2)
    return answers['choice']

def user_interface(my_user_id, my_role):
    '''
    This function handles the user interface
    '''
    # Prompt user to select the action to perform
    action_choice = prompt_user(f'Please select an action to perform and press the enter key: ', \
        PRIVILEGES[my_role])
    if action_choice == Action.MANAGE.value:
        print("The system currently has the following users: ")
        get_all_users()
        
        user_action_choice = prompt_user(f'Please select an action to perform and press the enter key: ', \
            [
                "Add a user",
                "Edit a user",
                "Remove a user",
                "Deactivate a user",
                "Reactivate a user",
            ]) 
        # Handle the case where user wants to add a user
        if user_action_choice == "Add a user":
            user_id = get_user_id("Please enter the User ID you wish to add: ")
            role = get_role("Please select the role of the user and press the enter key:")
            password = get_password()
            add_user(user_id, password, role)
            if role == "Client":
                balance = get_balance_update()
                update_balance(user_id, balance)
                
        # Handle the case where user wants to update a user role
        elif user_action_choice == "Edit a user":
            user_id = get_user_id("Please enter the User ID you wish to edit: ")
            edit_user_choice = prompt_user(f'Please select an action to perform and press the enter key: ', \
                [
                    "Update a user role",
                    "Change a user ID",
                    "Change a user password",
                ]) 
            # Handle the case where user wants to update a user role
            if edit_user_choice == "Update a user role":
                role = get_role("Please select the new role of the user and press the enter key:")
                update_user_role(user_id, role)
            # Handle the case where user wants to update a user ID
            elif edit_user_choice == "Change a user ID":
                new_user_id = get_user_id("Please enter the User ID you wish to update TO: ")
                update_user_id(user_id, new_user_id)
            # Handle the case where user wants to update a user password
            elif edit_user_choice == "Change a user password":
                new_pw = get_password('Please enter the new password')
                update_user_password(user_id, new_pw)

        # Handle the case where user wants to remove a user
        elif user_action_choice == "Remove a user":
            user_id = get_user_id("Please enter the User ID you wish to remove: ")
            remove_user(user_id)
        # Handle deactivation
        elif user_action_choice == "Deactivate a user":
            user_id = get_user_id("Please enter the User ID you wish to deactivate: ")
            deactivate_user(user_id)

        # Handle reactivation
        elif user_action_choice == "Reactivate a user":
            user_id = get_user_id("Please enter the User ID you wish to activate: ")
            activate_user(user_id)
    elif action_choice == Action.EDITPROFILE.value:
        edit_user_choice = prompt_user(f'Please select an action to perform and press the enter key: ', \
            [
                "Change user ID",
                "Change password",
            ]) 
        if edit_user_choice == "Change user ID":
            new_user_id = get_user_id("Please enter the User ID you wish to update TO: ")
            update_user_role(my_user_id, new_user_id)
        elif edit_user_choice == "Change password":
            new_pw = get_password('Please enter the new password')
            update_user_password(my_user_id, new_pw)

    # Handle the case where user wants to make a reservation or hold
    elif (action_choice == Action.BOOK.value) or (action_choice == Action.HOLD.value):
        
        if my_role == "client":
            client_id = my_user_id
        else:
            client_id = get_client_id()

        # Get the reservation date, time, and duration
        str_reservation_date, reservation_time, duration = get_reservation_datetime()

        # Get the booking item
        item = get_booking_item()

        
        if action_choice == Action.BOOK.value:
            post_body = {
            "facility": "facility1",
            "user_id": my_user_id,
            "reservation_item": item,
            "reservation_client_id": client_id,
            "reservation_date": str_reservation_date,
            "reservation_time": reservation_time,
            "duration": duration
            }
            make_reservation(post_body)
        else:
            post_body = {
            "facility": "facility1",
            "user_id": my_user_id,
            "hold_item": item,
            "hold_client_id": client_id,
            "hold_date": str_reservation_date,
            "hold_time": reservation_time,
            "duration": duration
            }
            make_hold(post_body)

    # Handle the case where user wants to cancel a reservation
    elif action_choice == Action.CANCEL.value:
        reservation_id = get_reservation_id()
        cancel_reservation(reservation_id)

    # Handle the case where user wants to view all reservations
    elif action_choice == Action.VIEWRESDATE.value:
        export = prompt_user("Please select if you would like to export your report as a CSV and press enter: ",\
            ["Yes", "No"]
        )
        
        start_date = check_input_date("Enter the start date of your query (YYYY-MM-DD): ")
        end_date = check_input_date("Enter the end date of your query (YYYY-MM-DD): ")
        if export == "Yes":
            file_name = prompt({
                'type': 'input',
                'name': 'name',
                'message': "Please enter what you'd like the file name saved as. If no preference, just press enter: "
            }, style=custom_style_2)
            file_loc = prompt({
                'type': 'input',
                'name': 'loc',
                'message': "Please enter the directory you'd like the file saved in (ending in a \). If no preference, just press enter: "
            }, style=custom_style_2)
            get_reservations(start_date, end_date, customer_id = None, export_csv = True, location = file_loc['loc'], name = file_name['name'])
        else:
            get_reservations(start_date, end_date, customer_id = None, export_csv = False)

    # Handle the case where user wants to view all clients
    elif action_choice == Action.LISTALLCLIENTS.value:
        get_all_clients()

    # Handle the case where user wants to view all transactions
    elif action_choice == Action.VIEWTRANS.value:
        get_all_transactions()

    # Handle the case where user wants to view all reservtations by a specific client
    elif action_choice == Action.VIEWRESCLIENT.value:
        export = prompt_user("Please select if you would like to export your report as a CSV and press enter: ",\
            ["Yes", "No"]
        )
        
        start_date = check_input_date("Enter the start date of your query (YYYY-MM-DD): ")
        end_date = check_input_date("Enter the end date of your query (YYYY-MM-DD): ")
        client_id = get_client_id()
        if export == "Yes":
            file_name = prompt({
                'type': 'input',
                'name': 'name',
                'message': "Please enter what you'd like the file name saved as. If no preference, just press enter: "
            }, style=custom_style_2)
            file_loc = prompt({
                'type': 'input',
                'name': 'loc',
                'message': "Please enter the directory you'd like the file saved in (ending in a \). If no preference, just press enter: "
            }, style=custom_style_2)
            get_reservations(start_date, end_date, client_id, export_csv = True, location = file_loc['loc'], name = file_name['name'])
        else:
            get_reservations(start_date, end_date, client_id, export_csv = False)
    # Handle the case where user wants to view all reservtations by a specific client
    elif action_choice == Action.VIEWMYRES.value:
        export = prompt_user("Please select if you would like to export your report as a CSV and press enter: ",\
            ["Yes", "No"]
        )
        
        start_date = check_input_date("Enter the start date of your query (YYYY-MM-DD): ")
        end_date = check_input_date("Enter the end date of your query (YYYY-MM-DD): ")
        if export == "Yes":
            file_name = prompt({
                'type': 'input',
                'name': 'name',
                'message': "Please enter what you'd like the file name saved as. If no preference, just press enter: "
            }, style=custom_style_2)
            file_loc = prompt({
                'type': 'input',
                'name': 'loc',
                'message': "Please enter the directory you'd like the file saved in (ending in a \). If no preference, just press enter: "
            }, style=custom_style_2)
            get_reservations(start_date, end_date, my_user_id, export_csv = True, location = file_loc['loc'], name = file_name['name'])
        else:
            get_reservations(start_date, end_date, my_user_id, export_csv = False)
    # Handle the case where user wants to view all transactions by a specific client
    elif action_choice == Action.VIEWTRANSCLIENT.value:
        client_id = get_client_id()
        get_all_transactions_by_id(client_id)
    # Handle the case where client wants to all transactions by themselves
    elif action_choice == Action.VIEWMYTRANS.value:
        get_all_transactions_by_id(my_user_id)
    # Handle the case where client wants to view balance
    elif action_choice == Action.BALANCE.value:
        get_user_balance(my_user_id)

    # Handle the case where client wants to add funds
    elif action_choice == Action.ADDFUNDS.value:
        if my_role == "client":
            balance = get_balance_update()
            update_balance(my_user_id, balance)
        else: 
            print("The system currently has the following users: ")
            get_all_users()
            client = get_user_id("Please enter the client you'd like to add funds for: ")
            balance = get_balance_update()
            update_balance(client, balance)

    # Handle the case where user wants to view all holds made for other facilities
    elif action_choice == Action.VIEWHOLD.value:
        get_all_holds()
    # Handle the case where user wants to exit
    else:
        exit(0)

    restart_or_exit(my_user_id, my_role)


def restart_or_exit(user_id, role):
    '''
    This function checks if user wants to restart or exit the program
    '''
    if prompt_user(f'Do you want to restart? Select yes or no and press the enter key: ', \
        ['Yes', 'No'] ) == "Yes":
        user_interface(user_id, role)
    else:
        exit(0)

def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

def main():
    log("Mad Scientist", color="blue", figlet=True)
    pref = client_signin_pref()

    if pref:
        log("CLIENT SIGN-IN IS ALLOWED", color="green")
    else:
        log("CLIENT SIGN-IN IS DISABLED", color="red")

    user_id, role = get_and_validate_user_id()

    # Show user today's date
    str_today = date.today().strftime("%Y-%m-%d")
    print("Today's date: " + str_today)

    user_interface(user_id, role)


if __name__ == "__main__":
    main()