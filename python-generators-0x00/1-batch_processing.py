#!/usr/bin/env python
'''batch processing'''
from itertools import islice
import mysql.connector as mcnx

cnx = __import__('seed')

def stream_users_in_batches(batch_size):
    '''fetches row in batches of batch_size'''
    conn = cnx.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM user_data"
    try:
        while True:
            cursor.execute(query)
            for row in cursor.fetchmany(batch_size):
                if not row:
                    break
                else:
                    yield row
        cursor.close()
    except mcnx.Error as err:
        print("Error occured {}".format(err))
        exit(1)
    finally:
        conn.close()
        
        
def batch_processing(batch_size):
    '''
    process the rows fetched and filter users over the age of 25
    '''
    lim_age = 25
    try:
        for users in islice(stream_users_in_batches(batch_size), batch_size):
            if users['age'] <= lim_age:
                continue
            else:
                print(users)
    except Exception as err:
        print("Encountered Error(s): {}".format(err))
        exit(1)
