import os
import pyodbc
from flask import Flask, jsonify, request
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


@app.route('/delete-foods', methods=['DELETE'])
def delete_food():
    data = request.get_json()
    remove_food(data['food_name'], data['quantity'], data['expiry_date'], data['date_added']) 
    return jsonify({'message': 'Food removed successfully.'}), 200



def remove_food(food_name, quantity, expiry_date, date_added):
    try:
        cursor = connection.cursor()

        delete_query = "DELETE FROM Foods WHERE FoodName = ? AND Quantity = ? AND ExpiryDate = ? AND DateAdded = ?"
        cursor.execute(delete_query, food_name, quantity, expiry_date, date_added)
        
        connection.commit()
        print("Remove Called successfully.")
    except Exception as e:
        print("An error occurred:", e)
    

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__': 
    app.run(debug=True)

