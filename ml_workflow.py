import prefect
from flow_components import run_name_handler, set_executor, set_run_config, set_schedule, set_storage
from flow_components.model_entity import DataType, model_info
from flow_components.task import (
    convert_string_to_dataframe_task,
    preprocess_task,
    s3_download_task,
    save_as_pickle_task,
    train_task,
    upload_s3_task,
    validate_task,
)
from prefect import Flow, Parameter

FLOW_NAME = "ml-workflow"

with Flow(
    name=FLOW_NAME,
    storage=set_storage(image_tag="latest"),
    run_config=set_run_config(flow_name=FLOW_NAME, cpu=2048, memory=8192),
    schedule=set_schedule(cron="0 01-23/1 * * *"),
    state_handlers=[run_name_handler],
    executor=set_executor(n_workers=2),
) as flow:
    fit_intercept = Parameter("fit_intercept", default=True)
    penalty = Parameter("penalty", default="l2")
    random_state = Parameter("random_state", default=42)

    raw_str_data = s3_download_task.map([datatype.value.raw_data_s3_key for datatype in DataType])
    raw_data = convert_string_to_dataframe_task.map(raw_str_data)

    preprocessed_data = preprocess_task.map(data=raw_data)

    model = train_task(
        dataset=preprocessed_data[DataType.TRAIN.value.index],
        fit_intercept=fit_intercept,
        penalty=penalty,
        random_state=random_state,
    )
    validate_task(model=model, dataset=preprocessed_data[DataType.TEST.value.index], upstream_tasks=[model])
    save_model = save_as_pickle_task(data=model, path=model_info.path, upstream_tasks=[model])
    upload_s3_task(
        s3_bucket=prefect.config.s3_bucket, s3_key=model_info.s3_key, file_path=model_info.path, upstream_tasks=[save_model]
    )
