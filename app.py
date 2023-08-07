# from dbm import Database
from flask import Flask
from flask import request


import pyodbc
app = Flask(__name__)


import pyodbc

# Connect DB 

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
def select_data():
    
    print("Inside Select Function!")
    cursor = connect.cursor()
    select_query = "SELECT * FROM Foods;"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connect.commit()


def insert_data(food_name, quantity, expiry_date, date_added):
    try:
        cursor = connect.cursor()

        insert_query = "INSERT INTO Foods (FoodName, Quantity, ExpiryDate, DateAdded) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, food_name, quantity, expiry_date, date_added)
        
        connect.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        


def remove_food(food_name, quantity, expiry_date, date_added):
    try:
        cursor = connect.cursor()

        delete_query = "DELETE FROM Foods WHERE FoodName = ? AND Quantity = ? AND ExpiryDate = ? AND DateAdded = ?"
        cursor.execute(delete_query, food_name, quantity, expiry_date, date_added)
        
        connect.commit()
        print("Remove Called successfully.")
    except Exception as e:
        print("An error occurred:", e)
        


# QUERIES

select_data()

# INSERT DATA 

# Call the function to insert data
insert_data("Apple", 5, '2023-12-30', '2023-07-18')
insert_data("Banana", 5, '2023-12-30', '2023-07-18')

# REMOVE DATA- TEST
   
print("before remove Select")
select_data()
remove_food("Apple", 5, '2023-12-30', '2023-07-18')

print("after remove Select")
select_data()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__':
    app.run(debug=True)





# # QUERIES

# select_data()

# # INSERT DATA 

# # Call the function to insert data
# insert_data("Apple", 5, '2023-12-30', '2023-07-18')
# insert_data("Banana", 5, '2023-12-30', '2023-07-18')

# # REMOVE DATA- TEST
   
# print("before remove Select")
# select_data()
# remove_food("Apple", 5, '2023-12-30', '2023-07-18')

# print("after remove Select")
# select_data()
