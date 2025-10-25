from typing import Any, Final, List

import pendulum
from airflow import DAG
from airflow.models import XCom
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.utils.session import provide_session
from airflow.utils.task_group import TaskGroup
from unidecode import unidecode

from src.config.config import Config


def processo_etl_stg(cidade: str, **kwargs: Any):
    from src.etl_tempo import EtlTempo
    from src.servicos.api_tempo.tempo_api import TempoApi
    from src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer

    etl_tempo = EtlTempo(servico_api=TempoApi(), operacao_banco=OperacaoBancoSQLServer(id_conexao='stg_tempo'))
    etl_tempo.gravar_dados_tabela_temporaria(cidade=cidade, **kwargs)


municipios = ['Ribeirão Preto, BR', 'Cravinhos, BR']
ID_CONEXAO: Final[List[str]] = [Config.ID_BANCO_LOG, Config.ID_BANCO_DW, Config.ID_BANCO_STG]

with DAG(
        dag_id="dag_monitoramento_tempo_dw",

        schedule=None,
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        tags=["example"],
) as dag:
    inicio_dag = EmptyOperator(
        task_id='inicio_dag'
    )

    with TaskGroup('task_testar_conexoes') as tg_con:
        lista_task_conexoes = []
        for id_conexao in ID_CONEXAO:
            testar_conexao = MsSqlOperator(
                task_id=f'testar_conexao_sqlserver_{id_conexao.lower()}',
                mssql_conn_id=id_conexao,
                sql="SELECT 1 AS resultado;",
            )
            lista_task_conexoes.append(testar_conexao)

    with TaskGroup('task_municipios') as tg_mun:
        lista_task_canais = []
        for municipio in municipios:
            tempo_operator = PythonOperator(
                task_id=f'tempo_operator_{unidecode(municipio.lower().replace(",", "_", ).replace(" ", "_"))}',
                python_callable=processo_etl_stg,
                op_kwargs={
                    'cidade': municipio
                }
            )
            lista_task_canais.append(tempo_operator)

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


    inicio_dag >> tg_con >> tg_mun >> fim_dag
