#!/usr/bin/env python3
'''batch processing'''

from itertools import islice
import mysql.connector as mcnx

cnx = __import__('seed')

def stream_users_in_batches(batch_size):
    '''
    fetches row in batches of batch_size
    '''
    conn = cnx.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM user_data"
    try:
        cursor.execute(query)
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                cursor.close()
                break
            else:
                for user in rows:
                    yield user
        cursor.close()
    except mcnx.Error as err:
        print("Error occured {}".format(err))
    finally:
        conn.close()

def batch_processing(batch_size):
    '''
    processes user data for age greater than 25
    '''
    age_lim = 25
    try:
        for user in stream_users_in_batches(batch_size):
            if user:
                if user['age'] > age_lim:
                    print(user)
                else:
                    continue
            else:
                break
    except Exception as err:
        print("Caught an error {}".format(err))

if __name__ == '__main__':
    batch_processing(10)
