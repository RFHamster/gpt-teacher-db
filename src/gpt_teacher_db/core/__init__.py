from datetime import datetime

import pytz


def current_datetime() -> datetime:
    """
    Returns the current datetime in UTC timezone.

    This function centralizes timezone handling across the application.

    Returns:
        datetime: Current datetime in UTC timezone
    """
    return datetime.now(tz=pytz.UTC)
