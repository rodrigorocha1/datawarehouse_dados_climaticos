from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.state import State
from airflow.models import XCom

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,
}

def push_xcom(**kwargs):
    """Task que envia um valor para XCom"""
    value = "Olá XCom!"
    kwargs['ti'].xcom_push(key='mensagem', value=value)
    print(f"Valor enviado para XCom: {value}")

def pull_xcom(**kwargs):
    """Task que lê o valor de XCom"""
    ti = kwargs['ti']
    mensagem = ti.xcom_pull(key='mensagem', task_ids='push_task')
    print(f"Valor recebido do XCom: {mensagem}")

def clear_xcom(**kwargs):
    """Task que limpa os XComs"""
    ti = kwargs['ti']
    session = kwargs['session']
    # Apaga todos os XComs da DAG run atual
    XCom.clear(dag_id=ti.dag_id, run_id=ti.run_id, session=session)
    print("XComs apagados!")

with DAG(
    dag_id='teste_xcom_dag',
    default_args=default_args,
    description='DAG para testar XCom e apagar após uso',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['exemplo'],
) as dag:

    push_task = PythonOperator(
        task_id='push_task',
        python_callable=push_xcom,
        provide_context=True
    )

    pull_task = PythonOperator(
        task_id='pull_task',
        python_callable=pull_xcom,
        provide_context=True
    )

    clear_task = PythonOperator(
        task_id='clear_task',
        python_callable=clear_xcom,
        provide_context=True
    )

    # Definindo a ordem de execução
    push_task >> pull_task >> clear_task
