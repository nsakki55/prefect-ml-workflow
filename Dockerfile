FROM python:3.8.6-slim

WORKDIR /opt/prefect

COPY config.toml /opt/prefect/config.toml
COPY flow_components /opt/prefect/flow_components/
COPY requirements.txt /opt/prefect/

RUN pip install --upgrade pip \
	&& pip install -r /opt/prefect/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/opt/prefect/flow_components/:"