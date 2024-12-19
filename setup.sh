#!/bin/bash

# Create directories if they don't exist
mkdir -p ./dw_postgres_data

# Set permissions
sudo chown -R 999:999 ./dw_postgres_data  # 999 is the postgres user in the container
sudo chmod -R 750 ./dw_postgres_data

# Set Airflow directories permissions
sudo chown -R ${AIRFLOW_UID:-50000}:0 ./airflow
sudo chmod -R 775 ./airflow

echo "Directory structure created and permissions set successfully!"