#!/usr/bin/env python3

user_data = __import__("1-batch_processing")


def stream_user_ages():
    page_size = 100
    users = user_data.stream_users_in_batches(page_size)
    for user in users:
        yield user['age']


def calculate_average_age():
    total_users = 0
    total_age = 0 
    avg = 0
    user_age = stream_user_ages()
    for age in user_age:
        total_users += 1
        total_age += age

    avg = total_age/total_users

    print("Average age of users: {}".format(avg))
        
        
if __name__ == '__main__':
    calculate_average_age()
    #stream_user_ages()
