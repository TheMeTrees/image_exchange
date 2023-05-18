from .base_exception import BaseError


class ImageNotFoundError(BaseError):
    """Raised when the specified image cannot be found."""

    def __init__(self, path):
        super().__init__(f"Image not found at {path}")
        self.path = path
