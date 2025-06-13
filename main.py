import mysql.connector

def getconnection():
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345y.k",
        database="libmanage"
        )
    return mydb
