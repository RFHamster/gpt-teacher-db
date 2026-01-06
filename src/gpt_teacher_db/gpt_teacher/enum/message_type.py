from enum import Enum


class MessageType(str, Enum):
    """Type of message in a chat session"""

    USER = "user"  # Message from student
    AI = "ai"  # Message from AI assistant
