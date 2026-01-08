from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_, SQLModelGPTTeacher
from gpt_teacher_db.gpt_teacher.core.base_model_json_conversor import PydanticField
from gpt_teacher_db.gpt_teacher.dto.consolidated_data import ConsolidatedData
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    CONSOLIDATED_TABLE,
    STUDENT_SESSION_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.student_session import StudentSession


# Shared properties
class ConsolidatedBase(SQLModelGPTTeacher):
    """Base model with common consolidated properties"""

    session_id: UUID
    data: ConsolidatedData


class Consolidated(ConsolidatedBase, BaseModelGPTTeacher_, table=True):
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
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{STUDENT_SESSION_TABLE}.id",
        unique=True,
        nullable=False,
        index=True,
    )

    # Structured data stored as JSONB for flexible queries
    data: ConsolidatedData = PydanticField(ConsolidatedData)

    # Relationships
    session: "StudentSession" = Relationship(back_populates="consolidated")


# Properties to receive on creation
class ConsolidatedCreate(ConsolidatedBase):
    """Model for creating a new consolidated"""

    pass


# Properties to receive on update
class ConsolidatedUpdate(SQLModelGPTTeacher):
    """Model for updating a consolidated"""

    session_id: Optional[UUID] = Field(default=None)
    data: Optional[ConsolidatedData] = Field(default=None)


# Properties to return via API
class ConsolidatedPublic(ConsolidatedBase):
    """Model for returning consolidated data"""

    id: UUID
