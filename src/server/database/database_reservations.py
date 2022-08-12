# Function to interact with database:
# specifically the `reserbations` and `transactions` table
# reservations: with reservations data
# transactions: with transactions data for each reservation
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng

from database.database_helpers import *

def db_add_reservation(reservation_id, facility, recurring_number, reservation_date, resource, 
    client_id, start_time, end_time, status):
    '''
    Function to add a reservation to the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [reservation_id, facility, recurring_number, reservation_date, resource, client_id,
        start_time, end_time, status])

    # Commit and close
    conn.commit()
    conn.close()


def db_add_transaction(transaction_id, transaction_type, transaction_amount, transaction_timestamp, 
    user_id, reservation_id):
    '''
    Function to add a transaction to the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?)",
        [transaction_id, transaction_type, transaction_amount, transaction_timestamp, 
        user_id, reservation_id])

    # Commit and close
    conn.commit()
    conn.close()

def db_validate_reservation(reservation_id):
    '''
    Function to validate a reservation 
    Input: reservation_id
    Output: returns True if the user is a valid user, False otherwise
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM reservations WHERE reservation_id = {reservation_id}")

    # if a row returns from query, the user is valid
    if cursor.fetchone():
        return True
    else:
        return False


def db_validate_active_reservation(reservation_id):
    '''
    Function to validate a reservation 
    Input: reservation_id
    Output: returns True if the user is a valid user, False otherwise
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM reservations WHERE reservation_id = {reservation_id} "+
        f"AND status = 'on'")

    # if a row returns from query, the user is valid
    if cursor.fetchone():
        return True
    else:
        return False

def db_validate_hold(reservation_id):
    '''
    Function to validate a hold 
    Input: reservation_id
    Output: returns True if reservation is a hold, False otherwise
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM reservations WHERE reservation_id = {reservation_id} "+
        f"AND status = 'hold'")

    # if a row returns from query, the user is valid
    if cursor.fetchone():
        return True
    else:
        return False


def db_cancel_reservation(reservation_id):
    '''
    Function to connect to database
    '''
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query
    sql_query = f"UPDATE reservations SET status = 'off' WHERE reservation_id = {reservation_id}"
    cursor.execute(sql_query)

    # Commit and close
    conn.commit()
    conn.close()



def db_get_reservations_between_dates(start_date, end_date, facility):
    '''
    Function to get reservations between start and end dates
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT * FROM reservations WHERE reservation_date BETWEEN '{start_date}'"\
    f" AND '{end_date}' AND status = 'on' AND facility = '{facility}'"
    all_reservations = cursor.execute(query_reservations).fetchall()

    # Close
    conn.close()

    return all_reservations

def db_get_holds_between_dates(start_date, end_date):
    '''
    Function to get reservations between start and end dates
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    if start_date and end_date:
    # Get transactions between dates
        query_reservations = f"SELECT * FROM reservations WHERE reservation_date BETWEEN '{start_date}'"\
        f" AND '{end_date}' AND status = 'hold'"
    else:
        query_reservations = f"SELECT * FROM reservations WHERE status = 'hold'"
    all_holds = cursor.execute(query_reservations).fetchall()

    # Close
    conn.close()

    return all_holds


def db_get_reservations_between_dates_and_client(start_date, end_date, facility, client_id):
    '''
    Function to get reservations between start and end dates and for client_id
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT * FROM reservations WHERE reservation_date BETWEEN '{start_date}'"\
    f" AND '{end_date}' AND client_id = '{client_id}' AND status = 'on' AND facility = '{facility}'"
    all_reservations = cursor.execute(query_reservations).fetchall()

    # Close
    conn.close()

    return all_reservations


def db_get_transactions_between_dates(start_date, end_date, facility):
    '''
    Function to get transactions between start and end dates
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    end_date = end_date + "23:59:59.999999"
    query_transactions =f"SELECT * FROM transactions NATURAL JOIN "\
    f"(SELECT reservation_id FROM reservations WHERE facility = '{facility}')"\
    f"WHERE transaction_timestamp BETWEEN '{start_date}' AND '{end_date}'"
    all_transactions = cursor.execute(query_transactions).fetchall()

    # Close
    conn.close()

    return all_transactions


def db_get_reservations_for_date_and_time(reservation_date, reservation_time):
    '''
    Function to get reservations between start and end dates
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT * FROM reservations WHERE reservation_date = '{reservation_date}'"\
    f" AND (start_time >= {reservation_time} OR end_time <= {reservation_time})"
    all_reservations = cursor.execute(query_reservations).fetchall()

    # Close
    conn.close()

    return all_reservations



def db_get_reservations_for_id(reservation_id):
    '''
    Function to get reservations between start and end dates
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT * FROM reservations WHERE reservation_id = {reservation_id}"
    reservation = cursor.execute(query_reservations).fetchone()

    # Close
    conn.close()

    return reservation


def db_get_payment_amount_for_id(reservation_id):
    '''
    Function to get payment amount for a reservation
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT * FROM transactions WHERE reservation_id = {reservation_id}"\
    f" AND transaction_type = 'payment'"
    transaction = cursor.execute(query_reservations).fetchone()

    # Close
    conn.close()

    return float(transaction['transaction_amount'])

def db_get_user_for_id(reservation_id):
    '''
    Function to get client for a reservation
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT * FROM reservations WHERE reservation_id = {reservation_id}"
    reservation = cursor.execute(query_reservations).fetchone()

    # Close
    conn.close()

    return reservation['client_id']


def db_get_latest_id():
    '''
    Function to get reservations between start and end dates
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get transactions between dates
    query_reservations = f"SELECT MAX(reservation_id) AS reservation_id FROM reservations"
    reservation = cursor.execute(query_reservations).fetchone()

    # Close
    conn.close()

    return int(reservation['reservation_id'])


def db_print_all_transactions():
    '''
    Function to print all transactions in the 'transactions' table
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all transactions
    query_transactions = "SELECT * FROM transactions"
    all_transactions = cursor.execute(query_transactions).fetchall()

    # Close
    conn.close()

    return all_transactions

def db_print_all_transactions_for_id(user_id):
    '''
    Function to print all transactions in the 'transactions' table
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all transactions
    query_transactions = f"SELECT * FROM transactions WHERE user_id = '{user_id}'"
    all_transactions = cursor.execute(query_transactions).fetchall()

    # Close
    conn.close()

    return all_transactions