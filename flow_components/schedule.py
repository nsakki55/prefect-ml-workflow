import pendulum
import prefect
from prefect.schedules import Schedule
from prefect.schedules.clocks import CronClock


def cron_clock_schedule(cron: str) -> Schedule:
    """Cronで実行スケジュールを作成"""
    return Schedule(clocks=[CronClock(cron, start_date=pendulum.now("Asia/Tokyo"))])


def set_schedule(cron: str = "0 01-23/1 * * *") -> Schedule:
    if prefect.config.system_env == "production":
        return cron_clock_schedule(cron)
    else:
        return None
