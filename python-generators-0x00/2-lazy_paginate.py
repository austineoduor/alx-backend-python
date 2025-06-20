#!/usr/bin/env python3
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
    while True:
        data = paginate_users(page_size, offset)
        if not data:
            return 0  # Exit loop if no more data is returned
        else:
            yield data
        offset += page_size

if __name__ == '__main__':
    lazy_paginate(100)
