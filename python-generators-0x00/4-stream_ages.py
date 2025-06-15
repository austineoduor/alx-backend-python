#!/usr/bin/env python

user_data = __import__("2-lazy_paginate").paginate_users


def stream_user_ages():
    page_size = 50
    offset = 0
    data = user_data.paginate_users(page_size, offset)
    if data:
        for user in data:
            print(user['age'])
            yield user('age')
    else:
        print("No data found")
    
def calculating_average_age():
    while True:
        data = stream_user_ages()
        if not data:
            break
        
        
if __name__ == '__main__':
    stream_user_ages()