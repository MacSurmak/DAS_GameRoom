import datetime

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database.models import Resource, ScheduleSlot


async def populate_initial_data(session: AsyncSession):
    """
    Populates the Resource and ScheduleSlot tables with default data
    if the tables are empty.
    """
    try:
        # Check if Resources table is empty
        result = await session.execute(select(func.count(Resource.resource_id)))
        resource_count = result.scalar()

        if resource_count == 0:
            logger.info("Populating initial data for Resources...")
            # Add default resources
            gaming_room = Resource(resource_name="Игровая комната", description="Комната для игр")
            gym = Resource(resource_name="Спортзал", description="Спортивный зал")
            session.add_all([gaming_room, gym])
            await session.flush()  # Important: Get the IDs assigned to the new resources

            logger.info("Populating initial data for ScheduleSlots...")
            # Add default schedule slots for Gaming Room (example)
            #  Make the schedule more realistic: different times on different days.
            gaming_slots = [
                ScheduleSlot(resource_id=gaming_room.resource_id, day_of_week=day, start_time=start, end_time=end)
                for day in range(7)  # Monday to Sunday (0-6)
                for start, end in [
                    (datetime.time(16, 0), datetime.time(23, 0)) if day < 5 else  # Weekdays: 16:00 - 23:00
                    (datetime.time(10, 0), datetime.time(23, 0)) if day == 5 else  # Saturday: 10:00 - 23:00
                    (datetime.time(10, 0), datetime.time(22, 0))  # Sunday: 10:00 - 22:00
                ]
            ]
            # Add default schedule for Gym (example, different times)
            gym_slots = [
              ScheduleSlot(resource_id=gym.resource_id, day_of_week=day, start_time=start, end_time=end)
              for day in range(7)  # Monday to Sunday (0-6)
              for start, end in [
                (datetime.time(7, 0), datetime.time(9, 0)),  # Morning slot
                (datetime.time(12, 0), datetime.time(14, 0)), # Afternoon slot
                (datetime.time(18, 0), datetime.time(22, 0)), # Evening slot
              ]
            ]
            session.add_all(gaming_slots)
            session.add_all(gym_slots)

            await session.commit()
            logger.info("Initial data populated successfully.")
        else:
            logger.info("Resources and ScheduleSlots tables are not empty. Skipping initial data population.")

    except Exception as e:
        await session.rollback()
        logger.exception(f"Error populating initial data: {e}")
        raise # re-raise exception to be handled upper
