import aioredis

from app.dependencies import get_settings


def init_redis_pool() -> aioredis.Redis:
    settings = get_settings()
    print(f"init_redis_pool(REDIS_URL: {settings.redis_url})...")
    return aioredis.from_url(
        f"{settings.redis_url}", encoding="utf-8", decode_responses=True
    )
