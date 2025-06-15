#!/usr/bin/env python3

user_data = __import__("2-lazy_paginate")


def stream_user_ages():
    print("runing ..")
    page_size = 100 
    while True:
        data = user_data.lazy_paginate(page_size)
        if data:
            for user in data:
                yield user['age']
        else:
            #print("No data found")
            return False


def calculate_average_age():
    while True:
        data = [ d for d in stream_user_ages()]
        if data:
            #size += len(data)
            #print(size,'\n')
            print(data)
        else:
            break
        
        
if __name__ == '__main__':
    calculate_average_age()
    #stream_user_ages()
