import database.database_reservations as database_reservations
from datetime import datetime



def test_db_get_reservations_between_dates_and_client():
    '''
    Test db_get_reservations_between_dates_and_client function output
    '''
    reservations_bewteen_dates = database_reservations.db_get_reservations_between_dates_and_client("2022-05-10",
        "2022-05-15", "facility1", "Bad Client")

    assert len(reservations_bewteen_dates) == 4

def test_db_get_reservations_between_dates():
    '''
    Test db_get_reservations_between_dates function output
    '''
    reservations_bewteen_dates = database_reservations.db_get_reservations_between_dates("2022-05-10",
        "2022-05-15", "facility1")

    assert len(reservations_bewteen_dates) == 8

def test_db_get_holds_between_dates():
    '''
    Test db_get_reservations_between_dates function output
    '''
    reservations_bewteen_dates = database_reservations.db_get_holds_between_dates("2022-05-10",
        "2022-05-31")

    assert len(reservations_bewteen_dates) == 2


def test_db_get_transactions_between_dates():
    '''
    Test db_get_transactions_between_dates function output
    '''
    transactions_bewteen_dates = database_reservations.db_get_transactions_between_dates("2022-05-05",
        "2022-05-15", "facility1")

    assert len(transactions_bewteen_dates) == 14


def test_db_add_reservation():
    '''
    Test db_add_reservation function
    '''
    # Use test data
    database_reservations.use_test_db()

    # Number of previous reservations for date
    prev_res = len(database_reservations.db_get_reservations_between_dates("2022-05-06",
        "2022-05-06", "facility1"))

    database_reservations.db_add_reservation('x1', 'facility1', 0, '2022-05-06', 'workshop',
        'test', 9, 9.5, 'on')

    # Number of new reservations for date
    new_res = len(database_reservations.db_get_reservations_between_dates("2022-05-06",
        "2022-05-06", "facility1"))
    
    # Restore original data
    database_reservations.restore_db_from_backup()

    assert new_res == prev_res + 1


def test_db_get_latest_id():
    '''
    Test function to get max of reservation_id
    '''
    latest_id = database_reservations.db_get_latest_id()
    assert latest_id == 14


def test_db_add_transaction():
    '''
    Test db_add_transaction function
    '''
    # Use test data
    database_reservations.use_test_db()

    # Number of previous transactions for date
    prev_trans = len(database_reservations.db_get_transactions_between_dates(datetime.today().strftime("%Y-%m-%d"),
        datetime.today().strftime("%Y-%m-%d"), 'facility1'))

    database_reservations.db_add_transaction('res1-1', 'remaining balance', 99, datetime.now(), 'admin1', '1')

    # Number of new transactions for date
    new_trans = len(database_reservations.db_get_transactions_between_dates(datetime.today().strftime("%Y-%m-%d"),
        datetime.today().strftime("%Y-%m-%d"), 'facility1'))

    # Restore original data
    database_reservations.restore_db_from_backup()

    assert new_trans == prev_trans + 1


def test_db_cancel_reservation():
    '''
    Test db_cancel_reservation function
    '''
    # Use test data
    database_reservations.use_test_db()
    
    # Number of previous reservations for date
    prev_res = len(database_reservations.db_get_reservations_between_dates("2022-05-10",
        "2022-05-10", "facility1"))

    database_reservations.db_cancel_reservation(5)

    # Number of new reservations for date
    new_res = len(database_reservations.db_get_reservations_between_dates("2022-05-10",
        "2022-05-10", "facility1"))
    
    # Restore original data
    database_reservations.restore_db_from_backup()

    assert new_res == prev_res - 1


def test_db_get_reservations_for_date_and_time():
    '''
    Test db_cancel_reservation function
    '''
    reservations_date_time = database_reservations.db_get_reservations_for_date_and_time('2022-05-10', 9)

    assert len(reservations_date_time) == 3