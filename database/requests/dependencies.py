from typing import Coroutine

from ..database import async_session


def connection(func: Coroutine):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper
