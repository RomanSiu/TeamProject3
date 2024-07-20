from sqlalchemy import String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from datetime import datetime

Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_license: Mapped[str] = mapped_column(String(10), unique=True)
    banned: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Parking(Base):
    __tablename__ = "parking"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(String(10))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    move_in_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    move_out_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class User(BaseTable):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    car_id: Mapped[list[Car]] = relationship()
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    park_history: Mapped[list[Parking]] = relationship()
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
