"""Student-accommodation scenario JSON API (OpenAPI /docs)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.services import housing_auth as auth
from app.services import listings

router = APIRouter(tags=["student-accommodation"])


class LoginBody(BaseModel):
    email: str
    password: str


class ListingBody(BaseModel):
    title: str
    area: str
    price: int
    amenities: str = ""
    contact_phone: str
    contact_email: str
    photos: str = ""


class TransitionBody(BaseModel):
    action: str = Field(
        description="verify | reject | activate | deactivate | resubmit"
    )


class MessageBody(BaseModel):
    listing_id: int
    body: str


def _actor_id(x_user_id: str | None) -> int:
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-Id header required")
    try:
        return int(x_user_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="X-User-Id must be int") from exc


@router.post("/auth/login")
def login(body: LoginBody) -> dict[str, Any]:
    user = auth.login(body.email, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return {"user": user}


@router.post("/landlord/listings")
def submit(
    body: ListingBody, x_user_id: str | None = Header(default=None)
) -> dict[str, Any]:
    result = listings.submit_listing(
        _actor_id(x_user_id),
        title=body.title,
        area=body.area,
        price=body.price,
        amenities=body.amenities,
        contact_phone=body.contact_phone,
        contact_email=body.contact_email,
        photos=body.photos,
    )
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.post("/listings/{listing_id}/transition")
def transition(
    listing_id: int,
    body: TransitionBody,
    x_user_id: str | None = Header(default=None),
) -> dict[str, Any]:
    result = listings.transition(_actor_id(x_user_id), listing_id, body.action)
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result


@router.get("/student/listings")
def browse(
    area: str | None = None,
    max_price: int | None = None,
    amenity: str | None = None,
    x_user_id: str | None = Header(default=None),
) -> dict[str, Any]:
    result = listings.browse_for_students(
        _actor_id(x_user_id), area=area, max_price=max_price, amenity=amenity
    )
    if not result.get("ok"):
        raise HTTPException(status_code=403, detail=result.get("error"))
    return result


@router.get("/admin/listings")
def admin_list(
    status: str | None = None, x_user_id: str | None = Header(default=None)
) -> dict[str, Any]:
    actor = auth.get_user(_actor_id(x_user_id))
    if not actor or actor["role"] != "admin":
        raise HTTPException(status_code=403, detail="admin only")
    return {"listings": listings.list_all(status=status)}


@router.post("/student/messages")
def message(
    body: MessageBody, x_user_id: str | None = Header(default=None)
) -> dict[str, Any]:
    result = listings.send_message(
        _actor_id(x_user_id), body.listing_id, body.body
    )
    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return result
