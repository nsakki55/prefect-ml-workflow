import pendulum
import prefect
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock

from .environment import Environment


def set_schedule(cron: str = "0 01-23/1 * * *") -> Schedule:
    if Environment.from_str(prefect.config.system_env) is Environment.PRODUCTION:
        return Schedule(clocks=[CronClock(cron, start_date=pendulum.now("Asia/Tokyo"))])

    if Environment.from_str(prefect.config.system_env) is Environment.DEVELOP:
        return None
