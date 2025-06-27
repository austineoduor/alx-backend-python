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
                for row in rows:
                    print(row)
    except aiosqlite.Error as err:
        print(f"Error occured: {err}")

async def async_fetch_older_users():
    try:
        async with aiosqlite.connect(db_name) as db:
            async with db.execute(query2) as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    print(row)
    except aiosqlite.Error as err:
        print(f"Error occured: {err}")

async def main():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(main())