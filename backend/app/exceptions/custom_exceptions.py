"""
Custom exception classes matching Java exception hierarchy.
"""


class ResourceNotFoundException(Exception):
    """
    Matches Java ResourceNotFoundException.
    Raised when a requested resource (user, candidate, etc.) is not found.
    """
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class DuplicateResourceException(Exception):
    """
    Matches Java DuplicateResourceException.
    Raised when attempting to create a resource that already exists (e.g., duplicate email).
    """
    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)


class AccessDeniedCustomException(Exception):
    """
    Matches Java AccessDeniedCustomException.
    Raised for custom access denied scenarios beyond role checks.
    """
    def __init__(self, message: str = "Access denied"):
        self.message = message
        super().__init__(self.message)


class BadCredentialsException(Exception):
    """
    Matches Spring Security BadCredentialsException.
    Raised during login when credentials are invalid.
    """
    def __init__(self, message: str = "Invalid email or password"):
        self.message = message
        super().__init__(self.message)


class DisabledException(Exception):
    """
    Matches Spring Security DisabledException.
    Raised when user account is disabled.
    """
    def __init__(self, message: str = "This account has been disabled"):
        self.message = message
        super().__init__(self.message)
