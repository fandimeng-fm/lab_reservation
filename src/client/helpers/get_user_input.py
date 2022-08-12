from ast import Assert
from PyInquirer import prompt
from examples import custom_style_2
from datetime import date, timedelta, datetime

from helpers.check_user_input import *
from helpers.reservation_api_calls import *
from helpers.user_api_calls import *


def get_and_validate_user_id():
    '''
    Prompt the user to input the user ID and perform validation
    '''
    while True:
        answers = prompt({
            'type': 'input',
            'name': 'user_id',
            'message': 'Please enter your user ID: '
        }, style=custom_style_2)
        user_id = answers['user_id']
        answers = prompt({
            'type': 'password',
            'name': 'password',
            'message': 'Please enter password: '
        }, style=custom_style_2)
        password = answers['password']
        role = get_user_role(user_id, password)
        if role:
            return user_id, role

def get_user_id(text):
    '''
    Prompt the user to input the user ID
    '''
    answers = prompt({
        'type': 'input',
        'name': 'user_id',
        'message': text
    }, style=custom_style_2)
    return answers['user_id']

def get_password(message = 'Please enter password: '):
    '''
    Prompt the user to input password
    '''
    answers = prompt({
        'type': 'password',
        'name': 'password',
        'message': message
    }, style=custom_style_2)
    return answers['password']

def get_role(text):
    '''
    Prompt the user to input the user ID and validate
    '''
    answers = prompt({
        'type': 'list',
        'name': 'role',
        'message': text,
        'choices': [
            "Scheduler",
            "Admin",
            "Client"
        ]
    }, style=custom_style_2)
    return answers['role']

def get_client_id(text = 'Please enter the client ID you are making a reservation for: '):
    '''
    Prompt the user to input the client ID
    '''
    answers = prompt({
        'type': 'input',
        'name': 'client_id',
        'message': text
    }, style=custom_style_2)
    return answers['client_id']

def get_duration():
    '''
    Prompt for duration and check if input is a float
    '''
    # While loop until the input is a valid float
    while True:
        try: 
            answers = prompt({
                'type': 'input',
                'name': 'float',
                'message': "Please enter booking duration as a float:"
            }, style=custom_style_2)
            f = float(answers['float'])
            break
        except ValueError:
            pass
        print("Input has to be a float, please re-enter")
    return f

def get_balance_update():
    '''
    Prompt the user to input the amount of balance they awnat ot 
    '''
    while True:
        try: 
            answers = prompt({
                'type': 'input',
                'name': 'bal',
                'message': "Please enter the amount to add to balance:"
            }, style=custom_style_2)
            f = int(answers['bal'])
            assert f >= 1 and f <= 25000
            break
        except AssertionError:
             pass
        print("Input has to be an amount between 1 and 25,000")
    return f

def get_reservation_datetime():
    '''
    Get user input of reservation date and time
    '''
    # calculating the last date the user can enter for
    today = date.today()
    end_date = today + timedelta(days = 30)
    str_end_date = end_date.strftime("%Y-%m-%d")
    
    # Input date of booking
    print("Only make bookings until: " + str_end_date)
    str_reservation_date = check_input_date(
        'Enter your reservation date (YYYY-MM-DD): ', 
        reservation=True
    )
    reservation_date = datetime.strptime(str_reservation_date, 
        '%Y-%m-%d').date()

    # Booking time
    print(f"Booking day is: { reservation_date.strftime('%A') }")
    reservation_time = check_input_float("Enter start time in multiples of 0.5" \
        " (9 - 18 on Weekdays, 10 - 16 on Saturdays): ", reservation_date)

    duration = check_input_float(f"Enter duration in multiples of 0.5", reservation_date, \
        duration = True, start = reservation_time)
    
    return str_reservation_date, reservation_time, duration

def get_reservation_id():
    '''
    Get user input of reservation ID
    '''
    return check_input_int("Enter the reservation ID you wish to cancel: ")

def get_booking_item():
    '''
    Get user input of reservation item
    '''
    answers = prompt({
        'type': 'list',
        'name': 'item',
        'message': 'Please select the item you want to reserve, and press the enter key: ',
        'choices': [
            "Microvac",
            "Irradiator",
            "Polymer Extruder",
            "High Velocity Crusher",
            "1.21 Gigawatt Lightning Harvester",
            "Workshop",
            "Exit"
        ]
    }, style=custom_style_2)

    if answers['item'] == "Exit":
        exit(0)
    else:
        if answers['item'] == "Polymer Extruder":
            return "extruder"
        if answers['item'] == "High Velocity Crusher":
            return "crusher"
        if answers['item'] == "1.21 Gigawatt Lightning Harvester":
            return "harvester"
        return answers['item'].lower()


def get_recurrence():
    '''
    Get user input of whether the reservation is recurring
    '''
    answers = prompt({
        'type': 'list',
        'message': 'Is this a recurring reservation? Select yes or no and press the enter key: ',
        'name': 'recurrence',
        'choices':[
            "Yes",
            "No"
        ],
    }, style=custom_style_2)

    # recurring is off by default
    recurring, recurring_times = "off", 0

    if answers['recurrence'] == "Yes":
        recurring = "on"
        recurring_times = check_input_int("Please enter the recurring time: ")
    return recurring, recurring_times