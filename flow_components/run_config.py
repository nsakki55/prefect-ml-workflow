import prefect
from prefect.run_configs import DockerRun, ECSRun
from prefect.run_configs.base import RunConfig


def ecs_run_config(flow_name: str, cpu: int = 1024, memory: int = 2048) -> RunConfig:
    """Flowを実行するECS Taskの設定"""
    return ECSRun(
        labels=prefect.config.labels,
        task_definition=dict(
            family=flow_name,
            networkMode="awsvpc",
            cpu=cpu,
            memory=memory,
            taskRoleArn=prefect.config.task_role_arn,
            executionRoleArn=prefect.config.task_execution_role_arn,
            containerDefinitions=[
                dict(
                    name="flow",
                    essential=True,
                    environment=[{"name": "SYSTEM_ENV", "value": prefect.config.system_env}],
                    logConfiguration=dict(
                        logDriver="awslogs",
                        options={
                            "awslogs-group": prefect.config.aws_log_group,
                            "awslogs-region": prefect.config.region,
                            "awslogs-stream-prefix": flow_name,
                            "awslogs-create-group": "true",
                        },
                    ),
                )
            ],
        ),
        run_task_kwargs=dict(
            cluster=prefect.config.cluster_arn,
            launchType="FARGATE",
            networkConfiguration={
                "awsvpcConfiguration": dict(subnets=prefect.config.subnets, securityGroups=prefect.config.security_groups),
            },
        ),
    )


def set_run_config(flow_name: str, cpu: int = 1024, memory: int = 2048) -> RunConfig:
    if prefect.config.system_env == "production":
        return ecs_run_config(flow_name=flow_name, cpu=cpu, memory=memory)

    elif prefect.config.system_env == "develop":
        return DockerRun(image=prefect.config.image_name)

    else:
        raise ValueError(f"{prefect.config.system_env} is inappropriate environment")
