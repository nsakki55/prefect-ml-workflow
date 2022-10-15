import os
from dataclasses import dataclass
from enum import Enum
from typing import List

import numpy as np

S3_PREFIX = "prefect-ml-workflow"
DATA_DIR = "./data"


@dataclass
class FeatureInfo:
    names: List[str]
    target: str


@dataclass
class Dataset:
    X: np.array
    y: np.array


@dataclass
class DataInfo:
    index: int
    s3_prefix: str
    data_dir: str
    raw_data_name: str

    def __post_init__(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)

    @property
    def raw_data_s3_key(self) -> str:
        return f"{self.s3_prefix}/{self.raw_data_name}"

    @property
    def raw_data_path(self) -> str:
        return f"{self.data_dir}/{self.raw_data_name}"


@dataclass
class ModelInfo:
    s3_prefix: str
    data_dir: str

    def __post_init__(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)

    @property
    def s3_key(self) -> str:
        return f"{self.s3_prefix}/model"

    @property
    def path(self) -> str:
        return f"{self.data_dir}/model"


class DataType(Enum):
    TRAIN = DataInfo(
        index=0,
        s3_prefix=S3_PREFIX,
        data_dir=DATA_DIR,
        raw_data_name="train.sample",
    )
    TEST = DataInfo(
        index=1,
        s3_prefix=S3_PREFIX,
        data_dir=DATA_DIR,
        raw_data_name="test.sample",
    )


model_info = ModelInfo(s3_prefix=S3_PREFIX, data_dir=DATA_DIR)

feature_info = FeatureInfo(
    names=[
        "id",
        "hour",
        "C1",
        "banner_pos",
        "site_id",
        "site_domain",
        "site_category",
        "app_id",
        "app_domain",
        "app_category",
        "device_id",
        "device_ip",
        "device_model",
        "device_type",
        "device_conn_type",
    ],
    target="click",
)
