from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.gpt_teacher.metadata import TEACHER_TABLE

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.classroom import Classroom


class Teacher(BaseModelGPTTeacher_, table=True):
    """Teacher who creates classes and defines problems"""

    __tablename__ = TEACHER_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, nullable=False, index=True)
    password_hash: str = Field(max_length=255, nullable=False)
    name: str = Field(max_length=255, nullable=False)

    # Relationships
    classrooms: list["Classroom"] = Relationship(back_populates="teacher")
