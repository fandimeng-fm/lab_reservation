# Test file for reservations_API.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: pytest

import requests
import helpers.reservation_functions as reservation_functions
import database.database_reservations as database_reservations
import database.database_users as database_users
from datetime import datetime


def test_good_reservation():
    '''
    Test the creation of a non-recurring reservation
    '''

    # Use test data
    database_reservations.use_test_db()

    #Update admin1 balance to be sufficient for reservation
    database_users.db_update_balance('admin1', 100000)

    # Number of previous reservations for date
    prev_res = len(database_reservations.db_get_reservations_between_dates("2022-05-20",
        "2022-05-20", "facility1"))

    # Reservation details
    good_res = {"facility": "facility1",
      "user_id": "admin1",
      "reservation_item": "workshop",
      "reservation_client_id": "Good Client",
      "reservation_date": "2022-05-20",
      "reservation_time": 9,
      "duration": 0.5
    }
    url = "http://127.0.0.1:8000/reservations/"
    response = requests.post(url, json=good_res)

    j = response.json()

    # Number of new reservations for date
    new_res = len(database_reservations.db_get_reservations_between_dates("2022-05-20",
        "2022-05-20", "facility1"))
    
    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["message"] == "Reservation was successful! "
    assert new_res == prev_res + 1


def test_bad_reservation():
    '''
    Test the creation of a bad reservation for a used machine
    '''
    # Use test data
    database_reservations.use_test_db()

    #Update admin1 balance to be sufficient for reservation
    database_users.db_update_balance('admin1', 100000)
    
    res1 = {"facility": "facility1",
      "user_id": "admin1",
      "reservation_item": "harvester",
      "reservation_client_id": "Bad Client New",
      "reservation_date": "2022-05-12",
      "reservation_time": 9,
      "duration": 0.5
    }
    url = "http://127.0.0.1:8000/reservations/"
    response = requests.post(url, json=res1)

    res2 = {"facility": "facility1",
      "user_id": "admin1",
      "reservation_item": "harvester",
      "reservation_client_id": "Bad Client New",
      "reservation_date": "2022-05-12",
      "reservation_time": 9,
      "duration": 0.5
    }
    url = "http://127.0.0.1:8000/reservations/"
    response = requests.post(url, json=res2)

    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 400
    assert j["detail"] == 'Machine booked for that time.'


def test_cancel():
    '''
    Test cancelling a reservation
    '''
    # Use test data
    database_reservations.use_test_db()

    # Number of previous reservations for date
    prev_res = len(database_reservations.db_get_reservations_between_dates("2022-05-10",
        "2022-05-10", "facility1"))

    good_id = '5'
    user_id = 'scheduler1'
    facility = 'facility1'
    url = "http://127.0.0.1:8000/reservations/cancel/" + good_id + "?user_id=" + user_id\
    + '&facility=' + facility
    response = requests.get(url)
    j = response.json()

    # Number of new reservations for date
    new_res = len(database_reservations.db_get_reservations_between_dates("2022-05-10",
        "2022-05-10", "facility1"))

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["message"] == 'Cancellation was successful!'
    assert prev_res == new_res+1


def test_cancel_hold():
    '''
    Test cancelling a hold
    '''
    # Use test data
    database_reservations.use_test_db()

    # Number of previous holds for date
    prev_hold = len(database_reservations.db_get_holds_between_dates("2022-05-31",
        "2022-05-31"))

    good_id = '13'
    user_id = 'remote client'
    facility = 'facility4'
    url = "http://127.0.0.1:8000/reservations/cancel/" + good_id
    response = requests.get(url)
    j = response.json()

    # Number of new reservations for date
    new_hold = len(database_reservations.db_get_holds_between_dates("2022-05-31",
        "2022-05-31"))

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["message"] == 'Hold cancellation was successful!'
    assert prev_hold == new_hold + 1



def test_bad_cancel():
    '''
    Test cancelling a reservation using an invalid reservation_id
    '''
    # Use test data
    database_reservations.use_test_db()

    bad_id = '12345'
    user_id = 'scheduler1'
    facility = 'facility1'
    url = "http://127.0.0.1:8000/reservations/cancel/" + bad_id + "?user_id=" + user_id\
    + '&facility=' + facility
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 400
    assert j["detail"] == "That reservation ID does not exist in our system."


def test_already_cancel():
    '''
    Test a reservation that was already cancelled
    '''
    # Use test data
    database_reservations.use_test_db()

    id = "1"
    user_id = 'scheduler1'
    facility = 'facility1'
    url = "http://127.0.0.1:8000/reservations/cancel/" + id + "?user_id=" + user_id\
    + '&facility=' + facility
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 400
    assert j["detail"] == "This reservation is already cancelled."


def test_view_reservations_none():
    '''
    Test output of GET /reservations endpoint when there are no reservations for parameters given
    '''
    # Use test data
    database_reservations.use_test_db()
    
    date_start = '2022-06-20'
    date_end = '2022-06-30'
    facility = 'facility1'
    url = f"http://127.0.0.1:8000/reservations?start_date={date_start}&"\
    f"end_date={date_end}&facility={facility}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"] == f"All reservations for date range {date_start} to {date_end}: \n"


