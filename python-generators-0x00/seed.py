#!/usr/bin/env python3
import mysql.connector as mcnx
from mysql.connector import errorcode
def connect_db():
    try:
        cnx = mcnx.connect(user='root', password='kali')
        print("successful")
        return cnx
    except mcnx.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your usernmae or password")
        else:
            print(err)

if __name__ == "__main__":
    connect_db()
