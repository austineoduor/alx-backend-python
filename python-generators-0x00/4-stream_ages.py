#!/usr/bin/env python3

user_data = __import__("2-lazy_paginate").paginate_users


def stream_user_ages():
    print("calling ...")
    page_size = 50
    offset = 0
    while True:
        data = user_data.paginate_users(page_size, offset)
        if data:
            for _ in data:
                print(data['age'])
                #yield user('age')
        else:
            print("No data found")
            exit(1)
    
def calculating_average_age():
    while True:
        data = stream_user_ages()
        print(data)
        rows = (row for row in data)
        if rows:
            print(rows)

        else:
            break
        
        
if __name__ == '__main__':
    calculating_average_age()
