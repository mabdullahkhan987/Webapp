import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="abdullah",
    password="abdullah3539##",
    database="year2023"
)
cursor = db_connection.cursor()

def insert_data(month, name, procedure_type, amount, day):
    query = f"INSERT INTO {month} (name, procedure_type, amount, day) VALUES (%s, %s, %s, %s)"
    values = (name, procedure_type, amount, day)
    cursor.execute(query, values)
    db_connection.commit()

def insert_data2(procedurename):
    query = "INSERT INTO proceduretable (procedurename) VALUES (%s)"
    values = (procedurename,)
    cursor.execute(query, values)
    db_connection.commit() 