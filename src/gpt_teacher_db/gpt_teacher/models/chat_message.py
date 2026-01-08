from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import Column, Enum as SAEnum
from sqlmodel import Field, Relationship

from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_, SQLModelGPTTeacher
from gpt_teacher_db.gpt_teacher.enum import MessageType
from gpt_teacher_db.gpt_teacher.metadata import (
    DEFAULT_SCHEMA_NAME,
    MESSAGE_TABLE,
    STUDENT_SESSION_TABLE,
    PROBLEM_TABLE,
)

if TYPE_CHECKING:
    from gpt_teacher_db.gpt_teacher.models.problem import Problem
    from gpt_teacher_db.gpt_teacher.models.student_session import StudentSession


# Shared properties
class ChatMessageBase(SQLModelGPTTeacher):
    """Base model with common chat message properties"""

    session_id: UUID
    problem_id: UUID
    type: MessageType = MessageType.USER
    content: str
    code: Optional[str] = None
    code_review: Optional[str] = None


class ChatMessage(ChatMessageBase, BaseModelGPTTeacher_, table=True):
    """Message in a chat session - can be from user (student) or AI assistant

    Uses discriminator pattern with 'type' field:
    - type='user': Student's question + code
    - type='ai': AI's answer + code review

    Note: problem_id is denormalized (also accessible via session) to optimize queries
    """

    __tablename__ = MESSAGE_TABLE

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{STUDENT_SESSION_TABLE}.id",
        nullable=False,
        index=True,
    )
    problem_id: UUID = Field(
        foreign_key=f"{DEFAULT_SCHEMA_NAME}.{PROBLEM_TABLE}.id",
        nullable=False,
        index=True,
        description="Denormalized FK for query optimization",
    )
    type: MessageType = Field(
        sa_column=Column(
            SAEnum(MessageType, schema=DEFAULT_SCHEMA_NAME),
            default=MessageType.USER,
            index=True,
        ),
    )
    content: str = Field(
        sa_column=Column(sa.Text, nullable=False),
        description="Student's question OR AI's answer",
    )
    code: Optional[str] = Field(
        default=None,
        sa_column=Column(sa.Text, nullable=True),
        description="Code sent by student (for type='user')",
    )
    code_review: Optional[str] = Field(
        default=None,
        sa_column=Column(sa.Text, nullable=True),
        description="Code review by AI (for type='ai')",
    )

    # Relationships
    session: "StudentSession" = Relationship(back_populates="messages")
    problem: "Problem" = Relationship()


# Properties to receive on creation
class ChatMessageCreate(ChatMessageBase):
    """Model for creating a new chat message"""

    pass


# Properties to receive on update
class ChatMessageUpdate(SQLModelGPTTeacher):
    """Model for updating a chat message"""

    session_id: Optional[UUID] = Field(default=None)
    problem_id: Optional[UUID] = Field(default=None)
    type: Optional[MessageType] = Field(default=None)
    content: Optional[str] = Field(default=None)
    code: Optional[str] = Field(default=None)
    code_review: Optional[str] = Field(default=None)


# Properties to return via API
class ChatMessagePublic(ChatMessageBase):
    """Model for returning chat message data"""

    id: UUID
