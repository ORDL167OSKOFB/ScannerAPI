import pyodbc
import pyodbc 
from flask import Flask, jsonify, request

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

@app.route("/update-quantity", methods=['PUT'])
def reduce_quantity(uid, qty):
    
    try:
        connection = create_connection()
        cursor = connection.cursor()

        
        select_query = "SELECT Quantity, FoodName FROM Foods WHERE UID = ?"
        cursor.execute(select_query, uid)
        result = cursor.fetchone()

        if result:
            prev_qty, food_name = result[0], result[1]
            new_qty = max(0, prev_qty - qty)  # >0 boundary added for qty testing

            # Update the quantity in the database using UID
            update_query = "UPDATE Foods SET Quantity = ? WHERE UID = ?"
            cursor.execute(update_query, new_qty, uid)

            connection.commit()
            print(f"Quantity of  {uid} reduced by {qty}. New quantity is {new_qty}.")
        else:
            print(f"No food item found with UID {uid}")

    except Exception as e:
        print("An error occurred:", e)