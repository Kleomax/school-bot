<<<<<<< HEAD
from typing import TYPE_CHECKING

=======
>>>>>>> 45fa18f (add relation ship & change questions model)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from .dependencies import intpk, created_at

from ..database import Base

if TYPE_CHECKING:
    from .users_model import UserDataModel


class QuestionsModel(Base):
    __tablename__ = "questions"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    theme: Mapped[str]
    question: Mapped[str]
    photo: Mapped[str]
    nick: Mapped[str]

    created_at: Mapped[created_at]

    user: Mapped["UserDataModel"] = relationship(
        back_populates="questions"
    )
