
# Test file for client.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: pytest

import textwrap
import datetime

from helpers import keys
from helpers import create_example_fixture, next_weekday


client = create_example_fixture('client.py')
today = datetime.date.today()
end_date = today + datetime.timedelta(days = 30)
monday = next_weekday(today, 0)
saturday = next_weekday(today, 5)
sunday = next_weekday(today, 6)

str_end_date = end_date.strftime("%Y-%m-%d")
str_today = today.strftime("%Y-%m-%d")
str_monday = monday.strftime("%Y-%m-%d")
str_saturday = saturday.strftime("%Y-%m-%d")
str_sunday = sunday.strftime("%Y-%m-%d")

today_weekday = today.strftime("%A")

def test_invalid_user(client):
    '''
    Test if the client correctly check for valid user
    '''
    client.expect(textwrap.dedent("? Please enter your user ID:   "))
    client.writeline("invalid")
    client.expect(textwrap.dedent(f"""\
        ? Please enter your user ID:   invalid
        Validation failed: That user ID does not exist in our system.
        ? Please enter your user ID:   """))

def test_valid_admin(client):
    '''
    Test if the client correctly check for admin
    '''
    client.expect(textwrap.dedent("? Please enter your user ID:   "))
    client.writeline("admin1")
    client.expect(textwrap.dedent(f"""\
        ? Please enter your user ID:   admin1
        Validation successful! Your role is: admin
        Today's date: {str_today}
        ? Please select an action to perform and press the enter key:   (Use arrow keys)
         ❯ Manage users
           Make a booking
           Cancel a booking and get refund
           View all reservations on a date range
           View all reservations on a date range for a specific client
           View all financial transactions on a date range
           Exit"""))

def test_valid_scheduler(client):
    '''
    Test if the client correctly check for scheduler
    '''
    client.expect(textwrap.dedent("? Please enter your user ID:   "))
    client.writeline("scheduler1")
    client.expect(textwrap.dedent(f"""\
        ? Please enter your user ID:   scheduler1
        Validation successful! Your role is: scheduler
        Today's date: {str_today}
        ? Please select an action to perform and press the enter key:   (Use arrow keys)
         ❯ Make a booking
           Cancel a booking and get refund
           View all reservations on a date range
           View all reservations on a date range for a specific client
           View all financial transactions on a date range
           Exit"""))

