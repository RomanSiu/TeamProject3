from operator import not_

from sqlalchemy.orm import Session

from app.src.database.models import User
from app.src.schemas import UserModel, RoleOptions


async def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


async def get_user_by_username(username: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == username).first()


async def create_user(body: UserModel, db: Session) -> User:
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    if user.id == 1:
        user.role = "admin"
    db.commit()


async def change_user_role(user: User, role: RoleOptions, db: Session) -> User:
    user.role = role
    db.commit()
    return user


async def ban_user(user: User, banned: bool, db: Session) -> str:
    user.banned = banned
    db.commit()
    return f'User {user.username} has been {"un"*not_(banned)}banned'


async def change_user_username(user: User, username: str, db: Session) -> User:
    current_user = await get_user_by_email(user.email, db)
    current_user.username = username
    db.commit()
    return current_user


async def change_user_email(user: User, email: str, db: Session) -> User:
    current_user = await get_user_by_email(user.email, db)
    current_user.email = email
    current_user.confirmed = False
    db.commit()
    return current_user
