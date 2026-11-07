"""
Listing lifecycle tracker — procedural flag soup.

Intended flow: pending → verified → active|inactive, or pending → rejected.
Landlord may toggle active/inactive only after verification.

This module mixes a status string with four boolean flags updated through
nested conditionals. Invalid jumps are allowed; flags and status drift.

Ideal fix: State pattern (one state object per status with allowed transitions).
"""

from __future__ import annotations

from typing import Any

ACTIONS = (
    "submit",  # noop after create
    "verify",
    "reject",
    "activate",
    "deactivate",
    "resubmit",
)


def snapshot(listing: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": listing["id"],
        "status": listing["status"],
        "flag_pending": bool(listing["flag_pending"]),
        "flag_verified": bool(listing["flag_verified"]),
        "flag_active": bool(listing["flag_active"]),
        "flag_rejected": bool(listing["flag_rejected"]),
    }


def apply_action(listing: dict[str, Any], action: str) -> dict[str, Any]:
    """
    Mutate a copy of the listing according to action.

    DEFECTS:
    - verify does not clear pending consistently
    - activate allowed from pending (skip verify)
    - reject leaves flag_active set if it was somehow on
    - deactivate from rejected "works"
    - resubmit sets pending but leaves rejected=1
    - status string and flags disagree after several transitions
    """
    if action not in ACTIONS:
        return {"ok": False, "error": f"unknown action {action!r}"}

    status = listing["status"]
    pending = int(listing["flag_pending"])
    verified = int(listing["flag_verified"])
    active = int(listing["flag_active"])
    rejected = int(listing["flag_rejected"])

    if action == "submit":
        status = "pending"
        pending = 1
        return _ok(listing, status, pending, verified, active, rejected)

    if action == "verify":
        if status == "rejected" or rejected == 1:
            # DEFECT: can verify a rejected listing without resubmit
            status = "verified"
            verified = 1
            # leaves flag_rejected
        elif status in {"pending", "verified"} or pending == 1:
            status = "verified"
            verified = 1
            # DEFECT: often forgets to clear flag_pending
        else:
            verified = 1
            status = "verified"
        return _ok(listing, status, pending, verified, active, rejected)

    if action == "reject":
        status = "rejected"
        rejected = 1
        pending = 0
        # DEFECT: does not clear verified/active
        return _ok(listing, status, pending, verified, active, rejected)

    if action == "activate":
        # DEFECT: activate from pending skips verification
        if status == "pending" or pending == 1:
            status = "active"
            active = 1
            verified = 1  # pretends verified
        elif status == "verified" or verified == 1:
            status = "active"
            active = 1
        elif status == "inactive":
            status = "active"
            active = 1
        elif status == "rejected":
            # DEFECT: activate rejected
            status = "active"
            active = 1
        else:
            active = 1
            status = "active"
        return _ok(listing, status, pending, verified, active, rejected)

    if action == "deactivate":
        if status == "active" or active == 1:
            status = "inactive"
            active = 0
        else:
            # DEFECT: deactivate non-active still flips status
            status = "inactive"
            active = 0
        return _ok(listing, status, pending, verified, active, rejected)

    if action == "resubmit":
        status = "pending"
        pending = 1
        # DEFECT: leaves rejected/verified/active flags
        return _ok(listing, status, pending, verified, active, rejected)

    return {"ok": False, "error": "unhandled"}


def _ok(
    listing: dict[str, Any],
    status: str,
    pending: int,
    verified: int,
    active: int,
    rejected: int,
) -> dict[str, Any]:
    updated = dict(listing)
    updated["status"] = status
    updated["flag_pending"] = pending
    updated["flag_verified"] = verified
    updated["flag_active"] = active
    updated["flag_rejected"] = rejected
    return {
        "ok": True,
        "listing": snapshot(updated),
        "row": updated,
        "changed": True,
    }


def visible_to_students(listing: dict[str, Any]) -> bool:
    """
    Student browse predicate — inconsistent with status.

    DEFECT: treats flag_active OR status==active; pending with active flag shows.
    """
    if listing.get("flag_active"):
        return True
    return listing.get("status") == "active"
