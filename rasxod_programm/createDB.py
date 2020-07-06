import mysql.connector
from mysql.connector import Error
try:
    connection  = mysql.connector.connect(host="localhost",  user="root",  password="root")
    if connection .is_connected():
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_rasxod")
        cursor.execute("USE  db_rasxod")
        cursor.execute("CREATE TABLE IF NOT EXISTS test(Id INT AUTO_INCREMENT PRIMARY KEY, time DATETIME, value FLOAT(30,3))")
        cursor.execute('INSERT INTO test VALUES(0,"2000-12-12 00:00:00",0.0)')
        connection.commit()
        print("Successfull")
    
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
