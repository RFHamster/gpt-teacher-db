# Database Metadata
# Define your schemas and table names here

DEFAULT_SCHEMA_NAME: str = "gpt_teacher"

# Table name constants
TEACHER_TABLE = "teacher"
STUDENT_TABLE = "student"
CLASSROOM_TABLE = "classroom"
CLASSROOM_STUDENT_TABLE = "classroom_student"
PROBLEM_TABLE = "problem"
STUDENT_SESSION_TABLE = "student_session"
MESSAGE_TABLE = "chat_message"
CONSOLIDATED_TABLE = "consolidated"

# Add your table names here
all_tables = [
    TEACHER_TABLE,
    STUDENT_TABLE,
    CLASSROOM_TABLE,
    CLASSROOM_STUDENT_TABLE,
    PROBLEM_TABLE,
    STUDENT_SESSION_TABLE,
    MESSAGE_TABLE,
    CONSOLIDATED_TABLE,
]
