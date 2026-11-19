import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="wellness_db"
)

if conn.is_connected():
    print("Connected to MySQL successfully!")

conn.close()