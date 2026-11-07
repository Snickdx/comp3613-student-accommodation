from typing import Optional

from sqlmodel import Field, SQLModel


class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    landlord_id: int = Field(index=True)
    title: str
    area: str
    price: int
    amenities: str = ""
    contact_phone: str
    contact_email: str
    photos: str = ""
    # Canonical lifecycle label (often drifts from flags below).
    status: str
    flag_pending: int = 1
    flag_verified: int = 0
    flag_active: int = 0
    flag_rejected: int = 0
    created_at: str
