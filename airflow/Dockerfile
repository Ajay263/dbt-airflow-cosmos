FROM apache/airflow:2.10.2

USER root
# Install necessary packages including PostgreSQL development files
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    make \
    gosu \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create directory for PostgreSQL data
RUN mkdir -p /var/lib/postgresql/data && \
    chown -R 999:999 /var/lib/postgresql/data && \
    chmod -R 750 /var/lib/postgresql/data

# Switch back to airflow user for remaining operations
USER airflow

# Set the working directory
WORKDIR /opt/airflow

# Install all Python packages in a single RUN command to reduce layers
RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.9 \
    apache-airflow==2.10.2 \
    "apache-airflow[statsd]" \
    apache-airflow-providers-postgres \
    python-dotenv \
    numpy==1.26.4 \
    pandas \
    tqdm \
    dbt-core \
    dbt-postgres \
    "astronomer-cosmos>=1.0.3" \
    apache-airflow-providers-docker==2.1.0

# Copy the entire project directory into the container
COPY --chown=airflow:root . .

# Set the PYTHONPATH environment variable to include the project root
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"