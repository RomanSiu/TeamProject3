from operator import not_

from sqlalchemy.orm import Session

from app.src.database.models import Car, User
from app.src.repository.parking import get_all_entries_by_car_id


async def get_car_by_license(car_license: str, db: Session) -> Car | None:
    """
    Retrieves a car with the specified car license.

    Args:
        car_license (str): license of the car to retrieve.
        db (Session): The database session.

    Returns:
        Car or None: The car with the specified license, or None if it does not exist.
    """
    return db.query(Car).filter(Car.car_license == car_license).first()


async def create_car(car_license: str, user_id: int, db: Session) -> Car:
    """
    Create a new car

    Args:
        car_license (str): The license of the car to create.
        user_id (int): Owner of the car.
        db (Session): The database session.

    Returns:
        [Car]: The newly created car
    """
    car = Car(car_license=car_license, user_id=user_id)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


async def get_user_cars(user_id: int, db: Session) -> list:
    """
    Retrieves a list of user cars

    Args:
        user_id (int): The id of user to retrieve a list of cars.
        db (Session): The database session.

    Returns:
        [list]: The list of user cars
    """
    cars = db.query(Car).filter(Car.user_id == user_id).all()
    return cars


async def get_car_user_by_license(car_license: str, db: Session) -> tuple:
    """
    Retrieves a car with the specific license and its owner.

    Args:
        car_license (str): The license of the car to retrieve.
        db (Session): The database session.

    Returns:
        [tuple]: The car and user
    """
    car = db.query(Car).filter(Car.car_license == car_license).first()
    user = db.query(User).filter(User.id == car.user_id).first()
    return car, user


async def ban_car(car: Car, banned: bool, db: Session) -> str:
    """
    Set car ban flag in the database

    Args:
        car (Car): The car to ban.
        banned (bool): True = banned, False = unbanned
        db (Session): The database session.

    Returns:
        [str]: Message with the car license of banned car.
    """
    car.banned = banned
    db.commit()
    return f'Car {car.car_license} has been {"un"*not_(banned)}banned'


async def delete_car(car: Car, db: Session) -> str:
    """
    Delete car from the database

    Args:
        car (Car): The car to delete.
        db (Session): The database session.

    Returns:
        [str]: Message with the car license of deleted car
    """
    entries = await get_all_entries_by_car_id(car.id, db)
    for e in entries:
        db.delete(e)
    db.commit()
    db.delete(car)
    db.commit()
    return f'Car {car.car_license} has been deleted'
