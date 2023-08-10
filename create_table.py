import os
import pyodbc
from flask import Flask, jsonify, request
from Select_food import select_data
from flask_cors import CORS
import configparser

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://40268037flaskfrontend.azurewebsites.net"}})

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

def create_table(connection):
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

def check_table_exists(connection):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_NAME = 'Foods'
    """)
    result = cursor.fetchone()
    return result is not None

def init_food():
    with create_connection() as connection:
        if not check_table_exists(connection):
            create_table(connection)
            return "New Food Table has been created."
        else:
            return "Food Table already exists."

db_init_result = init_food()
print(db_init_result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    # Redeploy