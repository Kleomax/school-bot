import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, func, delete
from sqlalchemy.sql import exists

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
    async def add_question(session: AsyncSession, user_id: int, theme: str, question: str, nick: str, photo: str = "None") -> bool | None:

        """Функция для добавление вопроса в базу данных

        :param user_id: id пользователя
        :param theme: тема вопроса
        :param question: вопрос пользователя
        :param nick: имя пользователя в telegram
        :param photo: id прикреплённого фото к вопросу

        """

        user_exist = await session.scalar(
            exists()
            .where(UserDataModel.user_id == user_id)
            .select()
        )

        if user_exist:
            question = QuestionsModel(
                user_id=user_id,
                theme=theme,
                question=question,
                photo=photo,
                nick=nick,
            )

            session.add(question)

            await session.commit()
            await session.close()

            return True

    @staticmethod
    @connection
    async def get_all_questions_by_theme(session: AsyncSession, theme: str) -> list:
        """
        Функция для получения всех вопросов по определённой теме из базы данных

        :param theme: тема вопроса
        """

        all_questions_by_theme = await session.scalars(select(QuestionsModel).where(QuestionsModel.theme == theme))
        result = all_questions_by_theme.all()

        await session.close()

        return result

    @staticmethod
    @connection
    async def get_all_questions(session: AsyncSession) -> list:
        """
        Функция для получения всех вопросов из базы данных
        """

        all_questions= await session.scalar(select(QuestionsModel))

        if all_questions != None:
            result = [all_questions.user_id, all_questions.theme, all_questions.question, all_questions.photo, all_questions.nick] 

            await session.close()

            return result

    @staticmethod
    @connection
    async def count_all_questions(session: AsyncSession) -> int:
        """Возвращает общее кол-во вопросов"""

        all_questions= await session.scalar(func.count(QuestionsModel.id))

        await session.close()

        return all_questions

    @staticmethod
    @connection
    async def delete_question(session: AsyncSession, user_id: int, theme: str, qtn: str, photo: str) -> None:
        """Удаляет вопрос из базы данных"""

        await session.execute(delete(QuestionsModel).where(
                QuestionsModel.user_id == user_id,
                QuestionsModel.theme == theme,
                QuestionsModel.question == qtn,
                QuestionsModel.photo == photo
            )
        )

        await session.commit()
        await session.close()