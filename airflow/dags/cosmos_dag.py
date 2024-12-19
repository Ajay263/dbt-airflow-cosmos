import os
import pendulum
from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ProjectConfig, ExecutionConfig, ProfileConfig, RenderConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.constants import LoadMode, TestBehavior

# Get the workspace root directory
WORKSPACE_ROOT = os.getenv('GITHUB_WORKSPACE', '/workspaces/dbt-airflow-cosmos')

# Configure paths
DBT_PROJECT_PATH = os.path.join(WORKSPACE_ROOT, 'datawarehouse')
DBT_PROFILES_DIR = os.path.join(WORKSPACE_ROOT, 'airflow', '.dbt')

# Configure profile using PostgresUserPasswordProfileMapping with your specific connection details
profile_config = ProfileConfig(
    profile_name="datawarehouse",  # Changed to match your profiles.yml
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="datawarehouse_db",  # We'll need to create this connection in Airflow
        profile_args={
            "schema": "dev",
            "database": "airbnb_datawarehouse",
            "host": "172.19.0.6",
            "port": 5432,
            "user": "datawarehouse_admin",
            "password": "secure_dw_password_2024!",
            "threads": 4
        },
    ),
)

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': pendulum.duration(minutes=5),
}

@dag(
    schedule_interval="@daily",
    start_date=pendulum.datetime(2024, 1, 1),
    catchup=False,
    tags=["dbt"],
    max_active_runs=1,
    max_active_tasks=5,
    default_args=default_args
)
def dbt_cosmos_dag():
    """
    DAG using Cosmos for dbt orchestration with PostgreSQL connection
    """
    pre_dbt = EmptyOperator(task_id="pre_dbt")

    dbt_tasks = DbtTaskGroup(
        group_id="dbt_tasks",
        project_config=ProjectConfig(
            dbt_project_path=DBT_PROJECT_PATH,
            manifest_path=f"{DBT_PROJECT_PATH}/target/manifest.json",
            dbt_vars={
                "start_date": "{{ data_interval_start }}",
                "end_date": "{{ data_interval_end }}"
            },
            partial_parse=False,
        ),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=os.path.join(WORKSPACE_ROOT, 'airflow', 'dbt_venv', 'bin', 'dbt'),
        ),
        render_config=RenderConfig(
            load_method=LoadMode.DBT_MANIFEST,
            test_behavior=TestBehavior.AFTER_ALL,
            dbt_deps=False,
        ),
        operator_args={
            "env": {
                "DBT_PROFILES_DIR": DBT_PROFILES_DIR,
                "DBT_PROJECT_DIR": DBT_PROJECT_PATH
            }
        }
    )

    post_dbt = EmptyOperator(task_id="post_dbt")

    # Set task dependencies
    pre_dbt >> dbt_tasks >> post_dbt

dag = dbt_cosmos_dag()