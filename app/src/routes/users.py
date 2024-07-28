from fastapi import (APIRouter, Depends, UploadFile, File, HTTPException, status, BackgroundTasks, Request, Query)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import EmailStr
import pandas as pd

from app.src.database.db import get_db
from app.src.database.models import User
from app.src.repository import users as repository_users
from app.src.repository import cars as repository_cars
from app.src.repository import rates as repository_rates
from app.src.repository import parking as repository_parking
from app.src.services.auth import RoleChecker, auth_service
from app.src.schemas import UserDb, UserPassword, UserNewPassword, RoleOptions, CarResponse
from app.src.services.email import send_password_email, send_email
from app.src.routes.auth import r

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def read_users_me(current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)) -> dict:
    user_info = {"username": current_user.username,
                 "email": current_user.email,
                 "role": current_user.role,
                 "created_at": current_user.created_at}
    return user_info


@router.get("/{username}")
async def read_users(username: str, db: Session = Depends(get_db)) -> dict:
    user = await repository_users.get_user_by_username(username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username")
    user_info = {"username": user.username,
                 "email": user.email}
    return user_info


@router.patch("/me", response_model=UserDb)
async def update_user(background_tasks: BackgroundTasks,
                      request: Request,
                      token: str = Depends(auth_service.oauth2_scheme),
                      username: str | None = None,
                      email: EmailStr | None = None,
                      current_user: User = Depends(auth_service.get_current_user),
                      db: Session = Depends(get_db)):
    if username and username != current_user.username:
        user_check_username = await repository_users.get_user_by_username(username, db)
        if user_check_username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        user = await repository_users.change_user_username(current_user, username, db)

    if email and email != current_user.email:
        user_check_email = await repository_users.get_user_by_email(email, db)
        if user_check_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        user = await repository_users.change_user_email(current_user, email, db)
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
        r.set(token, 1)
        r.expire(token, 900)
    r.delete(f"user:{current_user.email}")
    return user


@router.patch("/me/change_password")
async def change_password(body: UserPassword,
                          current_user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)) -> dict:
    if not auth_service.verify_password(body.old_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    message = await auth_service.update_password(current_user, body.new_password, db)
    r.delete(f"user:{current_user.email}")
    return {"message": message}


@router.post("/me/forgot_password")
async def forgot_password(body: UserNewPassword,
                          background_tasks: BackgroundTasks,
                          request: Request,
                          db: Session = Depends(get_db)) -> dict:
    message = {"message": "Email to reset your password was sent"}
    try:
        user = await repository_users.get_user_by_email(body.email, db)
    except HTTPException:
        return message
    if not user:
        return message
    background_tasks.add_task(send_password_email, user.email, body.new_password, user.username, request.base_url)
    r.delete(f"user:{user.email}")
    return message


@router.get('/reset_password/{token}')
async def reset_password(token: str, db: Session = Depends(get_db)) -> dict:
    email = await auth_service.get_email_from_token(token)
    password = await auth_service.get_password_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    await auth_service.update_password(user, password, db)
    return {"message": "Password reset"}


@router.patch("/{user_id}", response_model=UserDb)
async def change_user_role(user_id: int,
                           new_role: RoleOptions = Query(default=RoleOptions.user),
                           current_user: User = Depends(RoleChecker(allowed_roles=["admin"])),
                           db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot change your own role")
    changed_user = await repository_users.change_user_role(user, new_role, db)
    r.delete(f"user:{user.email}")
    return changed_user


@router.patch('/{user_id}/ban')
async def ban_unban_user(user_id: int,
                         banned: bool,
                         current_user: User = Depends(RoleChecker(['admin'])),
                         db: Session = Depends(get_db)
                         ) -> dict:
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot ban/unban yourself")

    user = await repository_users.get_user_by_id(user_id, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    r.delete(f"user:{user.email}")
    message = await repository_users.ban_user(user, banned, db)
    return {"message": message}


@router.patch('/me/add_car', response_model=CarResponse)
async def add_car(car_license: str,
                  current_user: User = Depends(auth_service.get_current_user),
                  db: Session = Depends(get_db)) -> dict:
    exist_car = await repository_cars.get_car_by_license(car_license, db)
    if exist_car:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Car already exists")

    new_car = await repository_cars.create_car(car_license, current_user.id, db)
    return {"car": new_car, "detail": "Car successfully added"}


@router.get('/me/cars')
async def get_cars(current_user: User = Depends(auth_service.get_current_user),
                   db: Session = Depends(get_db)):
    cars = await repository_cars.get_user_cars(current_user.id, db)

    if not cars:
        raise HTTPException(status_code=404, detail=f"No cars found")
    cars = [i.car_license for i in cars]
    return cars


@router.patch('/{user_id}/rate')
async def change_rate(user_id: int, rate_id: int,
                      current_user: User = Depends(RoleChecker(['admin'])),
                      db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    rate = await repository_rates.get_rate_by_id(rate_id, db)

    if not rate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rate not found")

    user = await repository_users.change_user_rate(user, rate_id, db)
    return user


@router.delete('/me/car/delete')
async def delete_car(car_license: str,
                     current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    car = await repository_cars.get_car_by_license(car_license, db)

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    elif car.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")

    message = await repository_cars.delete_car(car, db)
    return message


@router.get('/me/parking_bills')
async def get_parking_bills(car_license: str,
                            csv_file: bool = False,
                            current_user: User = Depends(auth_service.get_current_user),
                            db: Session = Depends(get_db)):
    car = await repository_cars.get_car_by_license(car_license, db)

    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    elif car.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")

    bills = await repository_parking.get_bills(car.id, db)

    if not bills:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no bills for this car")
    new_bills = []
    for bill in bills:
        obill = {"car license": car.car_license,
                 "move in": bill.move_in_at.strftime("%H:%M:%S, %m-%d-%Y"),
                 "move out": bill.move_out_at.strftime("%H:%M:%S, %m-%d-%Y"),
                 "total amount": f"{bill.parking_cost} ₴"}
        new_bills.append(obill)

    if csv_file:
        df = pd.DataFrame(new_bills)
        return StreamingResponse(
            iter([df.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=bills.csv"}
        )
    return new_bills