def test_make_reservation_bad_date(client):
    '''
    Test if the client correctly check for invalid input date
    '''
    client.expect(textwrap.dedent("? Please enter your user ID:   "))
    client.writeline("admin1")
    client.expect(textwrap.dedent(f"""\
        ? Please enter your user ID:   admin1
        Validation successful! Your role is: admin
        Today's date: {str_today}
        ? Please select an action to perform and press the enter key:   (Use arrow keys)
         ❯ Manage users
           Make a booking
           Cancel a booking and get refund
           View all reservations on a date range
           View all reservations on a date range for a specific client
           View all financial transactions on a date range
           Exit"""))
    client.write(keys.DOWN)
    client.write(keys.ENTER)
    client.expect(textwrap.dedent(f"""\
        ? Please select an action to perform and press the enter key:   Make a booking
        ? Please enter the client ID you are making reservation for:   """))
    client.writeline('test')
    client.expect(textwrap.dedent(f"""\
        ? Please enter the client ID you are making reservation for:   test
        Only make bookings until: {str_end_date}
        ? Enter your reservation date (YYYY-MM-DD):   """))

    # The case where the input is not a date
    client.writeline('invalid date')
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   invalid date
        Incorrect format, please re-enter
        ? Enter your reservation date (YYYY-MM-DD):   """))
    
    # The case where the input is a date formatted incorrectly
    client.writeline('05-22-2022')
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   05-22-2022
        Incorrect format, please re-enter
        ? Enter your reservation date (YYYY-MM-DD):   """))
    
    # The case where the input date is in the past
    client.writeline('2022-03-05')
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   2022-03-05
        You can't make reservation in the past
        ? Enter your reservation date (YYYY-MM-DD):   """))
    
    # The case where the input date is more than 30 days away
    client.writeline('2022-11-03')
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   2022-11-03
        You can only make reservation up to 30 days in advance
        ? Enter your reservation date (YYYY-MM-DD):   """))
    
    # The case where the input date is a Sunday
    client.writeline(str_sunday)
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   {str_sunday}
        No bookings allowed on Sunday!
        ? Enter your reservation date (YYYY-MM-DD):   """))

def test_make_reservation_bad_time_weekday(client):
    '''
    Test if the client correctly check for invalid input time on weekdays
    '''
    client.expect(textwrap.dedent("? Please enter your user ID:   "))
    client.writeline("admin1")
    client.expect(textwrap.dedent(f"""\
        ? Please enter your user ID:   admin1
        Validation successful! Your role is: admin
        Today's date: {str_today}
        ? Please select an action to perform and press the enter key:   (Use arrow keys)
         ❯ Manage users
           Make a booking
           Cancel a booking and get refund
           View all reservations on a date range
           View all reservations on a date range for a specific client
           View all financial transactions on a date range
           Exit"""))
    client.write(keys.DOWN)
    client.write(keys.ENTER)
    client.expect(textwrap.dedent(f"""\
        ? Please select an action to perform and press the enter key:   Make a booking
        ? Please enter the client ID you are making reservation for:   """))
    client.writeline('test')
    client.expect(textwrap.dedent(f"""\
        ? Please enter the client ID you are making reservation for:   test
        Only make bookings until: {str_end_date}
        ? Enter your reservation date (YYYY-MM-DD):   """))
    client.writeline(str_monday)
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   {str_monday}
        Booking day is: Monday
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is not a float
    client.writeline("not a float")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   not a float
        Input has to be a float that's multiple of 0.5, please re-enter
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is not a multiple of 0.5
    client.writeline("9,2")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   9,2
        Input has to be a float that's multiple of 0.5, please re-enter
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is smaller than 9
    client.writeline("8")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   8
        You can only book reservation from 9 to 18 on Weekdays
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is larger than 18
    client.writeline("19")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   19
        You can only book reservation from 9 to 18 on Weekdays
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))

def test_make_reservation_bad_time_saturday(client):
    '''
    Test if the client correctly check for invalid input time on Saturday
    '''
    client.expect(textwrap.dedent("? Please enter your user ID:   "))
    client.writeline("admin1")
    client.expect(textwrap.dedent(f"""\
        ? Please enter your user ID:   admin1
        Validation successful! Your role is: admin
        Today's date: {str_today}
        ? Please select an action to perform and press the enter key:   (Use arrow keys)
         ❯ Manage users
           Make a booking
           Cancel a booking and get refund
           View all reservations on a date range
           View all reservations on a date range for a specific client
           View all financial transactions on a date range
           Exit"""))
    client.write(keys.DOWN)
    client.write(keys.ENTER)
    client.expect(textwrap.dedent(f"""\
        ? Please select an action to perform and press the enter key:   Make a booking
        ? Please enter the client ID you are making reservation for:   """))
    client.writeline('test')
    client.expect(textwrap.dedent(f"""\
        ? Please enter the client ID you are making reservation for:   test
        Only make bookings until: {str_end_date}
        ? Enter your reservation date (YYYY-MM-DD):   """))
    client.writeline(str_saturday)
    client.expect(textwrap.dedent(f"""\
        ? Enter your reservation date (YYYY-MM-DD):   {str_saturday}
        Booking day is: Saturday
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is not a float
    client.writeline("not a float")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   not a float
        Input has to be a float that's multiple of 0.5, please re-enter
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is smaller than 10
    client.writeline("9.5")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   9.5
        You can only book reservation from 10 to 16 on Saturday
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
    
    # The case where the input is larger than 16
    client.writeline("17")
    client.expect(textwrap.dedent(f"""\
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   17
        You can only book reservation from 10 to 16 on Saturday
        ? Enter start time in multiples of 0.5 (9 - 18 on Weekdays, 10 - 16 on Saturdays
        ):   """))
