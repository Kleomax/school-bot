import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, func
from sqlalchemy.sql import exists

from ..database import async_engine, Base
from ..models import UserDataModel

from .dependencies import connection


class UsersRequests:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    @connection
    async def insert_user(session: AsyncSession, user_id: int) -> bool | None:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if not user_exist:
            user = UserDataModel(
                user_id=user_id,
            )

            session.add(user)

            await session.commit()

            return True
    
    @staticmethod
    @connection
    async def create_user(session: AsyncSession, user_id: int, user_shift: str, user_class: str) -> bool | None:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if not user_exist:
            user = UserDataModel(
                user_id=user_id,
                user_shift=user_shift,
                user_class=user_class,
                signup="done",
                activity=True,
                blocked=False,
                last_activity=datetime.datetime.now().date()
            )

            session.add(user)

            await session.commit()

            return True

    @staticmethod
    @connection
    async def check_user_exists(session: AsyncSession, user_id: int) -> bool:
        """Проверяет, существует ли пользователь в базе данных"""

        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        return user_exist

    @staticmethod
    @connection
    async def get_user_tg_id(session: AsyncSession, user_id: int):
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.id == user_id)
            .select()
        )

        if user_exist:
            return await session.scalar(select(UserDataModel).where(UserDataModel.id == user_id))

        await session.commit()

    @staticmethod
    @connection
    async def update_user_shift(session: AsyncSession, user_id: int, user_shift: str) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(UserDataModel.user_id == user_id).values(user_shift=user_shift)

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def update_user_class(session: AsyncSession, user_id: int, user_class: str) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(UserDataModel.user_id == user_id).values(user_class=user_class)

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def update_signup(session: AsyncSession, user_id: int, signup: str) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(UserDataModel.user_id == user_id).values(signup=signup)

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def update_activity(session: AsyncSession, user_id: int, activity: str) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(UserDataModel.user_id == user_id).values(activity=activity)

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def update_last_activity(session: AsyncSession, user_id: int) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(UserDataModel.user_id == user_id).values(activity=True, last_activity=datetime.datetime.now().date())

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def block_user(session: AsyncSession, user_id: int) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(UserDataModel.user_id ==user_id).values(activity=False, blocked=True)

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def unblock_user(session: AsyncSession, user_id: int, activity: bool) -> bool:
        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            query = update(UserDataModel).where(
                UserDataModel.user_id == user_id).values(activity=activity, blocked=False)

            await session.execute(query)
            await session.commit()

        return user_exist

    @staticmethod
    @connection
    async def count_all_users(session: AsyncSession) -> int:
        """Возвращает общее кол-во пользователей"""

        all_users = await session.scalar(func.count(UserDataModel.user_id))

        return all_users

    @staticmethod
    @connection
    async def get_all_users_id(session: AsyncSession) -> list[int]:
        "Возвращает user_id заблокированных пользователей в виде списка\n\nПример: [123456779, 156262860, 122346267]"

        users = await session.scalars(select(UserDataModel.user_id))

        result = users.all()

        return result

    @staticmethod
    @connection
    async def get_shift(session: AsyncSession, user_id: int) -> str:
        """Возвращает смену, в которую учиться пользователь"""

        shift = await session.scalar(select(UserDataModel.user_shift).where(UserDataModel.user_id == user_id))

        return shift

    @staticmethod
    @connection
    async def get_class(session: AsyncSession, user_id: int) -> str:
        """Возвращает класс, в котором учиться пользователь"""

        user_class = await session.scalar(select(UserDataModel.user_class).where(UserDataModel.user_id == user_id))

        return user_class


    @staticmethod
    @connection
    async def get_all_active_users(session: AsyncSession) -> int:
        """Возвращает общее кол-во пользователей у которых бот не заблокирован и аккаунт пользователя ещё существует"""

        all_activity_users = await session.scalars(select(UserDataModel.user_id).where(UserDataModel.activity == True))

        return len(all_activity_users.all())

    @staticmethod
    @connection
    async def get_new_users_in_delta(session: AsyncSession, delta: int) -> int:
        """Возвращает кол-во новых пользователей за определённое кол-во дней"""

        threshold_date = datetime.datetime.now() - datetime.timedelta(days=delta)

        new_users_in_delta = await session.scalars(select(UserDataModel.user_id).where(UserDataModel.created_at >= threshold_date))

        return len(new_users_in_delta.all())

    @staticmethod
    @connection
    async def get_activity_users_in_delta(session: AsyncSession, delta: int) -> int:
        """Возвращает кол-во активных пользователей за определённое кол-во дней"""

        threshold_date = datetime.datetime.now() - datetime.timedelta(days=delta)

        activity_users_in_delta = await session.scalars(select(UserDataModel).where(UserDataModel.activity == True, (UserDataModel.last_activity >= threshold_date)))

        return len(activity_users_in_delta.all())

    @staticmethod
    @connection
    async def check_user_block(session: AsyncSession, user_id: int) -> bool:
        """Проверяет, заблокирован ли пользователь\n\nTrue - Заблокирован\n\nFalse - Не заблокирован"""

        check = await session.scalar(select(UserDataModel.blocked).where(UserDataModel.user_id == user_id))

        return check

    @staticmethod
    @connection
    async def get_all_blocked_users(session: AsyncSession) -> list[int]:
        "Возвращает user_id заблокированных пользователей в виде списка\n\nПример: [123456779, 156262860, 122346267]"

        blocked_users = await session.scalars(select(UserDataModel.user_id).where(UserDataModel.blocked == True))

        result = blocked_users.all()

        return result
