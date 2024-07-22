from sqlalchemy.orm import Session

from app.src.database.models import Parking


async def add_entry(user_id: int, car_id: int, db: Session):
    entry = Parking(user_id=user_id, car_id=car_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
