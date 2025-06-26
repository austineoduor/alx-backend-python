!#/usr/bin/env python

import sqlite3

class DatabaseConnection(object):
    
    def __init__(self, db_name):
        self.db_name = db_name
        

    def __enter__(self):
        self.conn = sqlite.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self
        
        
    def __exit__(self, exc_type,exc_val,exc_tb):
        if exc_type is not None:
            print("Caught an Error: {}\n{}".format(exc_val, exc_tb))
        print("Closing connection")
        self.conn.close()
    
if __name__ == '__main__':
    
    query = "SELECT * FROM users"
    db_name = "usrs.db"
   with DatabaseConnection(db_name) as db:
       res = db.cursor.execute(query)
       print(res)