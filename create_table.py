import os
import pyodbc
import configparser

def get_connection_string():
    azure_db = os.environ.get('DB_CONNECTION_STRING')
    
    if azure_db:
        return azure_db

    config = configparser.ConfigParser()
    config.read('config.ini')

    server = config['DATABASE']['server']
    db = config['DATABASE']['db']
    username = config['DATABASE']['user']
    password = config['DATABASE']['password']
    driver = config['DATABASE']['driver']
    port = config['DATABASE']['port']

    return f'DRIVER={driver};SERVER={server};PORT={port};DATABASE={db};UID={username};PWD={password}'

def create_connection():
    return pyodbc.connect(get_connection_string())

connection = create_connection()

def check_table_exists():
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = 'Foods'
    """)
    result = cursor.fetchone()
    return result is not None

def init_food():
    message = ""
    if not check_table_exists():
        create_table()
        message = "New Food Table has been created."
    else:
        message = "Food Table already exists."
    connection.close()
    print(message)

def create_table():
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE Foods (
        UID INT IDENTITY (1,1) PRIMARY KEY, 
        FoodName VARCHAR(255) NOT NULL, 
        Quantity INT NOT NULL, 
        ExpiryDate DATE NOT NULL,
        DateAdded DATE NOT NULL)
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Food table created successfully.")
    except Exception as e:
        print("An error occurred:", e)

init_food()

# redeployed to azure