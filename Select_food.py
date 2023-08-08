from flask import Flask
from flask import request


import pyodbc
app = Flask(__name__)

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

@app.route('/return_foods', methods=['GET'])
def select_data():
    
    print("Inside Select Function!")
    cursor = connect.cursor()
    select_query = "SELECT * FROM Foods;"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    connect.commit()
    connect.close()
    

select_data()

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
        
if __name__ == '__main__': 
    app.run(debug=True)

