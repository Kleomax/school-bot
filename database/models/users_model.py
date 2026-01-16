<<<<<<< HEAD
from typing import TYPE_CHECKING

=======
>>>>>>> 45fa18f (add relation ship & change questions model)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Date

from .dependencies import intpk, created_at

from ..database import Base

if TYPE_CHECKING:
    from .questions_model import QuestionsModel


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

<<<<<<< HEAD
    questions: Mapped[list["QuestionsModel"]] = relationship( 
=======
    questions: Mapped[list["QuestionsModel"]] = relationship(
>>>>>>> 45fa18f (add relation ship & change questions model)
        back_populates="user"
    )
