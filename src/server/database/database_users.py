# Function to interact with database:
# specifically the `users` table`
# which contains user information (admins and schedulers)
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng

import hashlib
from database.database_helpers import *


def db_user_exists(user_id):
    '''
    Function to check if a user_id exists in the database 
    Input: user_id
    Output: returns True if the user exists, False otherwise
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")

    # if a row returns from query, the user is valid
    if cursor.fetchone():
        return True
    else:
        return False

def db_validate_user(user_id, password):
    '''
    Function to validate a user 
    Input: user_id
    Output: returns True if the user is a valid user, False otherwise
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")

    # if a row returns from query, the user is valid
    user = cursor.fetchone()
    hash = user["hash"]
    salt = user["salt"]

    # Create hash to validate user
    new_hash = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=100000
    )

    return new_hash == hash


def db_get_user_role(user_id):
    '''
    Function to retrieve user's role, to be called after validating user
    to know if user is scheduler, admin, client, or remote manager 
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")

    # get the role from the one and only result
    role = cursor.fetchone()["role"]
    return role


def db_show_users():
    '''
    Function to retrieve all users in the system and their respective roles
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query and fetch all users
    cursor.execute(f"SELECT * FROM users")
    results = cursor.fetchall()

    return results

def db_show_clients():
    '''
    Function to retrieve only clients in the system and their roles and balances
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query and fetch all results
    cursor.execute(f"SELECT * FROM users WHERE role = 'client'")
    results = cursor.fetchall()

    return results

def db_show_client(user_id):
    '''
    Function to retrieve only clients in the system and their roles and balances
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute query and fetch one result
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    results = cursor.fetchone()

    return results


def db_count_admins():
    '''
    Function to check how many admins exist, need at least 1 
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Count admin query
    cursor.execute(f"SELECT Count() FROM users WHERE role = 'admin'")
    admins = cursor.fetchone()[0]

    return admins


def db_add_user(user_id, role, salt, hash):
    '''
    Function to add a user to the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
        [user_id, role, 0, 'yes', salt, hash])

    # Commit and close
    conn.commit()
    conn.close()


def db_remove_user(user_id):
    '''
    Function to delete a user from the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute remove query
    cursor.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")

    # Commit and close
    conn.commit()
    conn.close()


def db_update_user_role(user_id, role):
    '''
    Function to update a user's role to the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"UPDATE users SET role = '{role}' WHERE user_id = '{user_id}'")

    # Commit and close
    conn.commit()
    conn.close()

def db_update_user_password(user_id, salt, hash):
    '''
    Function to update a user's password to the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"UPDATE users SET salt = ?, hash = ? WHERE user_id = '{user_id}'", [salt, hash])

    # Commit and close
    conn.commit()
    conn.close()

def db_update_user_id(user_id, new_user_id):
    '''
    Function to update a user's role to the database
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    user = cursor.fetchone()
    cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", 
        [new_user_id, user['role'], user['balance'], user['active'], user['salt'], user['hash']])
    cursor.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")

    # Commit and close
    conn.commit()
    conn.close()

def db_is_user_active(user_id):
    '''
    Function to check if a user is active
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    active = cursor.fetchone()['active']

    return active == "yes"

def db_activate_user(user_id):
    '''
    Function to activate a user
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"UPDATE users SET active = 'yes' WHERE user_id = '{user_id}'")

    conn.commit()
    conn.close()

def db_deactivate_user(user_id):
    '''
    Function to deactivate a user
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"UPDATE users SET active = 'no' WHERE user_id = '{user_id}'")

    conn.commit()
    conn.close()

def db_get_balance(user_id):
    '''
    Function to get balance for a user's account
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute insert query
    cursor.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    balance = cursor.fetchone()['balance']

    return balance

def db_update_balance(user_id, amount):
    '''
    Function to add balance to a user's account
    '''
    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor()

    if int(amount) > 0:
    # Execute insert query
        cursor.execute(f"UPDATE users SET balance = balance + {amount} WHERE user_id = '{user_id}'")
    else:
        cursor.execute(f"UPDATE users SET balance = balance - {abs(amount)} WHERE user_id = '{user_id}'")

    conn.commit()
    conn.close()