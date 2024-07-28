from sqlalchemy.orm import Session

from app.src.database.models import Rate


async def find_rate(rate_name: str, db: Session):
    return db.query(Rate).filter(Rate.rate_name == rate_name).first()


async def add_rate(rate_name: str, price: float, db: Session):
    rate = Rate(rate_name=rate_name, price=price)
    db.add(rate)
    db.commit()
    db.refresh(rate)
    return rate


async def change_rate(rate: Rate, price: float, db: Session):
    rate.price = price
    db.commit()
    return rate


async def delete_rate(rate:Rate, db: Session):
    db.delete(rate)
    db.commit()
    return "Rate was deleted"


async def get_rate_by_id(rate_id: int, db: Session):
    return db.query(Rate).filter(Rate.id == rate_id).first()
