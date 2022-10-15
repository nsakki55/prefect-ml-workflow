import prefect
from prefect import Flow
from prefect.engine.state import Failed, State
from prefect.utilities.notifications import slack_notifier
from pytz import timezone


def run_name_handler(flow: Flow, old_state: State, new_state: State) -> None:
    """実行Flowの命名規則のハンドラ"""
    if new_state.is_running():
        client = prefect.Client()
        name = (
            f"{flow.name}-"
            f"{prefect.context.scheduled_start_time.astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d-%H-%M-%S')}"
        )
        client.set_flow_run_name(prefect.context.flow_run_id, name)


def notification_handler(state: State = Failed) -> State:
    """Slack通知用のハンドラ"""
    if prefect.config.system_env == "production":
        return [slack_notifier(only_states=[Failed])]
    else:
        return None
