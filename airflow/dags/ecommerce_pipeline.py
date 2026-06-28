from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id='ecommerce_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule='@weekly',   
    catchup=False,
) as dag:

    clean = BashOperator(
        task_id="clean_data",
        bash_command="python /opt/airflow/scripts/clean_data.py"
    )

    dimensions = BashOperator(
        task_id='create_dimensions',
        bash_command="python /opt/airflow/scripts/create_dimensions.py"
    )

    facts = BashOperator(
        task_id='create_facts',
        bash_command="python /opt/airflow/scripts/create_facts.py"
    )

    upload = BashOperator(
        task_id='upload_to_s3',
        bash_command="python /opt/airflow/scripts/upload_to_s3.py"
    )

    validate = BashOperator(
         task_id='validate_athena',
         bash_command="python /opt/airflow/scripts/athena_validation.py"
      )
    
    clean >> dimensions >> facts >> upload >> validate
