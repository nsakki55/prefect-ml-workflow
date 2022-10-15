import prefect
from dask_cloudprovider.aws import FargateCluster
from prefect.executors import DaskExecutor, Executor, LocalDaskExecutor


def fargate_cluster(n_workers: int = 2, cpu: int = 1024, memory: int = 2048) -> FargateCluster:
    """Dask用のFargateCluster作成"""
    cluster_kwargs = dict(
        n_workers=n_workers,
        image=f"{prefect.config.ecr_repository}{prefect.config.image_name}",
        cluster_arn=prefect.config.cluster_arn,
        skip_cleanup=True,
        task_role_arn=prefect.config.task_role_arn,
        execution_role_arn=prefect.config.task_execution_role_arn,
        security_groups=prefect.config.security_groups,
        subnets=prefect.config.subnets,
        vpc=prefect.config.vpc,
        cloudwatch_logs_group=prefect.config.aws_log_group,
        scheduler_timeout="5 minutes",
        fargate_use_private_ip=True,
        find_address_timeout=120,
        scheduler_cpu=cpu,
        scheduler_mem=memory,
        worker_cpu=cpu,
        worker_mem=memory,
    )
    return FargateCluster(**cluster_kwargs)


def set_executor(n_workers: int = 2) -> Executor:
    if prefect.config.system_env == "production":
        return DaskExecutor(
            cluster_class=fargate_cluster,
            cluster_kwargs={"n_workers": n_workers},
        )
    elif prefect.config.system_env == "develop":
        return LocalDaskExecutor(n_workers=n_workers)

    else:
        raise ValueError(f"{prefect.config.system_env} is inappropriate environment")
