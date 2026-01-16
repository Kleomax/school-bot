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

    def __init__(self, latency: Union[int, float] = 0.5):
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
        if await UsersRequests.check_user_block(event.from_user.id):
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
        user = dict(data["event_from_user"])

        if (await UsersRequests.check_user_block(user["id"]) == True) and (user["id"] in self.botCache):
            self.botCache = TTLCache(maxsize=20_000, ttl=20)
            return

        elif event.chat.id in self.botCache:
            return
        
        elif await UsersRequests.check_user_block(user["id"]):
            self.botCache[event.chat.id] = None

        return await handler(event, data)