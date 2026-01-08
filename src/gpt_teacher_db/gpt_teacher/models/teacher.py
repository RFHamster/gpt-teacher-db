from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_, SQLModelGPTTeacher
from gpt_teacher_db.gpt_teacher.metadata import TEACHER_TABLE

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom import Classroom


# Shared properties
class TeacherBase(SQLModelGPTTeacher):
    """Base model with common teacher properties"""

    email: str = Field(max_length=255)
    name: str = Field(max_length=255)


class Teacher(TeacherBase, BaseModelGPTTeacher_, table=True):
    """Teacher who creates classes and defines problems"""

    __tablename__ = TEACHER_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255, nullable=False)

    # Relationships
    classrooms: list["Classroom"] = Relationship(back_populates="teacher")


# Properties to receive on creation
class TeacherCreate(TeacherBase):
    """Model for creating a new teacher"""

    password: str = Field(min_length=8)


# Properties to receive on update
class TeacherUpdate(SQLModelGPTTeacher):
    """Model for updating a teacher"""

    email: Optional[str] = Field(default=None, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8)


# Properties to return via API
class TeacherPublic(TeacherBase):
    """Model for returning teacher data"""

    id: UUID
