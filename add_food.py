import os
import pyodbc
from flask import Flask, jsonify, request, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://40268037flaskfrontend.azurewebsites.net"}})
import configparser

def get_connection_string():
    # Obtainn string from azure environment before local
    azure_db = os.environ.get('DB_CONNECTION_STRING')
    
    if azure_db:
        return azure_db
    
    # Local db string
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

@app.route('/add-food', methods=['POST'])
def add_food():
    data = request.get_json()
    insert_data(data['food_name'], data['quantity'], data['expiry_date'], data['date_added'])
    connection.close()
    return jsonify({'message': 'Food added successfully.'}), 200


def insert_data(food_name, quantity, expiry_date, date_added):
    try:
        cursor = connection.cursor()

        insert_query = "INSERT INTO Foods (FoodName, Quantity, ExpiryDate, DateAdded) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, food_name, quantity, expiry_date, date_added)
        
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)

insert_data("Apple", 5, '2023-12-30', '2023-07-18')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__': 
    app.run(debug=True)
