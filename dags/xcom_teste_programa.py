from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import XCom
from airflow.utils.session import provide_session

# Argumentos padrão
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

@provide_session
def clear_xcom(session=None, **kwargs):
    """Task que limpa todos os XComs da DAG run atual"""
    ti = kwargs['ti']
    dag_id = ti.dag_id
    run_id = ti.run_id

    # Contar XComs antes
    before_count = session.query(XCom).filter(
        XCom.dag_id == dag_id,
        XCom.run_id == run_id
    ).count()

    # Apagar todos os XComs dessa DAG Run
    deleted = session.query(XCom).filter(
        XCom.dag_id == dag_id,
        XCom.run_id == run_id
    ).delete(synchronize_session=False)

    session.commit()

    # Contar XComs depois
    after_count = session.query(XCom).filter(
        XCom.dag_id == dag_id,
        XCom.run_id == run_id
    ).count()

    print(
        f"[CLEAR XCOM] DAG '{dag_id}', Run '{run_id}' — "
        f"Removidos {deleted} XCom(s). "
        f"Antes: {before_count}, Depois: {after_count}"
    )

# Definição da DAG
with DAG(
    dag_id='teste_xcom_dag',
    default_args=default_args,
    description='DAG para testar XCom e apagar após uso',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['exemplo', 'xcom'],
) as dag:

    push_task = PythonOperator(
        task_id='push_task',
        python_callable=push_xcom,
    )

    pull_task = PythonOperator(
        task_id='pull_task',
        python_callable=pull_xcom,
    )

    clear_task = PythonOperator(
        task_id='clear_task',
        python_callable=clear_xcom,
    )

    push_task >> pull_task >> clear_task
