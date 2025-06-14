#!/usr/bin/env python
'''batch processing'''
from itertools import islice
import mysql.connector as mcnx

cnx = __import__('seed')

def stream_users_in_batches(batch_size):
    '''fetches row in batches of batch_size'''
    conn = cnx.connect_to_prodev
    cursor = conn.cursor()
    query = "SELECT * FROM user_data"
    try:
        cursor.execute(query)
        for row in cursor.fetchmany(batch_size):
            yield row
    except mcnx.Error ass err:
        print(err)
        exit(1)
    finally:
        cursor.close()
        conn.close()
        
        
def batch_processing(batch_size):
    '''
    process the rows fetched and filter users over the age of 25
    '''
    try:
        for users in islice(stream_users_in_batches(batch_size)):
            if users['age'] =< 25:
                continue:
            else:
            yield users
    except Exception as err:
        print(err)
        exit(1)