from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, DateTime, TIMESTAMP, func, Boolean, BigInteger
from sqlalchemy import ForeignKey, text

from .base import Base

class UserBase(Base):
    __tablename__ = 'Users'

    user_id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    username: Mapped[str] = mapped_column(String())
    registration_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("NOW()")
    )
    first_name: Mapped[str] = mapped_column(String(), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(), nullable=True)
    last_name: Mapped[str] = mapped_column(String(), nullable=True)
    course: Mapped[int] = mapped_column(Integer(), nullable=True)
    room: Mapped[int] = mapped_column(Integer(), nullable=True)
    lang: Mapped[str] = mapped_column(String())
    admin: Mapped[bool] = mapped_column(Boolean(), server_default=text("FALSE"))

    def __repr__(self) -> str:
        return (f"User(user_id={self.user_id!r}, "
                f"username={self.username!r}, "
                f"registration_time={self.registration_time!r}"
                f"first_name={self.first_name!r}, "
                f"middle_name={self.middle_name!r}, "
                f"last_name={self.last_name!r}, "
                f"course={self.course!r}, "
                f"room={self.room!r}, "
                f"lang={self.lang!r}, "
                f"admin={self.admin!r})")


class ResourceBase(Base):
    __tablename__ = 'Resources'

    resource_id: Mapped[int] = mapped_column(primary_key=True)
    resource_name: Mapped[str] = mapped_column(String())

    def __repr__(self):
        return (f"User(resource_id={self.resource_id!r}, "
                f"name={self.resource_name!r}")


class BookingBase(Base):
    __tablename__ = 'Bookings'

    booking_id: Mapped[int] = mapped_column(primary_key=True)
    booking_user_id: Mapped[int] = mapped_column(ForeignKey("Users.user_id"))
    booking_resource_id: Mapped[int] = mapped_column(ForeignKey("Resources.resource_id"))
    booking_time: Mapped[datetime] = mapped_column(DateTime())

    def __repr__(self):
        return (f"User(booking_id={self.booking_id!r}, "
                f"user_id={self.booking_user_id!r}, "
                f"resource_id={self.booking_resource_id!r}, "
                f"booking_time={self.booking_time!r}")
