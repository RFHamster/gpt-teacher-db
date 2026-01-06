from typing import TYPE_CHECKING, Optional
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship
from sqlalchemy import Column, Enum as SAEnum

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_
from gpt_teacher_db.gpt_teacher.enum import SessionStatus
from gpt_teacher_db.core import current_datetime
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    SESSION_TABLE,
    STUDENT_TABLE,
    PROBLEM_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.consolidated import Consolidated
    from gpt_teacher_db.gpt_teacher.models.message import Message
    from gpt_teacher_db.gpt_teacher.models.problem import Problem
    from gpt_teacher_db.gpt_teacher.models.student import Student


class Session(BaseModelGPTTeacher_, table=True):
    """Study session where student interacts with AI assistant for a specific problem

    Business Rule: Each student can have at most ONE session with status='open' at a time.
    When opening a new session, the previous one must be closed automatically.
    """

    __tablename__ = SESSION_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{STUDENT_TABLE}.id",
        nullable=False,
        index=True,
    )
    problem_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{PROBLEM_TABLE}.id",
        nullable=False,
        index=True,
    )
    status: SessionStatus = Field(
        sa_column=Column(
            SAEnum(SessionStatus, schema=DEFAULT_SCHEMA_NAME),
            default=SessionStatus.OPEN,
            index=True,
        ),
    )
    started_at: Optional[datetime] = Field(
        default_factory=current_datetime, nullable=True
    )
    closed_at: Optional[datetime] = Field(default=None, nullable=True)

    # Relationships
    student: "Student" = Relationship(back_populates="sessions")
    problem: "Problem" = Relationship(back_populates="sessions")
    messages: list["Message"] = Relationship(back_populates="session")
    consolidated: Optional["Consolidated"] = Relationship(
        back_populates="session", sa_relationship_kwargs={"uselist": False}
    )
