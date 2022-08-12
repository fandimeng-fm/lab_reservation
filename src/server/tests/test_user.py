# Test file for reservations_API.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: pytest

import requests
import database.database_helpers as database_helpers

def test_validate_user_real():
    '''
    Test validate_user on real user_id
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = 'patrick'
    password = 'patrickpassword'

    url = f"http://127.0.0.1:8000/users?user_id={user_id}&password={password}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 200
    assert j["data"] == 'scheduler'


def test_validate_user_wrong_password():
    '''
    Test validate_user with incorrect password
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = 'peter'
    password = 'bobpassword'

    url = f"http://127.0.0.1:8000/users?user_id={user_id}&password={password}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 401
    assert j["detail"] == 'Incorrect credentials.'

def test_validate_user_nonexist():
    '''
    Test validate_user with user that's not in the system
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = 'bob'
    password = 'bobpassword'

    url = f"http://127.0.0.1:8000/users?user_id={user_id}&password={password}"
    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 400
    assert j["detail"] == 'That user ID does not exist in our system.'


def test_add_user_new():
    '''
    Test adding a new user.
    '''
    # Use test data
    database_helpers.use_test_db()

    user = {'user_id': 'new_user', 'password': 'password1234', 'role': 'scheduler'}

    url = "http://127.0.0.1:8000/users"
    response = requests.post(url, json=user)

    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 200
    assert j['message'] == 'new_user has been successfully added as a scheduler.'


def test_add_user_exists():
    '''
    Test adding a user that already exists.
    '''
    # Use test data
    database_helpers.use_test_db()

    user = {'user_id': 'peter', 'password': 'peterpassword', 'role':'scheduler'}

    url = "http://127.0.0.1:8000/users"
    response = requests.post(url, json=user)

    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 400
    assert j['detail']  == 'peter is already a user.'


def test_remove_user_scheduler():
    '''
    Test removing a user whose role is scheduler.
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = 'peter'

    url = f"http://127.0.0.1:8000/users/{user_id}"
    response = requests.delete(url)

    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 200
    assert j['message'] == 'peter has been successfully removed as a user.'


def test_remove_user_admins():
    '''
    Test removing last two admins. First removal is valid. Second removal should raise error.
    '''
    # Use test data
    database_helpers.use_test_db()

    id_1 = 'admin1'
    id_2 = 'admin2'

    url_1 = f"http://127.0.0.1:8000/users/{id_1}"
    response_1 = requests.delete(url_1)

    j_1 = response_1.json()

    url_2 = f"http://127.0.0.1:8000/users/{id_2}"
    response_2 = requests.delete(url_2)

    j_2 = response_2.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response_1.status_code == 200
    assert response_2.status_code == 400
    assert j_1['message'] == "admin1 has been successfully removed as a user."
    assert j_2['detail'] == "admin2 is the final admin and cannot be removed."


def test_update_user_upgrade_scheduler():
    '''
    Test updating role for a user from scheduler to admin
    '''
    # Use test data
    database_helpers.use_test_db()

    user = {'user_id': 'peter', 'password': '', 'role':'admin'}

    url = "http://127.0.0.1:8000/users/peter"
    response = requests.put(url, json=user)

    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 200
    assert j['message'] == 'peter has been updated to admin.'


def test_update_user_downgrade_admins():
    '''
    Test updating role for a user from admin to scheduler. First update is valid. Second update should raise error.
    '''
    # Use test data
    database_helpers.use_test_db()

    user_1 = {'user_id': 'admin1', 'password': '', 'role':'scheduler'}
    user_2 = {'user_id': 'admin2', 'password': '', 'role':'scheduler'}

    url = "http://127.0.0.1:8000/users"
    response_1 = requests.put(url + '/admin1', json=user_1)
    response_2 = requests.put(url + '/admin2', json=user_2)

    j_1 = response_1.json()
    j_2 = response_2.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response_1.status_code == 200
    assert response_2.status_code == 400
    assert j_1['message'] == "admin1 has been updated to scheduler."
    assert j_2['detail'] == "admin2 is the final admin and cannot be downgraded to scheduler."

def test_update_user_id_invalid():
    database_helpers.use_test_db()
    user_1 = {'user_id': 'client2', 'password': '', 'role':''}

    url = f"http://127.0.0.1:8000/users/client1"

    response = requests.put(url, json=user_1)
    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 400
    assert j['detail'] == "User ID client2 is occupied by another user."

