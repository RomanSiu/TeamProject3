from sqlalchemy import String, DateTime, ForeignKey, Boolean, Float, Interval
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from sqlalchemy.schema import Sequence
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
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    move_in_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    move_out_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    parking_time: Mapped[int] = mapped_column(nullable=True)
    parking_cost: Mapped[float] = mapped_column(Float, default=0.0)


class User(BaseTable):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(13), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    rate_id: Mapped[int] = mapped_column(ForeignKey("rates.id"), default=1)


class Rate(BaseTable):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(Sequence('rates_id_seq', start=2, increment=1), primary_key=True)
    rate_name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
