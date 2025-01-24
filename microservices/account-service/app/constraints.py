from datetime import datetime
from typing import Annotated
from sqlalchemy import func, BigInteger, SmallInteger
from sqlalchemy.orm import mapped_column
from pydantic import StringConstraints


small_serial_pk = Annotated[int , mapped_column(SmallInteger, primary_key=True, autoincrement=True)]
big_serial_pk = Annotated[int, mapped_column(BigInteger, primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]

varchar_20 = Annotated[str, StringConstraints(min_length=20, max_length=20)]
