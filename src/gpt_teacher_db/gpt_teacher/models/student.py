from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.gpt_teacher.metadata import STUDENT_TABLE

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom_student import ClassroomStudent
    from gpt_teacher_db.gpt_teacher.models.problem import Problem
    from gpt_teacher_db.gpt_teacher.models.session import Session


class Student(BaseModelGPTTeacher_, table=True):
    """Student who uses the VSCode extension to get help"""

    __tablename__ = STUDENT_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, nullable=False, index=True)
    password_hash: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=255, nullable=False)
    registration_number: Optional[str] = Field(default=None, max_length=50)

    # Relationships
    classroom_students: list["ClassroomStudent"] = Relationship(
        back_populates="student"
    )
    sessions: list["Session"] = Relationship(back_populates="student")
    sandbox_problems: list["Problem"] = Relationship(
        back_populates="created_by_student"
    )
