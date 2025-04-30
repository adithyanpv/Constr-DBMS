import json
from typing import Any
from redis.asyncio import Redis

# Global Redis client instance
redis_client: Redis = None

# Connect to Redis
async def connect_to_redis(redis_url: str = "redis://localhost:6379"):
    global redis_client
    redis_client = Redis.from_url(redis_url, decode_responses=True)
    try:
        await redis_client.ping()
        print("✅ Connected to Redis")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        redis_client = None

# Disconnect from Redis
async def disconnect_from_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        print("🛑 Redis connection closed")
        redis_client = None

# Add employee to Redis (no expiry)
async def add_employee(key: str, employee_data: Any):
    if not redis_client:
        raise RuntimeError("Redis client is not connected.")
    await redis_client.set(key, json.dumps(employee_data))

# Add employee with expiry (in seconds)
async def add_employee_with_expiry(key: str, employee_data: Any, expiry_seconds: int):
    if not redis_client:
        raise RuntimeError("Redis client is not connected.")
    await redis_client.set(key, json.dumps(employee_data), ex=expiry_seconds)

# Get employee from Redis
async def get_employee(key: str) -> Any:
    if not redis_client:
        raise RuntimeError("Redis client is not connected.")
    cached_data = await redis_client.get(key)
    if cached_data:
        try:
            return json.loads(cached_data)
        except json.JSONDecodeError:
            return None
    return None

# Delete employee from Redis
async def delete_employee(key: str):
    if not redis_client:
        raise RuntimeError("Redis client is not connected.")
    await redis_client.delete(key)
