from typing import TYPE_CHECKING, Optional
from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.core import current_datetime
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    CLASSROOM_STUDENT_TABLE,
    CLASSROOM_TABLE,
    STUDENT_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom import Classroom
    from gpt_teacher_db.gpt_teacher.models.student import Student


class ClassroomStudent(BaseModelGPTTeacher_, table=True):
    """Associative table for N:N relationship between Classroom and Student"""

    __tablename__ = CLASSROOM_STUDENT_TABLE

    classroom_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{CLASSROOM_TABLE}.id", primary_key=True
    )
    student_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{STUDENT_TABLE}.id", primary_key=True
    )
    joined_at: Optional[datetime] = Field(
        default_factory=current_datetime, nullable=True
    )

    # Relationships
    classroom: "Classroom" = Relationship(back_populates="classroom_students")
    student: "Student" = Relationship(back_populates="classroom_students")
