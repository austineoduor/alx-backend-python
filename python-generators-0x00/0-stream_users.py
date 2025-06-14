#!/usr/bin/env python
'''quering the user_data'''
cnx = __import__('seed')

def stream_users():
    '''
    generator function that yields user_data row at a time
    '''
    conn = cnx.connect_to_prodev()
    cursor = conn.cursor()
    query = "SELECT * FROM user_data"
    try:
        cursor.execute(query)
        for row in cursor.fetchall():
            yield row
    except conn.Error as err:
        print("Error occured {}".format(err))
        exit(1)
    cursor.close()
    conn.close()


