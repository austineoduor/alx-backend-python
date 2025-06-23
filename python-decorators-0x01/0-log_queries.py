#!/usr/bin/env python3

import sqlite3
import functools
import logging
#### decorator to log SQL queries

def log_queries(func):
    functools.wraps(func)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('query.log')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
     
    def log_queries_wrapper(*args, **kwargs):
        query = "Executing: {} - {}".format(*args, **kwargs)
        logger.info(query)
        return func(*args,**kwargs)
        return log_queries_wrapper
         
         

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
