import prefect
from prefect.storage import Docker, Storage

from .environment import Environment


def docker_storage(image_tag: str) -> Storage:
    """Flowをdocker imageとして管理するための設定"""
    return Docker(
        image_name=prefect.config.image_name,
        image_tag=image_tag,
        registry_url=prefect.config.ecr_repository,
        dockerfile=prefect.config.dockerfile,
        env_vars={"SYSTEM_ENV": prefect.config.system_env},
    )


def set_storage(image_tag: str = "latest") -> Storage:
    if Environment.from_str(prefect.config.system_env) in [Environment.PRODUCTION, Environment.DEVELOP]:
        return docker_storage(image_tag=image_tag)
