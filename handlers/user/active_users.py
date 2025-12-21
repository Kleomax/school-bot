from aiogram import Router

from aiogram.filters import IS_MEMBER, ChatMemberUpdatedFilter, KICKED
from aiogram.types import ChatMemberUpdated

from database import UsersRequests

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):

    await UsersRequests.update_activity(user_id=event.chat.id, activity=False)

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER))
async def user_comeback(event: ChatMemberUpdated):

    await UsersRequests.update_activity(user_id=event.chat.id, activity=True)
    await UsersRequests.update_last_activity(user_id=event.chat.id)


    
