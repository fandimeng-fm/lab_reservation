# Test file for reservation_api_calls.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: pytest

import helpers.reservation_api_calls as reservation_api_calls


def test_reservation(capfd):
    '''
    Test the creation of a non-recurring reservation
    '''

    # Reservation details
    payload = {"facility": "facility1",
      "user_id": "admin1",
      "reservation_item": "workshop",
      "reservation_client_id": "Good Client",
      "reservation_date": "2022-05-20",
      "reservation_time": 9,
      "duration": 0.5
    }
    reservation_api_calls.make_reservation(payload)
    out, _ = capfd.readouterr()

    assert 'Reservation failed: Insufficient balance.' in out


def test_cancel(capfd):
    '''
    Test cancelling a reservation using an invalid reservation_id
    '''
    # Use test data

    bad_id = '12345'
    
    reservation_api_calls.cancel_reservation(bad_id)
    out, _ = capfd.readouterr()

    assert "That reservation ID does not exist in our system." in out


def test_view_reservations(capfd):
    '''
    Test output of GET /reservations endpoint when there are no reservations for parameters given
    '''
    # Use test data
    
    date_start = '2022-06-20'
    date_end = '2022-06-30'
    reservation_api_calls.get_reservations(date_start, date_end)
    out, _ = capfd.readouterr()

    assert "All reservations for date range" in out


def test_view_client_reservations_none(capfd):
    '''
    Test output of GET /reservations endpoint using date and client_id when there are no reservations for parameters
    '''

    date_start = '2022-05-20'
    date_end = '2022-05-30'
    client_id = "Bad Client"
    reservation_api_calls.get_reservations(date_start, date_end, client_id)
    out, _ = capfd.readouterr()

    assert "All reservations for date range" in out

def test_get_transactions():
    '''
    Test output of GET /transactions endpoint when there are transactions for parameters given
    '''
    
    reservation_api_calls.get_all_transactions()

def test_get_transactions_by_id(capfd):
    '''
    Test output of GET /transactions endpoint when there are transactions for parameters given
    '''
    user_id = "Good Client"
    reservation_api_calls.get_all_transactions_by_id(user_id)
    out, _ = capfd.readouterr()

    assert user_id in out