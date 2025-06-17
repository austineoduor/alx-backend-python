#!/usr/bin/env python3

user_data = __import__("2-lazy_paginate")


def stream_user_ages():
    page_size = 100
    n = 0
    while True:
        users = user_data.lazy_paginate(page_size)
        ln = len(users)
        if users and n <= ln:
            n + 1
            for user in users:
                print(user)
                yield user
        else:
            #print("No data found")
            break


def calculate_average_age():
    size = 0
    total_age = 0
    while True:
        data = [ d for d in stream_user_ages()]
        if data:
            total += sum(data['age'])
            size = len(data)

        else:
            break
    avg = total_age/size
    print("Average age of users: {}".format(avg))
        
        
if __name__ == '__main__':
    calculate_average_age()
    #stream_user_ages()
