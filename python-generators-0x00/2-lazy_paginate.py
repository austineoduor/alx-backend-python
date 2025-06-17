#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows
    
    
def lazy_paginate(page_size):
    '''retrieves rows from from offset to Limit'''
    offset = 0
    data = paginate_users(page_size, offset)
    while len(data) != 0:
        print(data)
        print(offset)
        offset += page_size
        data = paginate_users(page_size, offset)
