FROM apache/airflow:2.9.2-python3.12

USER root
RUN apt-get update -y \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/airflow

# Copy requirements files individually with explicit paths
COPY ./requirements.txt /opt/airflow/requirements.txt
COPY ./requirements_dbt_venv.txt /opt/airflow/requirements_dbt_venv.txt

USER airflow
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

USER root
RUN python -m venv dbt_venv && \
    . dbt_venv/bin/activate && \
    pip install --no-cache-dir --no-user -r /opt/airflow/requirements_dbt_venv.txt && \
    deactivate

USER airflow