import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:51222"

def client_signin_pref():
    '''
    This function makes an api call to get client sign-in preference
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/pref"
    response = requests.get(url)
    data = response.json()

    return data['pref']

def make_hold(post_body):
    '''
    This function makes an api call to make a hold

    Inputs:
      post_body (dict): information needed to make a hold
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/holds"
    response = requests.post(url, json=post_body)
    data = response.json()

    # Check the status code of the response
    if response.status_code != 200:
        print(f"Hold failed: {data['detail']}")
    else:
        print(f"Hold successfully made! " \
            f"Your reservation ID is: {data['reservation_id']}")

def make_reservation(post_body):
    '''
    This function makes an api call to make reservation

    Inputs:
      post_body (dict): information needed to make reservation
    '''
    # Making API call to make reservation
    url = BASE_URL + f"/reservations"
    response = requests.post(url, json=post_body)
    data = response.json()

    # Check the status code of the response
    if response.status_code != 200:
        print(f"Reservation failed: {data['detail']}")
    else:
        print(f"Reservation successfully made!" \
            f"Your reservation ID is: {data['reservation_id']}")
    
def cancel_reservation(reservation_id):
    '''
    This function makes an api call to cancel reservation

    Inputs:
      reservation_id (string): id of the reservation to be cancelled
    '''
    # Making API call to cancel reservation
    #url = BASE_URL + f"/reservations/cancel/{reservation_id}?user_id={user_id}"
    url = BASE_URL + f"/reservations/cancel/{reservation_id}"
    response = requests.get(url)
    data = response.json()

    # Check the status code of the response
    if response.status_code == 400:
        print(f"Reservation cancellation failed: {data['detail']}")
    else:
        print("Reservation successfully cancelled")

def get_reservations(start_date, end_date, customer_id=None, export_csv=False, location = "", name = ""):
    '''
    This function makes an api call to get reservations on a date range

    Inputs:
      start_date (string): start date of the date range
      end_date (string): end date of the date range
      customer_id (string, optional): customer ID that we are interested in
    '''
    if customer_id:
        params = {
            'start_date': start_date, 
            'end_date': end_date, 
            'customer_id': customer_id
        }
    else:
        params = {
            'start_date': start_date, 
            'end_date': end_date
        }

    # Making API call to retreive reservations on the date range
    url = BASE_URL + f"/reservations"
    response = requests.get(url, params=params)
    data = response.json()

    # This API always return 200 so there's no need to check
    print(data['data'])

    if export_csv:
        if location:
            if name:
                output_file = f"{location}{name}.csv"
        else:
            output_file = f"{location}reservations_{start_date}_to_{end_date}.csv"
        output_reservations_csv(data['csv_data'], output_file)

def output_reservations_csv(data, output_file):
    '''Writes reservations JSON to CSV file.'''

    df = pd.DataFrame.from_records(data)
    df.to_csv(output_file, index=False)

def get_all_holds():
    '''
    This function makes an api call to get all holds
    '''
    url = BASE_URL + f"/reservations/holds"
    response = requests.get(url)
    data = response.json()

    print(data['data'])
    
def get_all_transactions():
    '''
    This function makes an api call to get transactions 
    '''

    # Making API call to retreive transactions on the date range
    url = BASE_URL + f"/transactions"
    response = requests.get(url)
    data = response.json()

    # This API always return 200 so there's no need to check
    print(data['data'])

def get_all_transactions_by_id(user_id):
    '''
    This function makes an api call to get transactions 
    '''

    # Making API call to retreive transactions on the date range
    url = BASE_URL + f"/transactions/{user_id}"
    response = requests.get(url)
    data = response.json()

    # This API always return 200 so there's no need to check
    print(data['data'])