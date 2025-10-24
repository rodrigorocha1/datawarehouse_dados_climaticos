from typing import Any

import pendulum
from airflow import DAG
from airflow.models import XCom
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.session import provide_session


def processo_etl_stg(cidade: str, **kwargs: Any):
    from src.etl_tempo import EtlTempo
    from src.servicos.api_tempo.tempo_api import TempoApi
    from src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer

    etl_tempo = EtlTempo(servico_api=TempoApi(),operacao_banco=OperacaoBancoSQLServer(id_conexao='stg_tempo'))
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


    inicio_dag >> tempo_operator >> fim_dag
