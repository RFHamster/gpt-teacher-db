from typing import Optional
from pydantic import BaseModel, Field


class ConsolidatedData(BaseModel):
    """Structured data from AI analysis of a study session

    This structure is stored as JSONB in the database to allow flexible queries
    like "find students who struggled with concept X" or "sessions with difficulty > 7"
    """

    tags: list[str] = Field(
        default_factory=list,
        description="Technical tags (e.g., 'loops', 'arrays', 'functions', 'recursion')",
    )

    concepts: list[str] = Field(
        default_factory=list,
        description="Programming concepts identified (e.g., 'iteration', 'indexing', 'scope')",
    )

    error_patterns: list[str] = Field(
        default_factory=list,
        description="Common error patterns found (e.g., 'index out of bounds', 'null pointer', 'syntax error')",
    )

    difficulty_score: Optional[int] = Field(
        default=None,
        ge=1,
        le=10,
        description="AI-assessed difficulty level (1=easy, 10=very hard)",
    )

    summary: Optional[str] = Field(
        default=None,
        description="Brief summary of the student's main difficulties in this session",
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="AI recommendations for the teacher (e.g., 'Review array indexing', 'Focus on loop logic')",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tags": ["loops", "arrays", "debugging"],
                "concepts": ["iteration", "indexing", "boundary conditions"],
                "error_patterns": ["index out of bounds", "off-by-one error"],
                "difficulty_score": 7,
                "summary": "Student struggled with array indexing and boundary conditions in loops",
                "recommendations": [
                    "Review array indexing basics",
                    "Practice loop boundary conditions",
                    "Introduce debugger usage",
                ],
            }
        }
