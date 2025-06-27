#!/usr/bin/env python

import sqlite3

class ExecuteQuery(object):
    
    def __init__(self, db_name:str, query:str, age:int) -> None:
        self.db_name = db_name
        self.age = age
        self.query = query
        self.res = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query)
        self.res = self.cursor.fetchall()
        return self.res
        
        
    def __exit__(self, exc_type,exc_val,exc_tb):
        if exc_type is not None:
            print("Caught an Error: {}\n{}".format(exc_val, exc_tb))
        print("Closing connection")
        self.conn.close()
    
if __name__ == '__main__':
    
    query = "SELECT * FROM users"
    db_name = "users.db"
    lim_age = 25
with ExecuteQuery(db_name,query, lim_age) as db:
    res = db
    print(res)