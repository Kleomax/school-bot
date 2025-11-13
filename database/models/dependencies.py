import datetime

from typing import Annotated

from sqlalchemy import MetaData, Date, func
from sqlalchemy.orm import mapped_column


metadata_obj = MetaData()

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime.date, mapped_column(Date, server_default=func.current_date())]

