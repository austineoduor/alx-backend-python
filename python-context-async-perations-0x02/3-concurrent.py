#!/usr/bin/env python
import aiosqlite
import asyncio

db_name = "users.db"
query1 = 'SELECT * FROM users'
query2 = 'SELECT * FROM users WHERE age > 40'

async def async_fetch_users():
    try:
        async with aiosqlite.connect(db_name) as db:
            async with db.execute(query1) as cursor:
                rows = await cursor.fetchall()
                return rows
    except aiosqlite.Error as err:
        print(f"Error occured: {err}")

async def async_fetch_older_users():
    try:
        async with aiosqlite.connect(db_name) as db:
            async with db.execute(query2) as cursor:
                rows = await cursor.fetchall()
                return rows
    except aiosqlite.Error as err:
        print(f"Error occured: {err}")

async def main():
    res = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print(res)

if __name__ == "__main__":
    asyncio.run(main())