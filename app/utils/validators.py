from datetime import datetime


def validate_time_format(time_str: str, expected_format: str = "%Y-%m-%dT%H:%M:%S") -> datetime:
    """
    Validates and converts a string to a datetime object based on the given format.

    Args:
        time_str (str): The time string to validate.
        expected_format (str): The expected datetime format.

    Returns:
        datetime: The validated datetime object.

    Raises:
        ValueError: If the time format is invalid.
    """
    try:
        return datetime.strptime(time_str, expected_format)
    except ValueError:
        raise ValueError(f"Time must be in the format '{expected_format}'")


def validate_time_range(from_time: str, to_time: str, format: str = "%Y-%m-%dT%H:%M:%S"):
    """
    Validates that 'from_time' is less than 'to_time'.

    Args:
        from_time (str): The start time.
        to_time (str): The end time.
        format (str): The expected datetime format.

    Raises:
        ValueError: If 'from_time' is greater than 'to_time'.
    """
    from_dt = validate_time_format(from_time, format)
    to_dt = validate_time_format(to_time, format)
    if from_dt > to_dt:
        raise ValueError("'from_time' should be less than 'to_time'")
