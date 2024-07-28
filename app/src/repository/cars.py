from operator import not_

from sqlalchemy.orm import Session

from app.src.database.models import Car, User
from app.src.repository.parking import get_all_entries_by_car_id


async def get_car_by_license(car_license: str, db: Session) -> Car | None:
    return db.query(Car).filter(Car.car_license == car_license).first()


async def create_car(car_license: str, user_id: int, db: Session) -> Car:
    car = Car(car_license=car_license, user_id=user_id)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


async def get_user_cars(user_id, db: Session) -> list:
    cars = db.query(Car).filter(Car.user_id == user_id).all()
    return cars


async def get_car_user_by_license(car_license: str, db: Session) -> tuple:
    car = db.query(Car).filter(Car.car_license == car_license).first()
    user = db.query(User).filter(User.id == car.user_id).first()
    return car, user


async def ban_car(car: Car, banned: bool, db: Session) -> str:
    car.banned = banned
    db.commit()
    return f'Car {car.car_license} has been {"un"*not_(banned)}banned'


async def delete_car(car: Car, db: Session) -> str:
    entries = await get_all_entries_by_car_id(car.id, db)
    for e in entries:
        db.delete(e)
    db.commit()
    db.delete(car)
    db.commit()
    return f'Car {car.car_license} has been deleted'
