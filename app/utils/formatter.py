from datetime import datetime


def format_datetime(dt, datetime_format: str = "%Y-%m-%dT%H:%M:%S") -> str:
    """
    Formats a datetime object into a string based on the given format.

    Args:
        dt (datetime): The datetime object to format.
        datetime_format (str): The desired format.

    Returns:
        str: The formatted datetime string.
    """
    return dt.strftime(datetime_format)
