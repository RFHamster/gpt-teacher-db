from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    CLASSROOM_TABLE,
    TEACHER_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom_student import ClassroomStudent
    from gpt_teacher_db.gpt_teacher.models.problem import Problem
    from gpt_teacher_db.gpt_teacher.models.teacher import Teacher


class Classroom(BaseModelGPTTeacher_, table=True):
    """Classroom grouping students under a teacher's responsibility"""

    __tablename__ = CLASSROOM_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    teacher_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{TEACHER_TABLE}.id",
        nullable=False,
        index=True,
    )
    name: str = Field(max_length=255, nullable=False)

    # Relationships
    teacher: "Teacher" = Relationship(back_populates="classrooms")
    classroom_students: list["ClassroomStudent"] = Relationship(
        back_populates="classroom"
    )
    problems: list["Problem"] = Relationship(back_populates="classroom")
