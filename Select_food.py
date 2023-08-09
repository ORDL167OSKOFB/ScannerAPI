from flask import Flask
from flask import request


import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://foodwasteappfrontend.azurewebsites.net"}})


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

