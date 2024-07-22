from http.client import HTTPException

from fastapi import (APIRouter, Depends, HTTPException, status)
from sqlalchemy.orm import Session

from app.src.database.db import get_db
from app.src.repository.cars import get_car_by_license
from app.src.repository.users import get_user_by_id
from app.src.repository.parking import add_entry

router = APIRouter(prefix="/parking", tags=["parking"])


@router.post("/entry")
async def create_entry(car_license: str,
                       db: Session = Depends(get_db)):
    # camera make photo
    # call def with model, to take car license
    car = await get_car_by_license(car_license, db)

    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No car in DB")
    elif car.banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Car is blocked")

    user = await get_user_by_id(car.user_id, db)

    if user.balance <= 0:
        # send message to user phone, about negative balance
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Negative balance")

    entry = await add_entry(user.id, car.id, db)
    return entry
