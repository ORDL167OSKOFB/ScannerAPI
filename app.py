# from dbm import Database
from flask import Flask
from flask import request


import pyodbc
app = Flask(__name__)




import pyodbc


server = "sqlschema.database.windows.net"
db = "DatabaseSchema"
username = "Rebis"
password = "Osirion4"
driver = '{ODBC Driver 18 for SQL Server}'
port = '1433'
conn_str =  f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={db};UID={username};PWD={password}'
def create_connection():
    return pyodbc.connect(conn_str)  
print('Database connection successfully established') 

connect = create_connection()
@app.route('/')
def hello_world():
    return 'Hello, World!'

# As a scanner API, I am going to model the behaviour of this API After a real-life scanner. 
# That is, only one item can be scanned at a time. Therefore, the parameters passed will be the food name, date added and expiry date. 

@app.route('/add_food', methods=['POST'])
def add_food(): 
    food_name = request.json['FoodName']
    date_added = request.json['DateAdded']
    expiry_date = request.json['ExpiryDate']
    cursor = connect.cursor()   
    cursor.execute("INSERT INTO Foods (name, added, expiry) values (?, ?, ?)", food_name, date_added, expiry_date)
    return {'status': 'success'}, 200

# def add_new_food():
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

    

# @app.route('/remove_food', methods=['POST'])
# def remove_food():
#     food_name = request.json['FoodName']
#     cursor = connect.cursor()
#     cursor.execute("SELECT TOP 1 id FROM Foods WHERE name = ?", food_name)
#     return {'status': 'success'}, 200
# if __name__ == '__main__':
#     app.run(debug=True)
    
# def remove_multiple():
#     food_name = request.json['FoodName']
#     cursor = connect.cursor()
#     for i in range(0, len(food_name)):
#         cursor.execute("SELECT id FROM Foods WHERE name = ?", food_name)
#     return {'status': 'success'}, 200