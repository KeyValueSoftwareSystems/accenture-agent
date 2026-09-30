from backend.db import get_db, save_db


def apply_discount_code(reservation_id: str, code: str) -> dict | None:
    """Stamp a discount code onto a reservation."""
    db = get_db()
    reservation = next((r for r in db["reservations"] if r["id"] == reservation_id), None)
    if reservation is None:
        return None
    reservation["discount"] = {"type": "discount_code", "code": code}
    save_db(db)
    return reservation


def apply_gift_certificate(reservation_id: str, code: str) -> dict | None:
    """Stamp a gift certificate onto a reservation."""
    db = get_db()
    reservation = next((r for r in db["reservations"] if r["id"] == reservation_id), None)
    if reservation is None:
        return None
    reservation["discount"] = {"type": "gift_certificate", "code": code}
    save_db(db)
    return reservation