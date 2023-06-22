import json
from datetime import datetime

from aioredis import Redis


class RedisClient:
    def __init__(self, redis_session: Redis, repos_page_ex, keys_prefix="popular-github-repos"):
        self._redis_session = redis_session
        self._repos_page_ex = repos_page_ex
        self._repos_list_key = f"{keys_prefix}:repos-list"

    @staticmethod
    def _data_parser(data: dict):
        for key, val in data.items():
            if isinstance(val, str) and val.endswith("+00:00"):
                try:
                    data[key] = datetime.fromisoformat(val)
                except Exception as ex:  # noqa: E722
                    print(ex)
        return data

    async def get_repositories(self, url: str) -> dict | None:
        key = f"{self._repos_list_key}:{url}"
        respos_data = await self._redis_session.get(key)
        if not respos_data:
            print(f"Cache miss for key: '{key}'")
            return None

        print(f"Cache hit for key: '{key}'")
        return json.loads(respos_data, object_hook=self._data_parser)

    async def cache_repositories(self, url: str, repositories_data: dict):
        key = f"{self._repos_list_key}:{url}"
        return await self._redis_session.set(
            key,
            json.dumps(
                repositories_data,
                default=lambda value: value.isoformat()
                if isinstance(value, datetime)
                else value,
            ),
            ex=self._repos_page_ex,
        )
