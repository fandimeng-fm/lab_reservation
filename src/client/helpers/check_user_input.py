from PyInquirer import prompt
from examples import custom_style_2
from datetime import datetime, date

def check_input_date(text, reservation=False):
    '''
    Prompt and check if the input date is valid

    Inputs:
      text (string): the message the show the user
      reservation (bool): if the input is for making reservation
    '''
    # While loop until the input is of correct format
    while True:
        try: 
            answers = prompt({
                'type': 'input',
                'name': 'date',
                'message': text
            }, style=custom_style_2)
            date_str = answers['date']
            reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            break
        except ValueError:
            pass
        print("Incorrect format, please re-enter")

    # If the input date is for reservation, check if it's in allowed date range
    if reservation:
        # check if the input date is a Sunday
        if reservation_date.strftime("%A") == "Sunday":
            print("No bookings allowed on Sunday!")
            return check_input_date(text, reservation=True)

        # check if the input is within 30 days
        today = date.today()
        diff = reservation_date - today
        if diff.days < 0:
            print("You can't make reservation in the past")
            return check_input_date(text, reservation=True)
        elif diff.days > 30:
            print("You can only make reservation up to 30 days in advance")
            return check_input_date(text, reservation=True)
    return date_str

def check_input_float(text, reservation_date=None, duration=False, start=None):
    '''
    Prompt and check if the input float is valid

    Inputs:
      reservation_date (string): the reservation date
      text (string): the message the show the user
    '''
    # While loop until the input is a valid float
    while True:
        try: 
            answers = prompt({
                'type': 'input',
                'name': 'float',
                'message': text
            }, style=custom_style_2)
            f = float(answers['float'])
            if (2 * f).is_integer():
                break
        except ValueError:
            pass
        print("Input has to be a float that's multiple of 0.5, please re-enter")
    if duration:
        if reservation_date.strftime("%A") == "Saturday" and ( start + f > 16):
            print("You can only book reservation from 10 to 16 on Saturday")
            return check_input_float(text, reservation_date, duration = True, start = start)
        elif f + start > 18:
            print("You can only book reservation from 9 to 18 on Weekdays")
            return check_input_float(text, reservation_date, duration = True, start = start)
    elif reservation_date:
        # check if the input time is valid according to the reservation date
        if reservation_date.strftime("%A") == "Saturday" and (f < 10 or f > 15.5):
            print("You can only book reservation from 10 to 16 on Saturday")
            return check_input_float(text, reservation_date)
        elif f < 9 or f > 17.5:
            print("You can only book reservation from 9 to 18 on Weekdays")
            return check_input_float(text, reservation_date)
    
    return f

def check_input_int(text):
    '''
    Prompt and check if the input text is valid

    Inputs:
      text (string): the message the show the user
    '''
    # While loop until the input is a valid uuid
    while True:
        try: 
            answers = prompt({
                'type': 'input',
                'name': 'int',
                'message': text
            }, style=custom_style_2)
            i = int(answers['int'])
            break
        except ValueError:
            pass
        print("Input has to be a valid integer, please re-enter")
    return i
