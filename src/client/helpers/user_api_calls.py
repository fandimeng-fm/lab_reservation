import requests

BASE_URL = "http://127.0.0.1:8000"

def get_user_role(user_id, password = ""):
    '''
    This function makes an api validate a user_id

    Inputs:
      user_id (str)

    Return:
      None if the user is not in the database
      "admin" if the user's role is admin
      "scheduler" if the user's role is scheduler
    '''
    url = BASE_URL + f"/users?user_id={user_id}&password={password}"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        print(f"Validation failed: {data['detail']}")
        return None
    else:
        print(f"Validation successful! Your role is: {data['data']}")
        return data['data']

def get_all_users():
    '''
    This function makes an api validate a user_id

    Return:
      a table of all users and their roles
    '''
    url = BASE_URL + f"/users/all"
    response = requests.get(url)
    data = response.json()
    print(data['data'])

def add_user(user_id, password, role):
    '''
    This function makes an api call to add a user

    Inputs:
      user_id (str)
      role (str): scheduler or admin
    '''
    url = BASE_URL + f"/users"
    post_body = {
        "user_id": user_id,
        "password": password,
        "role": role
    }
    response = requests.post(url, json=post_body)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(data['detail'])
    else:
        print(data['message'])
    
def remove_user(user_id):
    '''
    This function makes an api call to remove a user

    Inputs:
      user_id (str)
    '''
    url = BASE_URL + f"/users/{user_id}"
    response = requests.delete(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(data['detail'])
    else:
        print(data['message'])

def update_user_id(user_id, new_user_id):
    '''
    This function makes an api call to change user's user_id

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/users/{user_id}"
    post_body = {
        "user_id": new_user_id,
        "password": "",
        "role": ""
    }
    
    response = requests.put(url, json=post_body)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")

def update_user_role(user_id, role):
    '''
    This function makes an api call to change user's role

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/users/{user_id}"
    post_body = {
        "user_id": "",
        "password": "",
        "role": role
    }
    
    response = requests.put(url, json=post_body)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")

def update_user_password(user_id, password):
    '''
    This function makes an api call to change user's password

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/users/{user_id}"
    post_body = {
        "user_id": "",
        "password": password,
        "role": ""
    }
    
    response = requests.put(url, json=post_body)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")

def activate_user(user_id):
    '''
    This function makes an api call to activate a user

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/users/activate/{user_id}"
    
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")

def deactivate_user(user_id):
    '''
    This function makes an api call to deactivate a user

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/users/deactivate/{user_id}"
    
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")

def get_all_clients():
    '''
    This function makes an api call to get all clients

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/clients"
    
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    print(f"{data['data']}")

def get_client(user_id):
    '''
    This function makes an api call to get a specific client

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/clients/{user_id}"
    
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['data']}")

def get_user_balance(user_id):
    '''
    This function makes an api call to get the balance of client

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/balance?user_id={user_id}"
    
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")

def update_balance(user_id, amount):
    '''
    This function makes an api call to get the balance of client

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/balance?user_id={user_id}&amount={amount}"
    
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Update failed: {data['detail']}")
    else:
        print(f"{data['message']}")
