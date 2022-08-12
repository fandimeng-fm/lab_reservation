# Helper function to interact with database:
#
# Fabrizio Giovannini Filho, Yuxin Guan, Lynnette Jiang, Jared McKeon, Fandi Meng

import sqlite3, os, csv, shutil, hashlib

DIRNAME = os.path.dirname(__file__)
CREATE_DB_FILE = os.path.join(DIRNAME, 'create_db.sql')
DATA_DIRECTORY = os.path.join(DIRNAME, '../../../data')
RESERVATIONS_DATA = os.path.join(DATA_DIRECTORY, 'reservations.csv')
TRANSACTIONS_DATA = os.path.join(DATA_DIRECTORY, 'transactions.csv')
USERS_DATA = os.path.join(DATA_DIRECTORY, 'users.csv')
DATABASE_FILE = os.path.join(DATA_DIRECTORY, 'reservations.db')
BACKUP_DATABASE_FILE = os.path.join(DATA_DIRECTORY, 'reservations_backup.db')
TEST_DATABASE_FILE = os.path.join(DATA_DIRECTORY, 'test_reservations.db')


def get_db_connection():
    '''
    Function to connect to database
    '''
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_hash(password):
    salt = os.urandom(32)
    hashed = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=100000
    )
    return salt, hashed

def add_data_to_table(cursor, data_path, table):
    '''
    Function to insert data into a database (determined by the cursor), given a data path
    and table (3 tables - reservations, transactions and users)
    '''
    # Get number of values to be used in each table
    DICT_NUMBER_OF_VALUES = {'reservations': 9, 'transactions': 6, 'users': 6}
    number_of_values = DICT_NUMBER_OF_VALUES[table]

    # Insert data into table
    open_data_file = open(data_path)
    if table == "users":
        # Read CSV data
        raw_data = csv.reader(open_data_file)
        next(raw_data, None)
        data_rows = []

        # Create hashed password using salt
        for row in raw_data:
            password = row[4]
            salt, hashed = generate_hash(password)
            data_rows.append([row[0], row[1], row[2], row[3], salt, hashed])
    else:
        data_rows = csv.reader(open_data_file)
        next(data_rows, None)
        
    # Execute query
    cursor.executemany(f"INSERT INTO {table} VALUES (?{' , ?'*(number_of_values-1)})", data_rows)


def reset_dbs_to_original():
    '''
    Function to repopulate both reservation and testing databases with original data.
    Returns True if database creating was successful.
    '''

    # Connect to DB
    conn = get_db_connection()
    sql_query = open(CREATE_DB_FILE, 'r').read()

    # Execute script to create tables
    cursor = conn.cursor()
    cursor.executescript(sql_query)

    # Add reservations data
    add_data_to_table(cursor, RESERVATIONS_DATA, 'reservations')
    add_data_to_table(cursor, TRANSACTIONS_DATA, 'transactions')
    add_data_to_table(cursor, USERS_DATA, 'users')

    # Commit and close
    conn.commit()
    conn.close()

    # Copy reservations data to testing database
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)
    shutil.copyfile(DATABASE_FILE, TEST_DATABASE_FILE)

if __name__ == '__main__':
    reset_dbs_to_original()

def save_current_version_of_db():
    '''
    Function to preserve user data to run tests
    '''
    if os.path.exists(BACKUP_DATABASE_FILE):
        # Delete backup file if it already exists
        os.remove(BACKUP_DATABASE_FILE)
    # Rename current DB to backup name
    shutil.copyfile(DATABASE_FILE, BACKUP_DATABASE_FILE)
    

def restore_db_from_backup():
    '''
    Function to restore database file from backup
    '''
    if os.path.exists(BACKUP_DATABASE_FILE):
        os.remove(DATABASE_FILE)
        shutil.copyfile(BACKUP_DATABASE_FILE, DATABASE_FILE)
        os.remove(BACKUP_DATABASE_FILE)
    else:
        raise Exception("Backup file does not exits and database cannot be restored.")


def use_test_db():
    '''
    Function that substitutes current version of the database with the test data
    '''
    # First, backup current database
    save_current_version_of_db()

    # Copy test data to database
    os.remove(DATABASE_FILE)
    shutil.copyfile(TEST_DATABASE_FILE, DATABASE_FILE)