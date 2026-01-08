from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_, SQLModelGPTTeacher
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    CLASSROOM_TABLE,
    TEACHER_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom_student import ClassroomStudent
    from gpt_teacher_db.gpt_teacher.models.problem import Problem
    from gpt_teacher_db.gpt_teacher.models.teacher import Teacher


# Shared properties
class ClassroomBase(SQLModelGPTTeacher):
    """Base model with common classroom properties"""

    name: str = Field(max_length=255)
    teacher_id: UUID


class Classroom(ClassroomBase, BaseModelGPTTeacher_, table=True):
    """Classroom grouping students under a teacher's responsibility"""

    __tablename__ = CLASSROOM_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    teacher_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{TEACHER_TABLE}.id",
        nullable=False,
        index=True,
    )

    # Relationships
    teacher: "Teacher" = Relationship(back_populates="classrooms")
    classroom_students: list["ClassroomStudent"] = Relationship(
        back_populates="classroom"
    )
    problems: list["Problem"] = Relationship(back_populates="classroom")


# Properties to receive on creation
class ClassroomCreate(ClassroomBase):
    """Model for creating a new classroom"""

    pass


# Properties to receive on update
class ClassroomUpdate(SQLModelGPTTeacher):
    """Model for updating a classroom"""

    name: Optional[str] = Field(default=None, max_length=255)
    teacher_id: Optional[UUID] = Field(default=None)


# Properties to return via API
class ClassroomPublic(ClassroomBase):
    """Model for returning classroom data"""

    id: UUID
