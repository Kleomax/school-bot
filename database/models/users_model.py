from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Date

from .dependencies import intpk, created_at

from ..database import Base


class UserDataModel(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    user_id = mapped_column(BigInteger)
    user_shift: Mapped[str]
    user_class: Mapped[str]
    signup: Mapped[str]
    activity: Mapped[str]
    blocked: Mapped[str]

    # last_activity = mapped_column(Date)
    # created_at: Mapped[created_at]
