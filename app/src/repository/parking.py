from datetime import datetime
from math import ceil

from sqlalchemy.orm import Session

from app.src.database.models import Parking, Rate
from app.src.repository.users import get_user_by_id


async def add_entry(user_id: int, car_id: int, db: Session):
    entry = Parking(user_id=user_id, car_id=car_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


async def get_entry_by_car_id(car_id: int, db: Session):
    return db.query(Parking).filter(Parking.car_id == car_id).order_by(Parking.move_in_at.desc()).first()


async def get_all_entries_by_car_id(car_id: int, db: Session):
    return db.query(Parking).filter(Parking.car_id == car_id).all()


async def close_entry_rep(entry: Parking, db: Session):
    entry.move_out_at = datetime.now()
    entry.parking_time = int((entry.move_out_at - entry.move_in_at).total_seconds())
    db.commit()
    return entry


async def parking_fee(entry: Parking, free: bool, db: Session):
    user = await get_user_by_id(entry.user_id, db)
    rate = db.query(Rate).filter(Rate.id == user.rate_id).first()
    price = rate.price * ceil(int(entry.parking_time) / 3600)
    if not free:
        entry.parking_cost = price
        user.balance -= price
        db.commit()
    return
