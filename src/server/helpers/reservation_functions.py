# Reservation functions for reservations_API.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng

from datetime import date, timedelta, datetime
import json, os
from fastapi import HTTPException
import database.database_reservations as database_reservations
import database.database_users as database_users

def get_booked_machines(str_reservation_date, reservation_time):
    '''
    Determines machines booked at a date and reservation time.
    Returns the list of machines reserved for that date and time
    '''

    # Get current filled slots on this date:
    current_reservations = database_reservations.db_get_reservations_for_date_and_time(str_reservation_date, reservation_time)
    # Convert resources booked into list
    booked_machines = [res['resource'] for res in current_reservations]
                
    return booked_machines


def calculate_booking_costs(reservation_date, reservation_item, duration):
    '''
    Calculate booking costs based on reservation date and item
    '''

    # Calculate discount based on dates
    discount = 0
    if (reservation_date - date.today()).days >= 14:
        discount = 0.25

    # Total amount of the reservation
    d_cost = {
        "workshop": 99, 
        "microvac": 1000, 
        "irradiator": 2220, 
        "extruder": 600, 
        "crusher": 20000, 
        "harvester": 8800
    }

    payment_amount = d_cost[reservation_item] * (1 - discount) * duration
    
    return payment_amount

def check_active_user(user_id):
    '''
    Check if user is active.
    '''
    active = database_users.db_is_user_active(user_id)

    if not active:
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not an active user."
        )

    return active

def check_sufficient_balance(reservation_date, reservation_item, duration, user_id):
    '''
    Check if user has sufficient balance in account to cover the down payment.
    '''

    cost = calculate_booking_costs(reservation_date, reservation_item, duration)
    balance = database_users.db_get_balance(user_id)

    if balance >= cost:
        return True
    else:
        raise HTTPException(
            status_code=400,
            detail= f'Insufficient balance. Cost is {cost} and balance is {balance} and the user ID is {user_id}'
        )

def check_machine_availability(str_reservation_date, reservation_time, reservation_item):
    '''
    Check if there is availability on the machine requested
    '''

    # Get current filled slots on this date:
    current_reservations = get_booked_machines(str_reservation_date, reservation_time)

    # Each machine has own reservation constraint:
    d_reservation_constraints = {
        "workshop": 4,
        "microvac": 2,
        "irradiator": 2,
        "extruder": 2,
        "crusher": 1,
        "harvester": 1
    }

    if current_reservations.count(reservation_item) < d_reservation_constraints[reservation_item]:
        return True
    # If machines are booked
    else:
        raise HTTPException(
            status_code=400,
            detail='Machine booked for that time.'
        )


def check_booking_requirements(user_id, reservation_date, reservation_item, duration, str_reservation_date, reservation_time):
    '''
    Check if reservation request meets all booking requirements.
    '''
    user_active = check_active_user(user_id)
    sufficient_balance = check_sufficient_balance(reservation_date, reservation_item, duration, user_id)
    machine_available = check_machine_availability(str_reservation_date, reservation_time, reservation_item)

    return user_active and sufficient_balance and machine_available


def add_reservation_to_db(user_id, reservation_date, reservation_id, facility, reservation_item,
    client_id, reservation_time, duration, status):
    '''
    Add valid reservation to dictionary of reservations.
    Returns the updated dictionary.
    '''

    # Calculate payment amount
    payment_amount = calculate_booking_costs(reservation_date, reservation_item, duration)

    # Calculate end time
    end_time = reservation_time + duration

    # Add reservation to DB
    database_reservations.db_add_reservation(reservation_id, facility, 0, reservation_date, reservation_item, 
        client_id, reservation_time, end_time, status)

    if status == 'on':
        #Deduct reservation cost from client balance - only for reservations and validated users
        database_users.db_update_balance(user_id, -payment_amount)

        # Add payment transaction - only for reservations
        transaction_id = str(reservation_id) + '-t1'
        database_reservations.db_add_transaction(transaction_id, 'payment', payment_amount,
            datetime.now(), user_id, reservation_id)


def make_reservation(reservation_request):
    '''
    Make a reservation given reservation_request class
    '''

    # Get details from reservation request
    facility = reservation_request.facility
    user_id = reservation_request.reservation_client_id
    str_reservation_date = reservation_request.reservation_date
    reservation_date = datetime.strptime(str_reservation_date, '%Y-%m-%d').date()
    reservation_time = reservation_request.reservation_time    
    reservation_item = reservation_request.reservation_item
    client_id = reservation_request.reservation_client_id
    duration = reservation_request.duration
    status = 'on'

    valid_reservation = check_booking_requirements(user_id, reservation_date, reservation_item, duration,
                                                   str_reservation_date, reservation_time)
    if valid_reservation:
        # Make unique reservation id
        reservation_id = database_reservations.db_get_latest_id() + 1
        # Add to reservations database
        add_reservation_to_db(user_id, reservation_date, reservation_id, facility,
            reservation_item, client_id, reservation_time, duration, status)

        return {'message': 'Reservation was successful! ',
                 'reservation_id': reservation_id}
    else:
        raise HTTPException(
            status_code=400, 
            detail='This is not a valid reservation request. '
            )


