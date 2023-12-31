import sched
import time
from datetime import datetime, timedelta
from typing import Dict, Any

scheduler: Any = sched.scheduler(time.time, time.sleep)

TIME_TO_REMIND_IN_MINUTES: int = 30


def send_reminder(event: Dict[str, Any]) -> None:
    print(f"Reminder: Event '{event['name']}' is starting in TIME_TO_REMIND_IN_MINUTES minutes at {event['date']}!")


def schedule_reminder(event: Dict[str, Any]) -> None:
    # Get the event's scheduled time
    event_time: datetime = datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%S')

    # Calculate the time for the reminder (TIME_TO_REMIND_IN_MINUTES minutes before the event)
    reminder_time: datetime = event_time - timedelta(minutes=TIME_TO_REMIND_IN_MINUTES)

    # Calculate the delay until the reminder
    delay: float = (reminder_time - datetime.now()).total_seconds()

    # Schedule the reminder
    scheduler.enter(delay, 1, send_reminder, argument=(event,))
