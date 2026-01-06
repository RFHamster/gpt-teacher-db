from sqlmodel import Field
from gpt_teacher_db.gpt_teacher.core import BaseModelGPTTeacher_


class ExampleModel(BaseModelGPTTeacher_, table=True):
    """Example model for reference"""

    __tablename__ = "gpt_teacher_example"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
