# Test file for reservation_api_calls.py
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng
#
# Execution: pytest

import helpers.user_api_calls as user_api_calls

def test_validate_user_real(capfd):
    '''
    Test validate_user on real user_id
    '''
    # Use test data

    user_id = 'patrick'
    password = 'patrickpassword'

    user_api_calls.get_user_role(user_id=user_id, password=password)
    
    out, _ = capfd.readouterr()

    assert "Validation successful!" in out

def test_validate_user_wrong(capfd):
    '''
    Test validate_user on real wrong password
    '''
    # Use test data

    user_id = 'peter'
    password = '123456'

    user_api_calls.get_user_role(user_id=user_id, password=password)
    
    out, _ = capfd.readouterr()

    assert "Validation failed" in out

def test_validate_not_user(capfd):
    '''
    Test validate_user on real wrong password
    '''
    # Use test data

    user_id = '123456'
    password = '123456'

    user_api_calls.get_user_role(user_id=user_id, password=password)
    
    out, _ = capfd.readouterr()

    assert 'That user ID does not exist in our system.' in out


def test_add_user_new(capfd):
    '''
    Test adding a new user.
    '''
    # Use test data
    user_api_calls.add_user('peter', 'password1234', 'scheduler')

    out, _ = capfd.readouterr()

    assert 'is already a user.' in out

def test_get_all_clients(capfd):
    '''
    Test adding a new user.
    '''
    # Use test data
    user_api_calls.get_all_clients()

    out, _ = capfd.readouterr()

    assert 'client1' in out

def test_get_client(capfd):
    '''
    Test adding a new user.
    '''
    # Use test data
    user_api_calls.get_client('client1')

    out, _ = capfd.readouterr()

    assert 'client1' in out