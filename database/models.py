from decimal import Decimal

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Date, DECIMAL, BOOLEAN, TEXT, ForeignKey, \
    Identity, Time, Enum, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from .base import Base  # Import Base from the separate base.py file

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, Identity(), primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    middle_name = Column(String(255))
    room_number = Column(String(255))
    year = Column(Integer)
    grade = Column(Enum('bachelor', 'master', 'specialist', name='grade_type'), nullable=True)  # Use Enum, and it can be nullable
    lang = Column(String(255))
    is_admin = Column(BOOLEAN, default=False)

    def __repr__(self):
        return (f"<User(user_id={self.user_id}, telegram_id={self.telegram_id}, "
                f"first_name={self.first_name}, is_admin={self.is_admin})>")


class Resource(Base):
    __tablename__ = 'resources'

    resource_id = Column(Integer, Identity(), primary_key=True)
    resource_name = Column(String(255), nullable=False)
    description = Column(TEXT) # Optional description

    def __repr__(self):
        return f"<Resource(resource_id={self.resource_id}, resource_name={self.resource_name})>"

class ScheduleSlot(Base):
    """Represents a *recurring* time slot in the schedule."""
    __tablename__ = 'schedule_slots'

    slot_id = Column(Integer, Identity(), primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.resource_id'), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0 = Monday, 1 = Tuesday, ..., 6 = Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_active = Column(BOOLEAN, default=True) # Added, to deactivate slots without deleting

    resource = relationship("Resource", backref="schedule_slots")

    def __repr__(self):
      return (f"<ScheduleSlot(slot_id={self.slot_id}, resource_id={self.resource_id}, "
                f"day_of_week={self.day_of_week}, start_time={self.start_time}, "
                f"end_time={self.end_time})>")


class ScheduleOverride(Base):
    """Represents a one-time *exception* to the regular schedule."""
    __tablename__ = 'schedule_overrides'

    override_id = Column(Integer, Identity(), primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.resource_id'), nullable=False)
    date = Column(Date, nullable=False)  # The specific date of the override
    start_time = Column(Time, nullable=True)  # Start time of the override (can be different from slot)
    end_time = Column(Time, nullable=True)    # End time of the override (can be different from slot)
    is_available = Column(BOOLEAN, nullable=False)  # True = Available, False = Unavailable (blocked)
    reason = Column(TEXT) # Optional reason for the override

    resource = relationship("Resource", backref="schedule_overrides")
    __table_args__ = (
        UniqueConstraint('resource_id', 'date', 'start_time', name='unique_override'),
    )

    def __repr__(self):
      return (f"<ScheduleOverride(override_id={self.override_id}, resource_id={self.resource_id}, "
              f"date={self.date}, start_time={self.start_time}, end_time={self.end_time}, "
              f"is_available={self.is_available})>")

class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, Identity(), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.resource_id'), nullable=False)
    slot_id = Column(Integer, ForeignKey('schedule_slots.slot_id'), nullable=True)  # Link to ScheduleSlot (optional, but helpful for reporting)
    override_id = Column(Integer, ForeignKey('schedule_overrides.override_id'), nullable=True) # Link to override, if applicable
    booking_date = Column(Date, nullable=False)  # Date of the booking
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    request_time = Column(DateTime(timezone=True), server_default=func.now()) # Timestamp when booking made.
    status = Column(Enum('pending', 'confirmed', 'rejected', 'cancelled', name='booking_status'), default='pending')

    user = relationship("User", backref="bookings")
    resource = relationship("Resource", backref="bookings")
    slot = relationship("ScheduleSlot", backref="bookings")
    override = relationship("ScheduleOverride", backref="bookings")

    def __repr__(self):
      return (f"<Booking(booking_id={self.booking_id}, user_id={self.user_id}, "
              f"resource_id={self.resource_id}, booking_date={self.booking_date}, "
              f"start_time={self.start_time}, end_time={self.end_time}, status={self.status})>")
