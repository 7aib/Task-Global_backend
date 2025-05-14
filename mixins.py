from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Boolean
from datetime import datetime


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
