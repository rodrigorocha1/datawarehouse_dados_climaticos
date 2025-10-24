from typing import Any

import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def processo_etl_stg(cidade: str, **kwargs: Any):
    from src.etl_tempo import EtlTempo
    from src.servicos.api_tempo.tempo_api import TempoApi

    etl_tempo = EtlTempo(servico_api=TempoApi())
    etl_tempo.gravar_dados_tabela_temporaria(cidade=cidade, **kwargs)


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

    tempo_operator = PythonOperator(
        task_id='tempo_operator',
        python_callable=processo_etl_stg,
        op_kwargs={
            'cidade': 'Ribeirão Preto, Br'
        }
    )

    fim_dag = EmptyOperator(
        task_id='fim_dag'
    )

    inicio_dag >> tempo_operator >> fim_dag
