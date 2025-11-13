from __future__ import annotations
import asyncio
from aiogram.types import Message, TelegramObject
from aiogram import BaseMiddleware
from typing import Callable, Any, Awaitable, Union

from typing import *
from aiogram import BaseMiddleware
from aiogram.types import Message

from database import UsersRequests

from cachetools import TTLCache


class SomeMiddleware(BaseMiddleware):
    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        self.latency = latency
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: dict[str, Any]
    ) -> Any:
        if not message.media_group_id:
            await handler(message, data)
            return
        try:
            self.album_data[message.media_group_id].append(message)
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            data["_is_last"] = True

            data["album"] = self.album_data[message.media_group_id]

            await handler(message, data)


        if message.media_group_id and data.get("_is_last"):
            del self.album_data[message.media_group_id]
            del data["_is_last"]
            

class BlockUsers(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:

        if event.from_user.id in await UsersRequests.get_all_blocked_users():
            await event.answer("Вы были заблокированы администратором 😔")

            return
        else:
            return await handler(event, data)


class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self, time_limit: int | float) -> None:
        self.botCache = TTLCache(maxsize=20_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["TEST_DATA"] = 123456789
        user = dict(data["event_from_user"])

        if (user["id"] in await UsersRequests.get_all_blocked_users()) and (user["id"] in self.botCache):
            self.botCache = TTLCache(maxsize=20_000, ttl=20)
            return

        elif event.chat.id in self.botCache:
            return
        
        elif user["id"] in await UsersRequests.get_all_blocked_users():
            self.botCache[event.chat.id] = None

        return await handler(event, data)