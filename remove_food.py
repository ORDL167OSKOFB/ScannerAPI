import os
import pyodbc
from flask import Flask, jsonify, request

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

