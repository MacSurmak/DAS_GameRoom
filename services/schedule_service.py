import datetime
from typing import List, Tuple, Optional

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Resource, ScheduleSlot, ScheduleOverride, Booking

async def get_available_slots(session: AsyncSession, resource_id: int, date: datetime.date) -> List[datetime.time]:
    """
    Gets available *start* times for a resource on a given date.
    """
    available_start_times = []

    # 1. Get regular schedule slots.
    day_of_week = date.weekday()
    regular_slots_query = select(ScheduleSlot).where(
        ScheduleSlot.resource_id == resource_id,
        ScheduleSlot.day_of_week == day_of_week,
        ScheduleSlot.is_active == True
    )
    regular_slots = await session.execute(regular_slots_query)
    regular_slots = regular_slots.scalars().all()

    # 2. Get overrides.
    overrides_query = select(ScheduleOverride).where(
        ScheduleOverride.resource_id == resource_id,
        ScheduleOverride.date == date
    )
    overrides = await session.execute(overrides_query)
    overrides = overrides.scalars().all()

    # 3. Get confirmed bookings.
    bookings_query = select(Booking).where(
        Booking.resource_id == resource_id,
        Booking.booking_date == date,
        Booking.status == 'confirmed'
    )
    bookings = await session.execute(bookings_query)
    bookings = bookings.scalars().all()

    # 4. Process regular slots.
    for regular_slot in regular_slots:
        current_time = regular_slot.start_time
        while current_time < regular_slot.end_time:
            potential_start_time = current_time
            is_available = True

            # 4a. Check against overrides (blocking).
            for override in overrides:
                if not override.is_available:  # Blocking override
                    if (override.start_time is None or potential_start_time >= override.start_time) and \
                       (override.end_time is None or datetime.datetime.combine(date, potential_start_time) < datetime.datetime.combine(date, override.end_time)):
                        is_available = False
                        break

            # 4b. Check against bookings.
            if is_available:
                for booking in bookings:
                    potential_end_time = (datetime.datetime.combine(datetime.date.min, potential_start_time) + datetime.timedelta(hours=3)).time()
                    if (potential_start_time < booking.end_time and potential_end_time > booking.start_time):
                        is_available = False
                        break

            # 4c. Add if available.
            if is_available:
                available_start_times.append(potential_start_time)

            current_time = (datetime.datetime.combine(datetime.date.min, current_time) + datetime.timedelta(minutes=30)).time()

    # 5. Add slots from overrides (adding availability).
    for override in overrides:
        if override.is_available and override.start_time and override.end_time:
            current_time = override.start_time
            while current_time < override.end_time:
                potential_start_time = current_time
                is_available = True

                # Check against *regular* schedule (overrides can't add slots outside the base schedule).
                found_in_regular = False
                for regular_slot in regular_slots:
                    if regular_slot.start_time <= potential_start_time < regular_slot.end_time:
                        found_in_regular = True
                        break
                if not found_in_regular:
                    current_time = (datetime.datetime.combine(datetime.date.min, current_time) + datetime.timedelta(minutes=30)).time()
                    continue # Skip times that are not inside base schedule


                # Check against *other* overrides (don't double-count).
                for other_override in overrides:
                    if other_override != override and not other_override.is_available:
                         if (other_override.start_time is None or potential_start_time >= other_override.start_time) and \
                            (other_override.end_time is None or datetime.datetime.combine(date, potential_start_time) < datetime.datetime.combine(date, other_override.end_time)):
                            is_available = False
                            break

                # Check against bookings.
                for booking in bookings:
                    potential_end_time = (datetime.datetime.combine(datetime.date.min, potential_start_time) + datetime.timedelta(hours=3)).time()
                    if (potential_start_time < booking.end_time and potential_end_time > booking.start_time):
                        is_available = False
                        break

                if is_available:
                    available_start_times.append(potential_start_time)

                current_time = (datetime.datetime.combine(datetime.date.min, current_time) + datetime.timedelta(minutes=30)).time()

    available_start_times = list(set(available_start_times)) # remove duplicates
    available_start_times.sort()
    return available_start_times


async def is_slot_available(session: AsyncSession, resource_id: int, date: datetime.date,
                            start_time: datetime.time, end_time: datetime.time) -> bool:
    """
    Checks if a *specific* time slot is available.
    """
    # 1. Get regular schedule.
    day_of_week = date.weekday()
    regular_slots_query = select(ScheduleSlot).where(
        ScheduleSlot.resource_id == resource_id,
        ScheduleSlot.day_of_week == day_of_week,
        ScheduleSlot.is_active == True
    )
    regular_slots = await session.execute(regular_slots_query)
    regular_slots = regular_slots.scalars().all()

    # Check if within regular schedule.
    slot_within_regular_schedule = False
    for regular_slot in regular_slots:
        if regular_slot.start_time <= start_time and end_time <= regular_slot.end_time:
            slot_within_regular_schedule = True
            break

    # 2. Get overrides.
    overrides_query = select(ScheduleOverride).where(
        ScheduleOverride.resource_id == resource_id,
        ScheduleOverride.date == date
    )
    overrides = await session.execute(overrides_query)
    overrides = overrides.scalars().all()

    # 3. Check against overrides.
    for override in overrides:
        if override.is_available is False:
            # Blocking override.
            if (override.start_time is None or start_time >= override.start_time) and \
               (override.end_time is None or end_time <= override.end_time):
                return False  # Blocked
        elif override.is_available and override.start_time and override.end_time:
            if override.start_time <= start_time and end_time <= override.end_time:
                return True

    # If outside regular and no adding overrides, return False.
    if not slot_within_regular_schedule and not overrides:
        return False

     # 4. Check against confirmed bookings.
    bookings_query = select(Booking).where(
        Booking.resource_id == resource_id,
        Booking.booking_date == date,
        Booking.status == 'confirmed'
    )
    bookings = await session.execute(bookings_query)
    bookings = bookings.scalars().all()

    for booking in bookings:
        if (start_time < booking.end_time and end_time > booking.start_time):
            return False  # Conflict

    return True

async def get_resource_name_by_id(session: AsyncSession, resource_id: int) -> str:
    """Helper function to get a resource name by its ID."""
    resource = await session.get(Resource, resource_id)
    if resource:
        return resource.resource_name
    return "Unknown Resource"
