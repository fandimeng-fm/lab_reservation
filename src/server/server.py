# Application that provides the functionality of the reservation system through
# a (pragmatic) RESTful API
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: uvicorn server:app --reload

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import helpers.reservation_functions as reservation_functions
import helpers.user_functions as user_functions
from PyInquirer import prompt
from examples import custom_style_2

# API launch and initial prompt
app = FastAPI()
answers = prompt({
    'type': 'list',
    'name': 'choice',
    'message': 'Would you like the system to allow client sign-in? Select and press enter: ',
    'choices': [
        "Yes",
        "No"
    ]}, style=custom_style_2)
if answers['choice'] == "Yes":
    allowed = True
else:
    allowed = False

# ReservationRequest class for POST request
class ReservationRequest(BaseModel):
    facility: str
    user_id: str
    reservation_item: str
    reservation_client_id: str
    reservation_date: str
    reservation_time: float
    duration: float

# HoldRequest class for holds POST request
class HoldRequest(BaseModel):
    facility: str
    user_id: str
    hold_item: str
    hold_client_id: str
    hold_date: str
    hold_time: float
    duration: float

# User class for POST request
class User(BaseModel):
    user_id: str
    password: str
    role: str

@app.get("/pref")
async def return_pref():
    return {'pref': allowed}


@app.post("/reservations")
async def create_reservation(reservation_request: ReservationRequest):
    '''
    Make reservation using reservation class.
    For documentation: https://fastapi.tiangolo.com/tutorial/body/

    Post request will have the following structure (similar to ReservationRequest
    class above):
    {
        "facility": "string",
        "user_id": "string",
        "reservation_item": "string",
        "reservation_client_id": "string",
        "reservation_date": "2022-04-28",
        "reservation_time": 9.0,
        "duration": 1.0
    }

    After running the make_reservation function, will return:
    {
        'code': 200,
        'message': 'Reservation was successful!',
        'reservation_id': reservation_id
    }
    '''

    # Call make_reservation to create reservation based on request
    reservation = reservation_functions.make_reservation(reservation_request)

    # Return reservation
    return reservation


@app.get("/reservations")
async def get_reservations(start_date: str = "", end_date: str = "", facility: str = "facility1", customer_id: Optional[str] = None):
    '''
    Get reservations. Query parameters:
    - start_date (required)
    - end_date (required)
    - facility (required)
    - customer_id (optional)
    For documentation: https://fastapi.tiangolo.com/tutorial/query-params/

    Returns list of strings with information about reservations between two dates and customer_id
    (if applicable):
    {
        'code': 200,
        'data': report
    }
    '''

    # Get reservations given parameters
    reservations = reservation_functions.view_reservations(start_date, end_date, facility, customer_id,)

    # Return transactions informartiion
    return reservations


@app.post("/holds")
async def create_hold(hold_request: HoldRequest):
    '''
    Make hold using reservation class.
    For documentation: https://fastapi.tiangolo.com/tutorial/body/

    Post request will have the following structure (similar to HoldRequest
    class above):
    {
        "user_id": "string",
        "hold_item": "string",
        "hold_client_id": "string",
        "hold_date": "2022-04-28",
        "hold_time": 9.0,
        "duration": 1.0
    }

    After running the make_hold function, will return:
    {
        'code': 200,
        'message': 'Hold was successful!',
        'reservation_id': reservation_id
    }
    '''

    # Call make_reservation to create reservation based on request
    hold = reservation_functions.make_hold(hold_request)

    # Return reservation
    return hold


@app.get("/reservations/holds")
async def get_reservations(start_date: str = "", end_date: str = ""):
    '''
    Get reservations. Query parameters:
    - start_date (required)
    - end_date (required)
    For documentation: https://fastapi.tiangolo.com/tutorial/query-params/

    Returns list of strings with information about reservations between two dates and customer_id
    (if applicable):
    {
        'code': 200,
        'data': report
    }
    '''

    # Get reservations given parameters
    holds = reservation_functions.view_holds(start_date, end_date)

    # Return transactions informartion
    return holds


@app.get("/reservations/cancel/{reservation_id}")
async def cancel_reservation(reservation_id): #, facility: str = "facility1"):
    '''
    Cancel reservation based on reservation_id. For
    documentation: https://fastapi.tiangolo.com/tutorial/path-params/

    Will return a dictionary with all outstanding reservations, including cancelled one
    which will be flagged as such:
    {
        'code': 200,
        'data': d_reservations
    }
    '''

    # Call cancel_reservation to cancel reservation based on request
    cancellation = reservation_functions.cancel_reservation(reservation_id)

    # Return cancellation
    return cancellation


