import io
import pickle
from typing import Any

import boto3
import numpy as np
import pandas as pd
import prefect
from prefect import task
from prefect.tasks.aws import S3Download
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss

from .handler import notification_handler
from .model_entity import Dataset, feature_info

s3_download_task = S3Download(bucket=prefect.config.s3_bucket)


@task(name="upload to s3 task", log_stdout=True)
def upload_s3_task(s3_bucket: str, s3_key: str, file_path: str) -> None:
    """S3にローカルファイルをアップロード."""
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3_bucket)
    bucket.upload_file(Key=s3_key, Filename=file_path)


@task(name="convert string to dataframe task", log_stdout=True)
def convert_string_to_dataframe_task(data: str) -> pd.DataFrame:
    """文字列データをDataFrameとして読み込み."""
    df = pd.read_csv(io.StringIO(data))
    return df


@task(name="preprocess task", log_stdout=True)
def preprocess_task(data: pd.DataFrame) -> Dataset:
    """生データをFeatureHasherにかけ,学習用データを作成"""
    feature_hasher = FeatureHasher(n_features=2 ** 24, input_type="string")
    hashed_feature = feature_hasher.fit_transform(
        np.asanyarray(data[[feature_name for feature_name in feature_info.names]].astype(str))
    )
    dataset = Dataset(X=hashed_feature, y=data[feature_info.target])
    return dataset


@task(name="save pickle task", log_stdout=True)
def save_as_pickle_task(data: Any, path: str) -> None:
    """データオブジェクトをpickleとして保存"""
    with open(path, "wb") as f:
        pickle.dump(data, f)


@task(name="train model task", log_stdout=True, state_handlers=notification_handler())
def train_task(dataset: Dataset, **kwargs: Any) -> SGDClassifier:
    """SGDClassifierの学習を実行"""
    model = SGDClassifier(loss="log", **kwargs)
    model.partial_fit(dataset.X, dataset.y, classes=[0, 1])
    return model


@task(name="validate model task", log_stdout=True)
def validate_task(model: SGDClassifier, dataset: Dataset) -> None:
    """テストデータでモデル評価"""
    y_pred = model.predict_proba(dataset.X)
    print(f"Finished validate model.logloss: {log_loss(dataset.y, y_pred)}")
