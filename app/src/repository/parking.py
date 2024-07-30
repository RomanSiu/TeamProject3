from datetime import datetime
from math import ceil

from sqlalchemy.orm import Session

from app.src.database.models import Parking, Rate
from app.src.repository.users import get_user_by_id


async def add_entry(user_id: int, car_id: int, db: Session) -> Parking:
    """
    Create a new entry record

    Args:
        user_id (int): Car owner id
        car_id (int): Car id
        db (Session): The database session.

    Returns:
        [Parking]: The newly created entry
    """
    entry = Parking(user_id=user_id, car_id=car_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


async def get_entry_by_car_id(car_id: int, db: Session) -> Parking | None:
    """
    Retrieves last entry with the car id.

    Args:
        car_id (int): id of the car to retrieve the entry.
        db (Session): The database session.

    Returns:
        Parking or None: The entry record, or None if it does not exist.
    """
    return db.query(Parking).filter(Parking.car_id == car_id).order_by(Parking.move_in_at.desc()).first()


async def get_all_entries_by_car_id(car_id: int, db: Session) -> list[Parking]:
    """
    Retrieves all entries by the car id.

    Args:
        car_id (int): id of the car to retrieve all entries.
        db (Session): The database session.

    Returns:
        List[Parking]: List of entry records.
    """
    return db.query(Parking).filter(Parking.car_id == car_id).all()


async def close_entry_rep(entry: Parking, db: Session) -> Parking:
    """
    Close the entry, save exit time and parking time calculation.

    Args:
        entry (Parking): The entry to close.
        db (Session): The database session.

    Returns:
        Parking: The closed entry.
    """
    entry.move_out_at = datetime.now()
    entry.parking_time = int((entry.move_out_at - entry.move_in_at).total_seconds())
    db.commit()
    return entry


async def parking_fee(entry: Parking, free: bool, db: Session) -> None:
    """
    Calculate the parking fee and wright off money from the user.

    Args:
        entry (Parking): The entry to calculate the parking fee.
        free (bool, optional): Whether the entry is free or not.
        db (Session): The database session/

    Returns:
        None
    """
    user = await get_user_by_id(entry.user_id, db)
    rate = db.query(Rate).filter(Rate.id == user.rate_id).first()
    price = rate.price * ceil(int(entry.parking_time) / 3600)
    if not free:
        entry.parking_cost = price
        user.balance -= price
        db.commit()
    return


async def get_bills(car_id: int, db: Session) -> list[Parking]:
    """
    Get the bills by car id.

    Args:
        car_id (int): The car id to get the bills.
        db (Session): The database session.

    Returns:
        List[Parking]: List of closed entry records.
    """
    return db.query(Parking).filter(Parking.car_id == car_id).all()