def test_view_client_reservations_none():
    '''
    Test output of GET /reservations endpoint using date and client_id when there are no reservations for parameters
    '''
    # Use test data
    database_reservations.use_test_db()

    date_start = '2022-05-20'
    date_end = '2022-05-30'
    client_id = "Bad Client"
    facility = 'facility1'
    url = f"http://127.0.0.1:8000/reservations?start_date={date_start}&"\
    f"end_date={date_end}&customer_id={client_id}&facility={facility}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"] == f"All reservations for date range {date_start} to {date_end} for client {client_id}: \n"


def test_view_reservations_using_dates():
    '''
    Test output of GET /reservations endpoint using only dates
    '''
    # Use test data
    database_reservations.use_test_db()

    date_start = '2022-05-21'
    date_end = '2022-05-26'
    facility = 'facility1'
    url = f"http://127.0.0.1:8000/reservations?start_date={date_start}&"\
    f"end_date={date_end}&facility={facility}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"].count('Reservation ID') == 1

def test_view_holds_using_dates():
    '''
    Test output of GET /reservations endpoint using only dates
    '''
    # Use test data
    database_reservations.use_test_db()

    date_start = '2022-05-21'
    date_end = '2022-05-31'
    url = f"http://127.0.0.1:8000/reservations/holds?start_date={date_start}&"\
    f"end_date={date_end}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"].count('Reservation ID') == 2


def test_view_reservations_using_dates_client():
    '''
    Test output of GET /reservations endpoint using dates and a client_id
    '''
    # Use test data
    database_reservations.use_test_db()

    date_start = '2022-05-21'
    date_end = '2022-05-26'
    client_id = '3'
    facility = 'facility1'
    url = f"http://127.0.0.1:8000/reservations?start_date={date_start}&end_date={date_end}&"\
    f"customer_id={client_id}&facility={facility}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"].count('Reservation ID') == 1


def test_get_transactions():
    '''
    Test output of GET /transactions endpoint when there are transactions for parameters given
    '''
    # Use test data
    database_reservations.use_test_db()
    
    url = "http://127.0.0.1:8000/transactions"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"].count('Reservation ID') == 12

def test_get_transactions_by_id():
    '''
    Test output of GET /transactions endpoint when there are transactions for parameters given
    '''
    # Use test data
    database_reservations.use_test_db()

    user_id = 'admin1'
    
    url = f"http://127.0.0.1:8000/transactions/{user_id}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"].count('Reservation ID') == 2


def test_booked_machines():
    '''
    Test get_booked_machines function from reservation_functions
    '''
    # Use test data
    database_reservations.use_test_db()

    str_reservation_date = "2022-05-10"
    reservation_time = 9

    current_reservations = reservation_functions.get_booked_machines(str_reservation_date, reservation_time)
    assert len(current_reservations) == 3
    assert current_reservations == ['workshop', 'workshop', 'harvester']


def test_add_reservation_db():
    '''
    Test add_reservation_dict function
    '''
    # Use test data
    database_reservations.use_test_db()

    # Number of previous reservations for date
    prev_res = len(database_reservations.db_get_reservations_between_dates("2022-05-20",
        "2022-05-20", "facility1"))

    # Add 3 reservations
    reservation_functions.add_reservation_to_db('admin1', datetime(2022, 5, 20).date(), 'resy1', 'facility1', 'workshop',
    'Good Client', 9, 0.5, 'on')
    reservation_functions.add_reservation_to_db('admin1', datetime(2022, 5, 20).date(), 'resy2', 'facility1', 'workshop',
    'Good Client', 9, 0.5, 'on')
    reservation_functions.add_reservation_to_db('admin1', datetime(2022, 5, 20).date(), 'resy3', 'facility1', 'workshop',
    'Good Client', 9, 0.5, 'on')

    # Number of new reservations for date
    new_res = len(database_reservations.db_get_reservations_between_dates("2022-05-20",
        "2022-05-20", "facility1"))

    # Return DB to previous state
    database_reservations.restore_db_from_backup()

    assert new_res == prev_res + 3


def test_create_report():
    '''
    Test create_report function from reservation_functions
    '''
    # Use test data
    database_reservations.use_test_db()

    reservation = {'reservation_id':'1', 'resource':'workshop', 'client_id':'x', 'start_time':9, 'end_time':9.5, 'reservation_date':"2022-05-22"}
    report = reservation_functions.create_report(reservation)
    correct_report = '\nReservation ID: 1\n- Reserved Item: workshop\n- Booked Date: 2022-05-22\n'\
    '- Booked Time: 9\n- Booked by Client ID: x\n'
    assert report == correct_report

def test_good_hold():
    '''
    Test the creation of a non-recurring reservation
    '''

    # Use test data
    database_reservations.use_test_db()

    # Number of previous reservations for date
    prev_hold = len(database_reservations.db_get_holds_between_dates("2022-05-20",
        "2022-05-20"))

    # Reservation details
    good_hold = {"facility": "facility1",
      "user_id": "hold1",
      "hold_item": "workshop",
      "hold_client_id": "Good Hold Client",
      "hold_date": "2022-05-20",
      "hold_time": 9,
      "duration": 0.5
    }
    url = "http://127.0.0.1:8000/holds/"
    response = requests.post(url, json=good_hold)

    j = response.json()

    # Number of new reservations for date
    new_hold = len(database_reservations.db_get_holds_between_dates("2022-05-20",
        "2022-05-20"))
    
    # Restore original data
    database_reservations.restore_db_from_backup()

    assert response.status_code == 200
    assert j["message"] == "Hold was successful! "
    assert new_hold == prev_hold + 1