from typing import Optional

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    listing_id: int = Field(index=True)
    student_id: int = Field(index=True)
    body: str
    created_at: str
