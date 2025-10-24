import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator



with DAG(
    dag_id="example_python_operator",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
) as dag:
    inicio_dag = EmptyOperator(
        task_id='inicio_dag'
    )

    fim_dag = EmptyOperator(
        task_id='fim_dag'
    )


    inicio_dag >> fim_dag
