from netra.decorators import task

from backend.db import get_db, next_id, save_db


@task
def send_payment_link(reservation_id: str, phone: str, landline_check: bool = False) -> dict:
    """Send a payment link to a phone number.

    Args:
        reservation_id: The reservation to collect payment for.
        phone: Phone number to send the link to.
        landline_check: Whether the number was verified not to be a landline.
    """
    db = get_db()
    link = {
        "id": next_id("plink"),
        "reservation_id": reservation_id,
        "phone": phone,
        "status": "pending",
    }
    db["payment_links"].append(link)
    save_db(db)
    return link


@task
def request_payment(reservation_id: str) -> dict | None:
    """Return the amount due for a reservation."""
    reservation = next((r for r in get_db()["reservations"] if r["id"] == reservation_id), None)
    if reservation is None:
        return None
    total = reservation.get("total", 0)
    paid = reservation.get("paid", 0)
    return {
        "reservation_id": reservation_id,
        "total": total,
        "paid": paid,
        "balance_due": total - paid,
    }