@app.get("/transactions")
async def get_transactions():
    '''
    Returns list of strings with information about all transactions:
    {
        'code': 200,
        'data': report
    }
    '''

    # Get transactions given parameters
    transactions = reservation_functions.view_all_transactions()

    # Return transactions information
    return transactions


@app.get("/transactions/{user_id}")
async def get_transactions(user_id: str):
    '''
    Returns list of strings with information about all transactions:
    {
        'code': 200,
        'data': report
    }
    '''

    # Get transactions given parameters
    transactions = reservation_functions.view_all_transactions(user_id)

    # Return transactions information
    return transactions


@app.get("/users")
async def validate_user(user_id: str = "", password: str = ""):
    '''
    Check if user_id is associated with a valid user in the system.

    Query parameters: 
        - user_id (required)
        - password (required)
    For documentation: https://fastapi.tiangolo.com/tutorial/query-params/

    Returns
    {
        'message': '{user_id} is a {role}",
        'data': role
    }
    '''

    return user_functions.validate_user(user_id, password, allowed)


@app.post("/users")
async def add_user(user: User):
    '''
    Add a users References User class above.
    For documentation: https://fastapi.tiangolo.com/tutorial/body/

    Post request will have the following structure (similar to User
    class above):
    {
        "user_id": "string",
        "password": "string",
        "role": "string",
    }

    After running the add_user function, will return:
    {
        'code': 200,
        'message': '{user_id} has been successfully added as a {role}',
    }
    '''
    return user_functions.add_user(user.user_id, user.password, user.role)


@app.delete('/users/{user_id}')
async def remove_user(user_id: str = ""):
    '''
    Remove user_id from Users table in database given user ID in path.
    For documentation: https://fastapi.tiangolo.com/tutorial/path-params/

    After running the remove_user function, will return:
    {
        'code': 200,
        'message': "{user_id} has been successfully removed as a user."
    }
    '''

    return user_functions.remove_user(user_id)


@app.put('/users/{user_id}')
async def update_user(user_id: str, user: User):
    '''
    Update a user given user ID in path.
    For documentation: https://fastapi.tiangolo.com/tutorial/path-params/

    After running the update_user function, will return:
    {
        'code': 200,
        'message': "{user_id} has been updated to {role}."
    }
    '''
    if user.user_id and user.user_id != user_id:
        return user_functions.update_user_id(user_id, user.user_id)
    elif user.password:
        return user_functions.update_user_password(user_id, user.password)
    elif user.role:
        return user_functions.update_user_role(user_id, user.role)


@app.get('/users/activate/{user_id}')
async def activate_user(user_id: str):
    '''
    Activate a previously-deactivated user based on user ID in path.
    For documentation: https://fastapi.tiangolo.com/tutorial/path-params/

    After running the activate_user function, will return:
    {
        'code': 200,
        'message': "{user_id} successfully activated."
    }
    '''
    return user_functions.activate_user(user_id)


@app.get('/users/deactivate/{user_id}')
async def deactivate_user(user_id: str):
    '''
    Deactivate a user based on user ID in path.
    For documentation: https://fastapi.tiangolo.com/tutorial/path-params/

    After running the deactivate_user function, will return:
    {
        'code': 200,
        'message': "{user_id} successfully deactivated."
    }
    '''
    return user_functions.deactivate_user(user_id)


@app.get('/users/all')
async def show_users():
    '''
    Get list of users and their respective roles.

    After running the show_users function, will return table of users and roles:
    {
        'code': 200,
        'data': table
    }
    '''
    return user_functions.show_users()


@app.get('/clients')
async def show_clients():
    '''
    Get list of all clients.

    After running the show_clients function, will return table of user IDs, roles, balances, and status:
    {
        'code': 200,
        'data': table
    }
    '''
    return user_functions.show_clients()


@app.get('/clients/{user_id}')
async def show_clients(user_id: str):
    '''
    Get information for specific client given user ID in path.
    For documentation: https://fastapi.tiangolo.com/tutorial/path-params/

    After running the show_client function, will return one-row table of user ID, role, balance, and status:
    {
        'code': 200,
        'data': table
    }
    '''
    return user_functions.show_client(user_id)


@app.get('/balance')
async def balance(user_id: str = "", amount: int = 0):
    '''
    Show user's balance if amount not provided. Add to user's balance if amount provided.

    Query parameters: 
        - user_id
        - amount
    For documentation: https://fastapi.tiangolo.com/tutorial/query-params/

    After running the add_balance function, will return:
    {
        'code': 200,
        'message': "Fund successfully added to {user_id}'s account. Current balance is {balance}."
    }

    After running the show_balance function, will return:
    {
        'code': 200,
        'message': "Current balance is {balance}."
    }
    '''

    if amount != 0:
        # To add balance
        return user_functions.add_balance(user_id, amount)
    else:
        # To show balance
        return user_functions.show_balance(user_id)