# GW04 - Runtime Terror

### Program Description:
This is a command line program for reserving equipment at MPCS Inc. This progam utilises an API to interact with a database with reservation, transaction and user data. 

### Program Dependencies:
This program was written in Python 3.7. The full list of library requirements can be found in `requirements.txt` . 

### Execution:
- We recommend running `pip install -r requirements.txt` before running our client file. 
- To run the server, run `uvicorn server:app --reload` in the `src/server/` folder
- To run the client, run `python src/client/client.py`

### User Management:
- Users login with a user ID and password. The system user's ID is passed to the server when transactions are made so that their ID and timestamp can be recorded in a transaction database.
- We allow 3 types of user roles: "client", "scheduler", and "admin".
    - Clients can book reservations, cancel reservations, add funds to their account, show their transactions and balance, and  edit their profile.
    - Schedulers, or facility managers, can perform all the user functions for all users and can view reservation and transaction reporting for their entire facility. However, schedulers cannot add/delete/modify user roles. 
    - Admins can perform user management by adding users, removing users, and modifying their roles. We enforce the restriction that there should always be at least 1 admin.

### Optional Requirements and Features for G-03:
- Export Reports: if you sign in as a facility manager or a client, when you select the action to view reservations, you will be prompt to choose whether you want to export report or not.
- Launch-time parameter to specify if client logins are allowed: when start running the server, you will be prompt to select whether you want to allow client sign-in or not.
- Simplified business rules
- Allow facility managers to edit client details
- Additional features to let facility managers search for reservations and clients, and deactivate/reactivate clients

### Database implementation:
- We have implemented a database using the sqlite3 python library to persist the data for reservation, transactions and users.
- The functions to manage the database are in the `database_functions.py` file and the `create_db.sql` file.
- The `database_functions.reset_dbs_to_original()` function is used to restore both the reservations and testing data to its original state using th SQL script 'create_db.sql'.
- The `database_functions.use_test_db()` function is used for testing. It first backup up the current database to a 'reservations_backup.db' file in the 'data' folder. It then replaces the contents of the 'reservations.db' with those of 'test_reservations.db' to be used in the tests in the 'test_api.py' and 'test_db.py' programs.
- The `database_functions.restore_db_from_backup()` restores the data in the 'reservations.db' file to that of the backup file 'reservations_backup.db'. This function is used in the test programs 'test_api.py' and 'test_db.py' to maintain the latest state of the database while also being able to consistently test it.
- The database has three tables: reservations, transactions and users.
- The database is initially populated with data from `reservations.csv`, `transactions.csv`, and `users.csv`.

### Data Persistence: 
In our `data/` folder, we store our database `reservations.db` , which we use as a persistance mechanism across server sessions. When the database is reset, it is populated with data from `reservations.csv`, `transactions.csv`, and `users.csv`.

### Assumptions:
We are assuming clients never attempt to make reservations for crushers for more than 30 minutes at a time. We are also assuming that crushers and irradiators are able to recalibrate and cooldown, respectively, after hours. 

### Testing:
- There are three testing files: 
    - `test_api.py`: tests for functions for the reservations API
    - `test_db.py`: tests for functions for the database 
    - `test_client.py`: tests for functions for the client UI 
- To execute the tests for API and database, first start a terminal to run the server, then run ` python -m pytest` while in the `src/server/` folder
- To execute the tests for client UI, first start a terminal to run the server, then run `pytest` while in the `src/client/` folder
- You can also sign in as test users to test the functionalities:
    * user_id: admin1, password: admin1password (admin role)
    * user_id: scheduler1, password: scheduler1pw (facility manager role)
    * user_id: client1, password: client1pw (client role)
    * user_id: peter, password: peterpw (remote manager role)

### Endpoint testing troubles:
None that we are aware of.


### Source code management approach:
- We largely distributed work amongst ourselves via mutually exclusive features to be built. Given a code base of a previous assignment, we had a strong foundation to understand the different data structures and business functions that we had slight variations on individually in the prior assignments. We assigned different API endpoints to different people (such as post reservation method, get reservation method, get cancel_reservation method, etc). We were each responsible for writing tests for our assigned endpoints. Lastly, one team member was responsible for the client/UI.
- We used a mainline integration approach to manage updates to source code. Since most of our work could be done independently from each other and we had enough time throughout the week, there weren't many conflicts to manage as we pulled from the master branch from gitlab and pushed our updates back to it.


