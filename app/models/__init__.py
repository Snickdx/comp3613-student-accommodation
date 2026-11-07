"""Database table models.

Import every table model here so ``SQLModel.metadata.create_all`` sees them.
"""

from app.models.listing import Listing
from app.models.message import Message
from app.models.user import User

__all__ = [
    "User",
    "Listing",
    "Message",
]
