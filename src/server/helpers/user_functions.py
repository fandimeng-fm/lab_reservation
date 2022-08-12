# User functions for reservations_API.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng

from fastapi import HTTPException
import database.database_users as database_users
import os, hashlib


def validate_user(user_id, password, allowed):
    '''
    Validates user_id as a valid user. If it is valid, returns the role of the user.
    '''
    if database_users.db_user_exists(user_id):
        if  database_users.db_validate_user(user_id, password):
            role = database_users.db_get_user_role(user_id)
            if not allowed and role == "client":
                raise HTTPException(
                    status_code=400,
                    detail='Client sign-in disabled.'
                )
            return {'message': f"{user_id} is a {role}.", 'data': role}
        else:
            raise HTTPException(
                status_code=401,
                detail='Incorrect credentials.'
            )
    else:
        raise HTTPException(
            status_code=400,
            detail='That user ID does not exist in our system.'
        )


def add_user(user_id, password, role):
    '''
    Adds new user to the users table in database. Returns 
    string that user has been added.
    '''

    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is already a user."
        )
    else:
        role = role.lower()
        salt = os.urandom(32)
        hash = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=salt,
            iterations=100000
        )
        database_users.db_add_user(user_id, role, salt, hash)

        return {'message': f"{user_id} has been successfully added as a {role}."}


def remove_user(user_id):
    '''
    Removes user from users table in database. 
    Returns string if removal was successful.
    '''
    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        role = database_users.db_get_user_role(user_id)
        # can remove if scheduler
        if role == "scheduler":
            database_users.db_remove_user(user_id)
            return {'message': f"{user_id} has been successfully removed as a user."}
        else:
            num_admins = database_users.db_count_admins()
            # can remove if they are an admin but there's more than 1 admin left
            if num_admins != 1:
                database_users.db_remove_user(user_id)
                return {'message': f"{user_id} has been successfully removed as a user."}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"{user_id} is the final admin and cannot be removed."
                )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )


def update_user_role(user_id, role):
    '''
    Updates role of a user. Returns string if update was successful. 
    '''

    exist_user = database_users.db_user_exists(user_id)
    role = role.lower()

    if exist_user:
        prev_role = database_users.db_get_user_role(user_id)
        # can upgrade to admin if scheduler
        if prev_role == "scheduler":
            database_users.db_update_user_role(user_id, role)
            return {'message': f"{user_id} has been updated to {role}."}
        else:
            num_admins = database_users.db_count_admins()
            # can downgrade if they are an admin and there's more than 1 admin left
            if num_admins > 1:
                database_users.db_update_user_role(user_id, role)
                return {'message': f"{user_id} has been updated to {role}."}
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"{user_id} is the final admin and cannot be downgraded to scheduler."
                )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )


def update_user_id(user_id, new_user_id):
    '''
    Updates user_id of a user. Returns string if update was successful. 
    '''

    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        # Check if ID already exists for another user
        new_id_occupied = database_users.db_user_exists(new_user_id)

        if new_id_occupied:
            raise HTTPException(
                status_code=400,
                detail=f"User ID {new_user_id} is occupied by another user."
            )
        else:
            # Update user_d to new_user_id
            database_users.db_update_user_id(user_id, new_user_id)
            return {'message': f"Update successful! Old user id: {user_id} => New user_id: {new_user_id}."}
    else:
        # If old user_id  does not exist, return error
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )

def update_user_password(user_id, password):
    '''
    Updates password of a user. Returns string if update was successful.
    '''

    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        # Hash new password using salt
        salt = os.urandom(32)
        hash = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode('utf-8'),
            salt=salt,
            iterations=100000
        )
        # Update password, salt and hash
        database_users.db_update_user_password(user_id, salt, hash)
        return {'message': f"Successfully updated User {user_id}'s password."}
    else:
        # If user_id does not exist
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )


def activate_user(user_id):
    '''
    Function to activate a user
    '''
    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        # Check if active user
        active = database_users.db_is_user_active(user_id)
        
        if active:
            # If already active
            raise HTTPException(
                status_code=400,
                detail=f"{user_id} is already active."
            )
        else:
            # Activate user
            database_users.db_activate_user(user_id)
            return {'message': f"{user_id} successfully activated."}
    else:
        # If user_id does not exist
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )


def deactivate_user(user_id):
    '''
    Function to deactivate a user
    '''
    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        # Check if active user
        active = database_users.db_is_user_active(user_id)
        
        if not active:
            # Return 400 if already inactive
            raise HTTPException(
                status_code=400,
                detail=f"{user_id} is already deactivated."
            )
        else:
            # Deactivate user
            database_users.db_deactivate_user(user_id)
            return {'message': f"{user_id} successfully deactivated."}
    else:
        # If user_id does not exist
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )


def show_users():
    '''
    Returns string with all valid user_ids and their respective roles.
    '''

    results = database_users.db_show_users()

    # Format table with user data
    row_format = '{:<15} {:<10}'
    table = row_format.format('User ID', 'Role') + '\n'
    table += row_format.format('------------', '----------') + '\n'
    # Apply row format to data
    for row in results:
        table += row_format.format(*row) + '\n'

    return {'data': table}


def show_clients():
    '''
    Returns string with all valid client user_ids, their role, and their balances.
    '''

    results = database_users.db_show_clients()

    # Format table with client data
    row_format = '{:<15} {:<10} {:<10} {:<10}'
    table = row_format.format('User ID', 'Role', 'Balance', 'Active') + '\n'
    table += row_format.format('------------', '----------', '----------', '----------') + '\n'
    # Apply row format to data
    for row in results:
        table += row_format.format(*row) + '\n'

    return {'data': table}


def show_client(user_id):
    '''
    Returns string with all valid client user_ids, their role, and their balances.
    '''
    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        result = database_users.db_show_client(user_id)

        # Format table with client data
        row_format = '{:<15} {:<10} {:<10} {:<10}'
        table = row_format.format('User ID', 'Role', 'Balance', 'Active') + '\n'
        table += row_format.format('------------', '----------', '----------', '----------') + '\n'
        # Apply row format to data
        table += row_format.format(*result) + '\n'

        return {'data': table}
    else:
        # If user_id does not exist
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )
    

def add_balance(user_id, amount):
    '''
    Add balance to user_id
    '''
    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        # Add balance to user DB
        database_users.db_update_balance(user_id, amount)
        balance = database_users.db_get_balance(user_id)
        return {'message': f"Fund successfully added to {user_id}'s account. Current balance is {balance}."}
        
    else:
        # If user_id does not exist
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )


def show_balance(user_id):
    '''
    Show balance for user_id
    '''
    exist_user = database_users.db_user_exists(user_id)

    if exist_user:
        # Get balance for DB
        balance = database_users.db_get_balance(user_id)
        return {'message': f"Current balance is {balance}."}
        
    else:
        # If user_id does not exist
        raise HTTPException(
            status_code=400,
            detail=f"{user_id} is not a user."
        )