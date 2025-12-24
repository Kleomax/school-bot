from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload

from ..database import async_engine, Base
from ..models import QuestionsModel, UserDataModel

from .dependencies import connection


class QuestionsRequests:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


    @staticmethod
    @connection
    async def add_question(
        session: AsyncSession,
        user_id: int,
        theme: str,
        question: str,
        nick: str,
        photo: str = "None",
    ) -> bool | None:

        user = await session.scalar(select(UserDataModel).where(UserDataModel.user_id == user_id))

        if not user:
            return None


        question = QuestionsModel(
            user=user,
            theme=theme,
            question=question,
            photo=photo,
            nick=nick,
        )

        session.add(question)
        await session.commit()


        return True


    @staticmethod
    @connection
    async def get_all_questions_by_theme(session: AsyncSession, theme: str) -> list[QuestionsModel]:
        """
        Функция для получения всех вопросов по определённой теме из базы данных

        :param theme: тема вопроса
        """

        result = await session.scalars(
            select(QuestionsModel)
            .where(QuestionsModel.theme == theme)
        )

        return result.all()
        

    @staticmethod
    @connection
    async def get_all_questions(session: AsyncSession) -> list:
        """
        Функция для получения вопроса (возвращает самый старый)
        """

        result = await session.scalar(select(QuestionsModel).options(selectinload(QuestionsModel.user)))

        if result != None:
            return [result.user.user_id, result.theme, result.question, result.photo, result.nick]


    @staticmethod
    @connection
    async def count_all_questions(session: AsyncSession) -> int:
        return await session.scalar(select(func.count(QuestionsModel.id)))


    @staticmethod
    @connection
    async def delete_question(session: AsyncSession,user_id: int,theme: str,qtn: str,photo: str) -> None:
        """Удаляет вопрос из базы данных"""

        await session.execute(delete(QuestionsModel)
            .where(
                QuestionsModel.theme == theme,
                QuestionsModel.question == qtn,
                QuestionsModel.photo == photo,
                QuestionsModel.user.has(UserDataModel.user_id == user_id)
            )
        )

        await session.commit()