from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Date

from .dependencies import intpk, created_at

from ..database import Base


class UserDataModel(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    user_id = mapped_column(BigInteger)
    user_shift: Mapped[str] = mapped_column(nullable=True)
    user_class: Mapped[str] = mapped_column(nullable=True)
    signup: Mapped[str] = mapped_column(nullable=True)
    activity: Mapped[bool] = mapped_column(nullable=True)
    blocked: Mapped[bool] = mapped_column(nullable=True)

    last_activity = mapped_column(Date)
    created_at: Mapped[created_at]

    questions: Mapped[list["QuestionsModel"]] = relationship(
        back_populates="user"
    )
