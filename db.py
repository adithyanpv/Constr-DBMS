'''import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
#from fastapi import FastAPI

db_pool =  None

async def connect_to_db():
    global db_pool
    DATABASE_URL = os.getenv("DATABASE_URL")
    db_pool = await asyncpg.create_pool(DATABASE_URL) 
async def disconnect_from_db():
    await db_pool.close()'''
'''
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

db_pool = None

async def connect_to_db():
    global db_pool
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set in environment variables.")
    db_pool = await asyncpg.create_pool(DATABASE_URL)

async def disconnect_from_db():
    global db_pool
    if db_pool is not None:
        await db_pool.close()
        db_pool = None'''

import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

# Debugging step: print the loaded DATABASE_URL
print("Loaded DATABASE_URL:", os.getenv("DATABASE_URL"))

db_pool = None

async def connect_to_db():
    global db_pool
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set in environment variables.")
    db_pool = await asyncpg.create_pool(DATABASE_URL)

async def disconnect_from_db():
    global db_pool
    if db_pool is not None:
        await db_pool.close()
        db_pool = None

def get_db_pool():
    global db_pool
    if db_pool is None:
        raise RuntimeError("Database connection is not initialized.")
    return db_pool

