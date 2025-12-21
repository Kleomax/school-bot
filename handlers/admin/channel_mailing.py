import asyncio
import aiogram
import time
import fontstyle

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums.parse_mode import ParseMode

from config import bot, admins_list, ProductionMode

from middleware import SomeMiddleware

from functions import mixed_fns

from markups import MainMenu


from database import UsersRequests


router = Router()

if ProductionMode == True:
    router.channel_post.filter(mixed_fns.ChatTypeFilter(["-1002352294131"]))
else:
    router.channel_post.filter(mixed_fns.ChatTypeFilter(["-1002496699343"]))


router.channel_post.middleware(SomeMiddleware())
@router.channel_post()
async def get_message(msg: Message,  album: list[Message] = None):

    user_list: list = await UsersRequests.get_all_users_id()

    successful_msgs = 0
    msgs = []

    if msg.media_group_id is not None:
        MessageType = "MediaGroup"

        if msg.caption == None:
            msg_text = ""
        else:
            msg_text = msg.caption

        media_group = MediaGroupBuilder(caption=f"<I>Последние новости школы 👀</I>\n\n{msg_text}")

        
        media_number = 0

        for msg1 in album:
            if msg1.photo:
                file_id = msg1.photo[-1].file_id
                media_group.add_photo(media=file_id, parse_mode=ParseMode.HTML)

            elif msg1.video:
                file_id = msg1.video.file_id
                media_group.add_video(media=file_id, parse_mode=ParseMode.HTML)


            media_number += 1

    for user in user_list:
        try:
            if MessageType == "MediaGroup":
                await bot.send_media_group(user, media_group.build())
            else:
                await bot.send_message(user, f"<I>Последние новости школы 👇</I>", parse_mode=ParseMode.HTML)
                await bot.forward_message(user, '-1002496699343', msg.message_id)

            await UsersRequests.update_activity(user_id=user, activity=True)

            msgs += f"{msg.message_id}/"
            successful_msgs += 1

        except aiogram.exceptions.TelegramForbiddenError as exc:
            print(fontstyle.apply(exc, 'bold/Italic/yellow'))

            await UsersRequests.update_activity(user_id=user, activity=False)

            time.sleep(0.1)

            continue
        
        except aiogram.exceptions.TelegramBadRequest as exce:
            print(fontstyle.apply(exce, 'bold/Italic/yellow'))

            await UsersRequests.update_activity(user_id=user, activity=True)

            time.sleep(0.1)

            continue

        except aiogram.exceptions.TelegramRetryAfter as ex:
            await asyncio.sleep(ex.retry_after)

            return await get_message(msg)
            
    for admin in admins_list:
        await bot.send_message(admin, 'Сообщения отправлены ✅', reply_markup=MainMenu(msg.from_user.id))
        await bot.send_message(admin, f'<I>[+] Кол-во отправленных сообщений: {successful_msgs}/{len(user_list)}</I>', parse_mode=ParseMode.HTML)

