from typing import Coroutine

from ..database import async_session


def connection(func: Coroutine):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                return await func(session, *args, **kwargs)
            except Exception:
                await session.rollback()
                raise
    return wrapper
