from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import USER, PASSWORD, HOST, DB_NAME

async_engine = create_async_engine(
    url=f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{DB_NAME}",
    # echo=True,
)

async_session = async_sessionmaker(async_engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass
