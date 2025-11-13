from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from .dependencies import intpk, created_at

from ..database import Base


class QuestionsModel(Base):
    __tablename__ = "questions"

    id: Mapped[intpk]
    user_id = mapped_column(BigInteger)
    theme: Mapped[str]
    question: Mapped[str]
    photo: Mapped[str]
    nick: Mapped[str]

    # created_at: Mapped[created_at]