def make_hold(hold_request):
    '''
    Make a reservation given reservation_request class
    '''

    # Get details from reservation request
    facility = hold_request.facility
    user_id = hold_request.user_id
    str_hold_date = hold_request.hold_date
    hold_date = datetime.strptime(str_hold_date, '%Y-%m-%d').date()
    hold_time = hold_request.hold_time    
    hold_item = hold_request.hold_item
    client_id = hold_request.hold_client_id
    duration = hold_request.duration
    status = 'hold'

    valid_hold = check_machine_availability(str_hold_date, hold_time,
        hold_item)

    if valid_hold:
        # Make unique reservation id
        reservation_id = database_reservations.db_get_latest_id() + 1
        # Add to reservations database
        add_reservation_to_db(user_id, hold_date, reservation_id, facility,
            hold_item, client_id, hold_time, duration, status)

        return { 'message': 'Hold was successful! ',
                 'reservation_id': reservation_id}
    else:
        raise HTTPException(
            status_code=400, 
            detail='This is not a valid hold request. '
            )


def cancel_reservation(reservation_id):
    '''
    Cancel a reservation given reservation_request class
    '''

    today = date.today()
    
    # Validate reservation_id:
    valid_id = database_reservations.db_validate_reservation(reservation_id)
    if valid_id:
        active_reservation = database_reservations.db_validate_active_reservation(reservation_id)

        if active_reservation:
            reservation = database_reservations.db_get_reservations_for_id(reservation_id)
            database_reservations.db_cancel_reservation(reservation_id)

            # Add refund to transactions
            # Calculate refund
            refund = 0
            booking_date = datetime.strptime(reservation['reservation_date'], '%Y-%m-%d').date()

            if (booking_date - today).days > 7:
                refund = 0.75
            elif (booking_date - today).days > 2:
                refund = 0.5

            # Add transaction
            transaction_id = str(reservation_id) + '-t2'
            refund_amount = database_reservations.db_get_payment_amount_for_id(reservation_id) * refund
            user_id = database_reservations.db_get_user_for_id(reservation_id)
            database_users.db_update_balance(user_id, refund_amount)
            database_reservations.db_add_transaction(transaction_id, 'refund', refund_amount,
                datetime.now(), user_id, reservation_id)

            # Return successful cancellation
            return {'message': 'Cancellation was successful!'}
        else:
            # else check if held by remote manager
            active_hold = database_reservations.db_validate_hold(reservation_id)

            if active_hold:
                database_reservations.db_cancel_reservation(reservation_id)
                return {'message': 'Hold cancellation was successful!'}

            else:
                # Else if correct reservation found and already cancelled
                raise HTTPException(
                    status_code=400, 
                    detail='This reservation is already cancelled.'
                    )
    else:
        # If reservation not found
        raise HTTPException(
            status_code=400, 
            detail='That reservation ID does not exist in our system.'
        )
        

def view_reservations(date_start, date_end, facility, client_id):
    '''
    View reservations for date range and if specified, client_id
    '''
    if client_id is None:
        reservations_db = database_reservations.db_get_reservations_between_dates(
            date_start, date_end, facility)
    else:
        reservations_db = database_reservations.db_get_reservations_between_dates_and_client(
            date_start, date_end, facility, client_id)

    # Output reservations
    report = f"All reservations for date range {date_start} to {date_end}"
    if client_id:
        report += f" for client {client_id}: \n"
    else:
        report += f": \n"

    # Go through each reservation for a date in the dictionary
    for reservation in reservations_db:
        # Add reservation to report
        report += create_report(reservation)

    # Return report
    return {'data': report, 'csv_data': reservations_db}

def view_holds(date_start = "", date_end = ""):
    '''
    View holds for date range and if specified, client_id
    '''
    
    holds_db = database_reservations.db_get_holds_between_dates(
        date_start, date_end)
    
    # Output reservations
    if date_start and date_end:
        report = f"All holds for date range {date_start} to {date_end}"
    else:
        report = f"All holds"
    report += f": \n"

    # Go through each reservation for a date in the dictionary
    for hold in holds_db:
        # Add reservation to report
        report += create_report(hold)

    # Return report
    return {'data': report, 'csv_data': holds_db}

def view_transactions(date_start, date_end, facility):
    '''
    View transactions for date range
    '''

    # Output transactions
    report = f"All transactions for date range {date_start} to {date_end}: \n"

    # Go through each reservation for a date in the 
    transactions_db = database_reservations.db_get_transactions_between_dates(date_start, date_end, facility)
    for transaction in transactions_db:
        reservation_id = transaction['reservation_id']
        reservation = database_reservations.db_get_reservations_for_id(reservation_id)
        # Report transactions
        if transaction['transaction_type'] == 'payment':
            report += create_report(reservation)
        report += f'- {transaction["transaction_type"].capitalize()}: {transaction["transaction_amount"]}\n'
        report += f'- {transaction["transaction_type"].capitalize()}: {transaction["transaction_amount"]}\n'
    return {'data': report}

def view_all_transactions(user_id=None):
    '''
    View all transactions
    '''

    # Output transactions
    if user_id:
        report = f"All transactions for user {user_id}: \n"
        transactions_db = database_reservations.db_print_all_transactions_for_id(user_id)
    else:
        report = f"All transactions: \n"
        transactions_db = database_reservations.db_print_all_transactions()

    # Go through each reservation for a date in the 
    for transaction in transactions_db:
        reservation_id = transaction['reservation_id']
        reservation = database_reservations.db_get_reservations_for_id(reservation_id)
        # Report transactions
        if transaction['transaction_type'] == 'payment':
            report += create_report(reservation)
        report += f'- {transaction["transaction_type"].capitalize()}: {transaction["transaction_amount"]}\n'
    return {'data': report}


def create_report(reservation):
    '''
    Function to prepare report 
    '''
    report = (f'\nReservation ID: {reservation["reservation_id"]}\n'
        f'- Reserved Item: {reservation["resource"]}\n'
        f'- Booked Date: {reservation["reservation_date"]}\n'
        f'- Booked Time: {reservation["start_time"]}\n'
        f'- Booked by Client ID: {reservation["client_id"]}\n'
    )
    return report

