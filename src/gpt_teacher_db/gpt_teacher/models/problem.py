from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import Column
from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    PROBLEM_TABLE,
    CLASSROOM_TABLE,
    STUDENT_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom import Classroom
    from gpt_teacher_db.gpt_teacher.models.session import Session
    from gpt_teacher_db.gpt_teacher.models.student import Student


class Problem(BaseModelGPTTeacher_, table=True):
    """Programming problem/exercise defined by teacher or created by student (sandbox)"""

    __tablename__ = PROBLEM_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    classroom_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{CLASSROOM_TABLE}.id",
        nullable=False,
        index=True,
    )
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(
        default=None, sa_column=Column(sa.Text, nullable=True)
    )
    file_path: Optional[str] = Field(
        default=None, max_length=500, description="Path to PDF or other files"
    )
    is_sandbox: bool = Field(
        default=False,
        nullable=False,
        description="True if created by student for triage",
    )
    created_by_student_id: Optional[UUID] = Field(
        default=None,
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{STUDENT_TABLE}.id",
        nullable=True,
        description="Student who created this sandbox problem",
    )

    # Relationships
    classroom: "Classroom" = Relationship(back_populates="problems")
    created_by_student: Optional["Student"] = Relationship(
        back_populates="sandbox_problems"
    )
    sessions: list["Session"] = Relationship(back_populates="problem")
