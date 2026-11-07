"""Seed admin, students, landlords, and sample listings."""

from __future__ import annotations

from sqlmodel import Session, select

from app.database import drop_all, engine, ensure_db_and_tables
from app.models.listing import Listing
from app.models.user import User
from app.utilities.security import encrypt_password

USERS = [
    # username, email, password, role, display_name, student_id, provisional
    ("admin", "admin@example.com", "admin-dev", "admin", "Campus Admin", None, 0),
    (
        "student",
        "student@example.com",
        "stud-dev",
        "student",
        "Registered Student",
        "202012345",
        0,
    ),
    (
        "incoming",
        "incoming@example.com",
        "stud-dev",
        "student",
        "Provisional Incoming",
        None,
        1,
    ),
    ("landlord", "landlord@example.com", "land-dev", "landlord", "Landlord One", None, 0),
    (
        "landlord2",
        "landlord2@example.com",
        "land-dev",
        "landlord",
        "Landlord Two",
        None,
        0,
    ),
]


def seed(*, reset: bool = False) -> None:
    import app.models  # noqa: F401

    if reset:
        try:
            drop_all()
        except Exception:
            pass
    ensure_db_and_tables()

    with Session(engine) as session:
        existing = session.exec(select(User)).first()
        if existing and not reset:
            return

        for username, email, password, role, name, sid, prov in USERS:
            session.add(
                User(
                    username=username,
                    email=email,
                    password=encrypt_password(password),
                    role=role,
                    display_name=name,
                    student_id=sid,
                    provisional=prov,
                )
            )
        session.commit()

        landlord = session.exec(
            select(User).where(User.email == "landlord@example.com")
        ).one()

        session.add_all(
            [
                Listing(
                    landlord_id=landlord.id,
                    title="Verified Active Flat",
                    area="st_augustine",
                    price=3500,
                    amenities="wifi,parking",
                    contact_phone="555-0100",
                    contact_email="landlord@example.com",
                    photos="photo1.jpg",
                    status="active",
                    flag_pending=0,
                    flag_verified=1,
                    flag_active=1,
                    flag_rejected=0,
                    created_at="2099-01-01T10:00:00+00:00",
                ),
                Listing(
                    landlord_id=landlord.id,
                    title="Pending Unit",
                    area="mount_hope",
                    price=2800,
                    amenities="wifi",
                    contact_phone="555-0101",
                    contact_email="landlord@example.com",
                    photos="",
                    status="pending",
                    flag_pending=1,
                    flag_verified=0,
                    flag_active=0,
                    flag_rejected=0,
                    created_at="2099-01-02T10:00:00+00:00",
                ),
            ]
        )
        session.commit()


if __name__ == "__main__":
    seed(reset=True)
    print("Seeded student-accommodation demo data")
