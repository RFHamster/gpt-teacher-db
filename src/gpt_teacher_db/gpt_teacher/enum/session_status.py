from enum import Enum


class SessionStatus(str, Enum):
    """Status of a study session"""

    OPEN = "open"
    CLOSED = "closed"
