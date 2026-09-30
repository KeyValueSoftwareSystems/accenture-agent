from netra.decorators import task

from backend.db import get_db, next_id, save_db


@task
def create_group_block(
    block_code: str,
    room_type_id: str,
    check_in: str,
    check_out: str,
    units: int,
    rate: float,
    private: bool = True,
) -> dict:
    """Create a group block of rooms."""
    db = get_db()
    block = {
        "id": next_id("bk"),
        "block_code": block_code,
        "name": "",
        "room_type_id": room_type_id,
        "check_in": check_in,
        "check_out": check_out,
        "units": units,
        "rate": rate,
        "private": private,
    }
    db["blocks"].append(block)
    save_db(db)
    return block


@task
def book_room_under_block(reservation_id: str, block_code: str) -> dict | None:
    """Attach a reservation to a group block by block code."""
    db = get_db()
    reservation = next((r for r in db["reservations"] if r["id"] == reservation_id), None)
    if reservation is None:
        return None
    reservation["block_code"] = block_code
    save_db(db)
    return reservation