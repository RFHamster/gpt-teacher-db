import typing as t
from datetime import datetime

from sqlmodel import TIMESTAMP, Field, MetaData, SQLModel, text

from gpt_teacher_db.gpt_teacher.metadata import DEFAULT_SCHEMA_NAME
from gpt_teacher_db.core import current_datetime
from gpt_teacher_db.core.constants import convention


class SQLModelGPTTeacher(SQLModel):
    metadata = MetaData(schema=DEFAULT_SCHEMA_NAME, naming_convention=convention)


class BaseModelGPTTeacher_(SQLModelGPTTeacher):
    created_at: t.Optional[datetime] = Field(
        default_factory=current_datetime, nullable=True
    )

    # https://github.com/fastapi/sqlmodel/discussions/743
    updated_at: t.Optional[datetime] = Field(
        sa_type=type(TIMESTAMP(timezone=True)),
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "server_onupdate": text("CURRENT_TIMESTAMP"),
        },
        nullable=True,
        default_factory=current_datetime,
    )
    deleted_at: t.Optional[datetime] = Field(nullable=True, default=None)
    is_deleted: t.Optional[bool] = Field(nullable=True, default=False)
