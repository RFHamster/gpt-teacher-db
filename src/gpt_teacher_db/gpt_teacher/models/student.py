from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_, SQLModelGPTTeacher
from gpt_teacher_db.gpt_teacher.metadata import STUDENT_TABLE

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom_student import ClassroomStudent
    from gpt_teacher_db.gpt_teacher.models.problem import Problem
    from gpt_teacher_db.gpt_teacher.models.student_session import StudentSession


# Shared properties
class StudentBase(SQLModelGPTTeacher):
    """Base model with common student properties"""

    email: str = Field(max_length=255)
    name: str = Field(max_length=255)
    registration_number: Optional[str] = Field(default=None, max_length=50)


class Student(StudentBase, BaseModelGPTTeacher_, table=True):
    """Student who uses the VSCode extension to get help"""

    __tablename__ = STUDENT_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str = Field(max_length=255, nullable=False)

    # Relationships
    classroom_students: list["ClassroomStudent"] = Relationship(
        back_populates="student"
    )
    sessions: list["StudentSession"] = Relationship(back_populates="student")
    sandbox_problems: list["Problem"] = Relationship(
        back_populates="created_by_student"
    )


# Properties to receive on creation
class StudentCreate(StudentBase):
    """Model for creating a new student"""

    password: str = Field(min_length=8)


# Properties to receive on update
class StudentUpdate(SQLModelGPTTeacher):
    """Model for updating a student"""

    email: Optional[str] = Field(default=None, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    registration_number: Optional[str] = Field(default=None, max_length=50)
    password: Optional[str] = Field(default=None, min_length=8)


# Properties to return via API
class StudentPublic(StudentBase):
    """Model for returning student data"""

    id: UUID
