from sqlalchemy.orm import Session

from app.src.database.models import Rate


async def find_rate(rate_name: str, db: Session) -> Rate:
    """
    Find a rate by name

    Args:
        rate_name (str): The name of the rate to be found.
        db (Session): The database session.

    Returns:
        [Rate]: The rate with the given name
    """
    return db.query(Rate).filter(Rate.rate_name == rate_name).first()


async def add_rate(rate_name: str, price: float, db: Session) -> Rate:
    """
    Create a new rate

    Args:
        rate_name (str): The name of the rate to be created.
        price (float): The price of the rate (unit/hour).
        db (Session): The database session.

    Returns:
        [Rate]: The newly created rate
    """
    rate = Rate(rate_name=rate_name, price=price)
    db.add(rate)
    db.commit()
    db.refresh(rate)
    return rate


async def change_rate(rate: Rate, price: float, db: Session) -> Rate:
    """
    Update a rate

    Args:
        rate (Rate): The rate to be changed.
        price (float): The new price of the rate (unit/hour).
        db (Session): The database session.

    Returns:
        [Rate]: The updated rate
    """
    rate.price = price
    db.commit()
    return rate


async def delete_rate(rate: Rate, db: Session) -> str:
    """
    Delete a rate

    Args:
        rate (Rate): The rate to be deleted.
        db (Session): The database session.

    Returns:
        str: message
    """
    db.delete(rate)
    db.commit()
    return "Rate was deleted"


async def get_rate_by_id(rate_id: int, db: Session):
    """
    Find a rate by id

    Args:
        rate_id (int): The id of the rate to be found/
        db (Session): The database session.

    Returns:
        [Rate]: The rate with the given id
    """
    return db.query(Rate).filter(Rate.id == rate_id).first()
