from backend.db import get_db, next_id, save_db


def generate_invoice(reservation_id: str) -> dict | None:
    """Generate an invoice for a reservation."""
    db = get_db()
    reservation = next((r for r in db["reservations"] if r["id"] == reservation_id), None)
    if reservation is None:
        return None
    invoice = {
        "id": next_id("inv"),
        "reservation_id": reservation_id,
        "line_items": [{"description": "Total", "amount": reservation.get("total", 0)}],
        "total": reservation.get("total", 0),
    }
    db["invoices"].append(invoice)
    save_db(db)
    return invoice


def get_invoice(reservation_id: str) -> list:
    """Return invoices for a reservation."""
    return [i for i in get_db()["invoices"] if i["reservation_id"] == reservation_id]


def resend_confirmation(reservation_id: str, email: str | None = None) -> dict | None:
    """Resend a confirmation email for a reservation."""
    db = get_db()
    reservation = next((r for r in db["reservations"] if r["id"] == reservation_id), None)
    if reservation is None:
        return None
    guest = next((g for g in db["guests"] if g["id"] == reservation["guest_id"]), {})
    record = {
        "id": next_id("email"),
        "reservation_id": reservation_id,
        "address": email or guest.get("email"),
        "sent_at": "2026-09-28",
    }
    db["confirmation_emails"].append(record)
    save_db(db)
    return record