import os
import pyodbc
from flask import Flask, jsonify, request
from Select_food import select_data
app = Flask(__name__)

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

server = config['DATABASE']['server']
db = config['DATABASE']['db']
username = config['DATABASE']['user']
password = config['DATABASE']['password']
driver = config['DATABASE']['driver']
port = config['DATABASE']['port']
conn_str =  f'DRIVER={driver};SERVER={server};PORT={1433};DATABASE={db};UID={username};PWD={password}'


def create_connection():
    return pyodbc.connect(conn_str)
 
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


@app.route('/init-food', methods=['POST'])
def init_food():
    if not check_table_exists():
        create_table()
        message = "New Food Table has been created."
    else:
        message = "Food Table already exists."
    
    connection.close()
    return jsonify({'message': message}), 200


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__': 
    app.run(debug=True)
