"""Listing CRUD, browse filters, messaging, and lifecycle transitions."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlmodel import Session, select

from app.database import engine
from app.models.listing import Listing
from app.models.message import Message
from app.services.housing_auth import get_user
from app.services.lifecycle import ACTIONS, apply_action, visible_to_students

ALLOWED_AREAS = {"st_augustine", "mount_hope"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_amenities(raw: str) -> list[str]:
    return [a.strip().lower() for a in (raw or "").split(",") if a.strip()]


def submit_listing(
    landlord_id: int,
    *,
    title: str,
    area: str,
    price: int,
    amenities: str,
    contact_phone: str,
    contact_email: str,
    photos: str = "",
) -> dict[str, Any]:
    user = get_user(landlord_id)
    if not user or user["role"] != "landlord":
        return {"ok": False, "error": "landlords only"}
    # DEFECT: area not restricted to ALLOWED_AREAS
    if price <= 0:
        return {"ok": False, "error": "price must be positive"}
    # DEFECT: empty amenities allowed

    with Session(engine) as session:
        listing = Listing(
            landlord_id=landlord_id,
            title=title,
            area=area,
            price=price,
            amenities=amenities,
            contact_phone=contact_phone,
            contact_email=contact_email,
            photos=photos,
            status="pending",
            flag_pending=1,
            flag_verified=0,
            flag_active=0,
            flag_rejected=0,
            created_at=_now(),
        )
        session.add(listing)
        session.commit()
        session.refresh(listing)
        return {"ok": True, "listing": listing.model_dump()}


def transition(actor_id: int, listing_id: int, action: str) -> dict[str, Any]:
    actor = get_user(actor_id)
    if not actor:
        return {"ok": False, "error": "unknown user"}
    if action not in ACTIONS:
        return {"ok": False, "error": f"action must be one of {ACTIONS}"}

    with Session(engine) as session:
        listing = session.get(Listing, listing_id)
        if listing is None:
            return {"ok": False, "error": "listing not found"}
        row = listing.model_dump()

        # Role gates (loose)
        if action in {"verify", "reject"} and actor["role"] != "admin":
            return {"ok": False, "error": "admin only"}
        if action in {"activate", "deactivate", "resubmit"} and actor["role"] not in {
            "landlord",
            "admin",
        }:
            return {"ok": False, "error": "landlord/admin only"}
        # DEFECT: any landlord can activate any listing (no ownership check)

        result = apply_action(row, action)
        if not result.get("ok"):
            return result

        updated = result["row"]
        listing.status = updated["status"]
        listing.flag_pending = updated["flag_pending"]
        listing.flag_verified = updated["flag_verified"]
        listing.flag_active = updated["flag_active"]
        listing.flag_rejected = updated["flag_rejected"]
        session.add(listing)
        session.commit()
        session.refresh(listing)
        return {"ok": True, "listing": listing.model_dump()}


def browse_for_students(
    student_id: int,
    *,
    area: str | None = None,
    max_price: int | None = None,
    amenity: str | None = None,
) -> dict[str, Any]:
    student = get_user(student_id)
    if not student or student["role"] != "student":
        return {"ok": False, "error": "students only"}
    # DEFECT: provisional / missing student_id not blocked

    with Session(engine) as session:
        rows = session.exec(select(Listing).order_by(Listing.id)).all()
        items = [r.model_dump() for r in rows]

    results = []
    for item in items:
        if not visible_to_students(item):
            continue
        if area and item["area"] != area:
            continue
        if max_price is not None and int(item["price"]) > max_price:
            continue
        # DEFECT: amenity filter is substring on raw string, case-sensitive sometimes
        if amenity and amenity not in item["amenities"]:
            continue
        results.append(item)
    return {"ok": True, "listings": results}


def list_all(*, status: str | None = None) -> list[dict[str, Any]]:
    with Session(engine) as session:
        stmt = select(Listing).order_by(Listing.id)
        if status:
            stmt = stmt.where(Listing.status == status)
        return [r.model_dump() for r in session.exec(stmt).all()]


def send_message(student_id: int, listing_id: int, body: str) -> dict[str, Any]:
    student = get_user(student_id)
    if not student or student["role"] != "student":
        return {"ok": False, "error": "students only"}
    if not body.strip():
        return {"ok": False, "error": "body required"}
    with Session(engine) as session:
        listing = session.get(Listing, listing_id)
        if listing is None:
            return {"ok": False, "error": "listing not found"}
        # DEFECT: can message pending/rejected listings
        message = Message(
            listing_id=listing_id,
            student_id=student_id,
            body=body,
            created_at=_now(),
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return {"ok": True, "message_id": message.id}
