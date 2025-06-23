#!/usr/bin/env python3

import sqlite3
import functools
import logging
#### decorator to log SQL queries

 def log_queries():
     functools.wrap()
     logger = logging.getLogger(__name__)
     hsndler = logging.formatter(query.log)
     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
     handler.setFormatter(formatter)
     logger.addHandler(handler)
     
     def log_queries_wrapper(*args, **kwargs):
         query = f"{}{}".format(*args, **kwargs)
         logger.info(query)
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