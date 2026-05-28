# reaper/exceptions.py

"""
Custom exceptions for the Reaper Realtor.com GraphQL client.
"""

class RealtorError(Exception):
    """Base exception for all Realtor.com client errors."""
    pass

class RealtorRequestError(RealtorError):
    """Exception raised when a request to Realtor.com fails (e.g. connection timeout)."""
    pass

class RealtorAPIError(RealtorError):
    """Exception raised when the Realtor.com API returns errors in the GraphQL response."""
    def __init__(self, message: str, errors: list[dict] | None = None):
        super().__init__(message)
        self.errors = errors or []

class RealtorAuthenticationError(RealtorError):
    """Exception raised when the request is rejected with a 403 or similar block."""
    pass
