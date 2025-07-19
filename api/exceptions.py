"""Custom exceptions for API."""
class NotFoundError(Exception):
    """There is no data."""

class AlreadyExistError(Exception):
    """Trying to add in database already existing data."""