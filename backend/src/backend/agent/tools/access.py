from backend.db import get_db


def get_door_lock_info(reservation_id: str) -> list:
    """Return door lock records for a reservation."""
    return [d for d in get_db()["door_locks"] if d["reservation_id"] == reservation_id]