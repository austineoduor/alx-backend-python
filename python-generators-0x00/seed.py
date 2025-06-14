#!/usr/bin/env python3

import csv
import mysql.connector as mcnx
from mysql.connector import errorcode

DBNAME = "ALX_prodev"
db_config = {'user':'root', 'password':'kali', 'database':'ALX_prodev'}
TABLES = {}

TABLES["user_data"] = ( 
"CREATE TABLE IF NOT EXISTS `user_data`("
"user_id BINARY(40),"
"name VARCHAR(100) NOT NULL,"
"email VARCHAR(100) NOT NULL,"
"age DECIMAL NOT NULL, "
"PRIMARY KEY (`user_id`),"
"UNIQUE INDEX(`user_id`)"

")ENGINE=InnoDB")

def connect_db():
    '''
    creates a connection to the mysqlserver
    and retuns a connection
    '''
    try:
        cnx = mcnx.connect(user='root', password='kali')
        if cnx.is_connected():
            #print("successful connected to mysql-sever")
            return cnx
    except mcnx.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your usernmae or password")
            exit(1)
        else:
            print(err)
            exit(1)


def create_database(connection):
    '''
    creates the database if it doesn't exist,
    and returns a cursor
    '''
    cursor = connection.cursor()
    try:
        dbnx = cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET utf8;".format(DBNAME))
        #print("connected to mysql server and created ALX_prodev database")
        return dbnx
    except mcnx.Error as err:
        print(err)
        exit(1)


def connect_to_prodev():
    '''
    creates connection to database ALX_prodev
    '''
    try :
        cnx = mcnx.connect(**db_config)
        if cnx.is_connected():
           # print("connected to ALX_prodev")
            return cnx
    except mcnx.Error as err:
        '''if err.errno == errorcode.ER.BAD_DB_ERROR:'''
        print("The requested database is: {}".format(err))
        exit(1)


def create_table(connection):
    '''
    creates table user_data, if the table doesn't exist
    '''
    if connection.is_connected():
        cursor = connection.cursor()
        for table in TABLES:
            table_description = TABLES[table]
            #cursor.execute("USE {};".format(DBNAME))
            #print("Using: {}".format(DBNAME))
            try:
                cursor.execute(table_description)
              #  print("created the table")
            except mcnx.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("Already present {}".format(err))
                    exit(1)
                else:
                    print(err)
    else:
        print("No database connection")
        exit(1)


def insert_data(connection, data):
    '''
    insert data to the ALX_prodev database in user_data table
    '''

    with open(data, 'r') as file:
        reader = csv.reader(file)
        lines = (line for line in reader)
        file_lines =  (s for s in lines)
        cols = next(file_lines)
        user_data = [dict(zip(cols, v)) for v in file_lines]
        for user in user_data:
            userdata= {'name': user['name'],
                       'email': user['email'],
                       'age':user['age']
                       }
            data_desc = (
                    "INSERT INTO user_data""(user_id, name, email, age)"
                    "VALUES""(uuid(),%(name)s, %(email)s, %(age)s)"
                    )
            if connection.is_connected():
                cursor = connection.cursor()
                try:
                    cursor.execute(data_desc, userdata)
                    connection.commit()
                   # print("data inserted successfully")
                except mcnx.Error as err:
                    print(err)
                    exit(1)
            else:
                print("No connection")
                exit(1)