def test_update_user_id_valid():
    database_helpers.use_test_db()
    old_user_id = "client1"
    new_user_id = "client"

    user_1 = {'user_id': new_user_id, 'password': '', 'role':''}

    url = f"http://127.0.0.1:8000/users/{old_user_id}"

    response = requests.put(url, json=user_1)
    j = response.json()

    assert response.status_code == 200
    assert j['message'] == f"Update successful! Old user id: {old_user_id} => New user_id: {new_user_id}."

    url = f"http://127.0.0.1:8000/clients/{old_user_id}"

    response = requests.get(url)
    j = response.json()

    assert response.status_code == 400
    assert j['detail'] == f"{old_user_id} is not a user."

    url = f"http://127.0.0.1:8000/clients/{new_user_id}"

    response = requests.get(url)
    j = response.json()

    assert response.status_code == 200
    assert j['data'] == \
    f'''User ID         Role       Balance    Active    
------------    ---------- ---------- ----------
client          client     100        yes       
'''

    # Restore original data
    database_helpers.restore_db_from_backup()

def test_update_user_password():
    database_helpers.use_test_db()
    user_id = "client1"
    old_password = "client1pw"
    new_password = "client1password"
    user_1 = {'user_id': '', 'password': new_password, 'role':''}

    url = f"http://127.0.0.1:8000/users/{user_id}"

    response = requests.put(url, json=user_1)
    j = response.json()

    assert response.status_code == 200
    assert j['message'] == f"Successfully updated User {user_id}'s password."

    url = f"http://127.0.0.1:8000/users?user_id={user_id}&password={old_password}"
    response = requests.get(url)
    j = response.json()

    assert response.status_code == 401
    assert j["detail"] == 'Incorrect credentials.'

    url = f"http://127.0.0.1:8000/users?user_id={user_id}&password={new_password}"
    response = requests.get(url)
    j = response.json()

    assert response.status_code == 200
    assert j["data"] == 'client'

    # Restore original data
    database_helpers.restore_db_from_backup()

def test_activate_user_bad():
    '''
    Test activate function
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = "client1"
    url = f"http://127.0.0.1:8000/users/activate/{user_id}"

    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 400
    assert j["detail"] == f"{user_id} is already active."

def test_deactivate_and_deactivate_user():
    '''
    Test deactivate function
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = "client1"
    url = f"http://127.0.0.1:8000/users/deactivate/{user_id}"

    response = requests.get(url)
    j = response.json()

    assert response.status_code == 200
    assert j["message"] == f"{user_id} successfully deactivated."

    response = requests.get(url)
    j = response.json()

    assert response.status_code == 400
    assert j["detail"] == f"{user_id} is already deactivated."

    # Restore original data
    database_helpers.restore_db_from_backup()

def test_deactivate_and_activate_user():
    '''
    Test deactivate and activate function
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = "client1"
    url = f"http://127.0.0.1:8000/users/deactivate/{user_id}"

    response = requests.get(url)
    j = response.json()

    assert response.status_code == 200
    assert j["message"] == f"{user_id} successfully deactivated."

    url = f"http://127.0.0.1:8000/users/activate/{user_id}"

    response = requests.get(url)
    j = response.json()

    assert response.status_code == 200
    assert j["message"] == f"{user_id} successfully activated."

    # Restore original data
    database_helpers.restore_db_from_backup()

def test_show_users():
    '''
    Test show_users function
    '''
    # Use test data
    database_helpers.use_test_db()

    url = f"http://127.0.0.1:8000/users/all"

    response = requests.get(url)
    j = response.json()

    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 200
    assert j['data'].count("admin") == 4

def test_show_clients():
    '''
    Test show_users function
    '''
    # Use test data
    database_helpers.use_test_db()

    url = f"http://127.0.0.1:8000/clients"
    response = requests.get(url)
    j = response.json()
    # Restore original data
    database_helpers.restore_db_from_backup()

    assert response.status_code == 200
    assert j['data'].count("client") == 4

def test_add_and_show_balance():
    '''
    Test add_balance function
    '''
    # Use test data
    database_helpers.use_test_db()

    user_id = 'client1'
    amount = 10000

    url = f"http://127.0.0.1:8000/balance?user_id={user_id}&amount={amount}"
    response = requests.get(url)
    j = response.json()

    assert response.status_code == 200
    assert j['message'] == f"Fund successfully added to {user_id}'s account. Current balance is 10100." 

    url = f"http://127.0.0.1:8000/balance?user_id={user_id}"
    response = requests.get(url)
    j = response.json()


    assert response.status_code == 200
    assert j['message'] == f"Current balance is 10100."

    # Restore original data
    database_helpers.restore_db_from_backup()