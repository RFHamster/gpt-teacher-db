from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.gpt_teacher.core.base_model_json_conversor import PydanticField
from gpt_teacher_db.gpt_teacher.dto.consolidated_data import ConsolidatedData
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    CONSOLIDATED_TABLE,
    SESSION_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.session import Session


class Consolidated(BaseModelGPTTeacher_, table=True):
    """AI-generated consolidation of a study session

    Generated automatically when a session is closed.
    Contains structured analysis (stored as JSONB) to enable teacher queries like:
    - "Students who struggled with concept X"
    - "Sessions with difficulty > 7"
    - "Most common error patterns in class Y"
    """

    __tablename__ = CONSOLIDATED_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{SESSION_TABLE}.id",
        unique=True,
        nullable=False,
        index=True,
    )

    # Structured data stored as JSONB for flexible queries
    data: ConsolidatedData = PydanticField(ConsolidatedData)

    # Relationships
    session: "Session" = Relationship(back_populates="consolidated")
