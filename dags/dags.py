from typing import Any, Final, List

import pendulum
from airflow import DAG
from airflow.models import XCom
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.utils.session import provide_session
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule
from unidecode import unidecode

from src.config.config import Config


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


def processo_etl_stg(cidade: str, **kwargs: Any):
    from src.etl_tempo import EtlTempo
    from src.servicos.api_tempo.tempo_api import TempoApi
    from src.servicos.banco.operacao_banco_sqlserver import OperacaoBancoSQLServer

    etl_tempo = EtlTempo(servico_api=TempoApi(), operacao_banco=OperacaoBancoSQLServer(id_conexao='stg_tempo'))
    etl_tempo.gravar_dados_tabela_temporaria(cidade=cidade, **kwargs)


municipios = [
    'Ribeirão Preto, BR', 'Cravinhos, BR', 'Altinópolis, BR', 'Barrinha, BR',
    'Batatais, BR', 'Cajuru, BR', 'Dumont, BR', 'Guatapará, BR', 'Jaboticabal, BR',
    'Jardinópolis, BR', 'Luís Antônio, BR', 'Monte Alto, BR', 'Morro Agudo, BR',
    'Pitangueiras, BR', 'Pradópolis, BR', 'Sertãozinho, BR', 'Sales Oliveira, BR',
    'São Simão, BR', 'Santa Rita do Passa Quatro, BR'
]
municipios_tratado = [unidecode(m.lower().replace(',', '_').replace(' ', '_')) for m in municipios]

ID_CONEXAO: Final[List[str]] = [Config.ID_BANCO_LOG, Config.ID_BANCO_DW, Config.ID_BANCO_STG]


def registrar_xcom(context):
    """
    Recebe o contexto da task e insere log na tabela dbo.LogOperacoesBanco
    """
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    dag_id = context['dag'].dag_id
    execution_date = context['execution_date']
    try:
        status = 'SUCCESS' if context['task_instance'].state == 'success' else 'FAILURE'
        codigo = 1 if status == 'SUCCESS' else 0
        mensagem = f"Tarefa {task_id} executada com status {status}"

        insert_sql = f"""
        INSERT INTO dbo.LogOperacoesBanco 
        (Consulta, Nome, NomeArquivo, Funcao, NumeroLinha, url, Codigo, JsonRetorno, Mensagem, NIVEL_LOG)
        VALUES 
        (NULL, '{task_id}', '{dag_id}', 'MsSqlOperator', 0, NULL, {codigo}, NULL, '{mensagem}', 'INFO')
        """

        insert_task = MsSqlOperator(
            task_id=f'log_{task_id}',
            mssql_conn_id=Config.ID_BANCO_LOG,
            sql=insert_sql
        )
        insert_task.execute(context)
    except Exception as e:
        print(f"Erro ao registrar log: {e}")


with DAG(
        dag_id="dag_monitoramento_tempo_dw",
        schedule=None,
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        tags=["example"],
) as dag:
    inicio_dag = EmptyOperator(
        task_id='inicio_dag',
        trigger_rule='all_success'
    )

    with TaskGroup('task_testar_conexoes') as tg_con:
        lista_task_conexoes = []
        for id_conexao in ID_CONEXAO:
            task = MsSqlOperator(
                task_id=f'testar_conexao_sqlserver_{id_conexao.lower()}',
                mssql_conn_id=id_conexao,
                sql="SELECT 1 AS resultado;",
                trigger_rule=TriggerRule.ALL_DONE,
                on_success_callback=registrar_xcom,
                on_failure_callback=registrar_xcom
            )
            lista_task_conexoes.append(task)

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
        task_id='fim_dag',
        trigger_rule=TriggerRule.ONE_SUCCESS

    )

    inserir_logs_task_sucesso = MsSqlOperator(
        task_id='inserir_logs_sucesso',
        mssql_conn_id=Config.ID_BANCO_LOG,
        trigger_rule=TriggerRule.ONE_SUCCESS,
        params={'municipios_tratado': municipios_tratado},
        sql="""
           {% for municipio_tratado in params.municipios_tratado %}
               {% set log = ti.xcom_pull(key='mensagem_log_sucesso_' + municipio_tratado) %}
               {% if log and log['NIVEL_LOG'] %}
                   INSERT INTO dbo.LogOperacoesBanco (
                       Consulta,
                       Nome,
                       NomeArquivo,
                       Funcao,
                       NumeroLinha,
                       url,
                       Codigo,
                       JsonRetorno,
                       Mensagem,
                       NIVEL_LOG
                   )
                   VALUES (
                       {{ "'" + log['Consulta'] + "'" if log and log['Consulta'] else 'NULL' }},
                       '{{ log["Nome"] if log else "NULL" }}',
                       '{{ log["NomeArquivo"] if log else "NULL" }}',
                       '{{ log["Funcao"] if log else "NULL" }}',
                       {{ log["NumeroLinha"] if log and log["NumeroLinha"] is not none else 'NULL' }},
                       {{ "'" + log['url'] + "'" if log and log['url'] else 'NULL' }},
                       {{ log["Codigo"] if log and log["Codigo"] is not none else 'NULL' }},
                       {{ "'" + (log["JsonRetorno"] | string) + "'" if log and log["JsonRetorno"] else 'NULL' }},
                       '{{ log["Mensagem"] if log else "NULL" }}',
                       '{{ log["NIVEL_LOG"] }}'
                   );
               {% endif %}
           {% endfor %}
        """,
        dag=dag
    )

    inserir_logs_task_erros = MsSqlOperator(
        task_id='inserir_logs_erros',
        mssql_conn_id=Config.ID_BANCO_LOG,
        trigger_rule=TriggerRule.ONE_FAILED,
        params={'municipios_tratado': municipios_tratado},
        sql="""
           {% for municipio_tratado in params.municipios_tratado %}
               {% set log = ti.xcom_pull(key='mensagem_log_erro_' + municipio_tratado) %}
               {% if log and log['NIVEL_LOG'] %}
                   INSERT INTO dbo.LogOperacoesBanco (
                       Consulta,
                       Nome,
                       NomeArquivo,
                       Funcao,
                       NumeroLinha,
                       url,
                       Codigo,
                       JsonRetorno,
                       Mensagem,
                       NIVEL_LOG
                   )
                   VALUES (
                       {{ "'" + log['Consulta'] + "'" if log and log['Consulta'] else 'NULL' }},
                       '{{ log["Nome"] if log else "NULL" }}',
                       '{{ log["NomeArquivo"] if log else "NULL" }}',
                       '{{ log["Funcao"] if log else "NULL" }}',
                       {{ log["NumeroLinha"] if log and log["NumeroLinha"] is not none else 'NULL' }},
                       {{ "'" + log['url'] + "'" if log and log['url'] else 'NULL' }},
                       {{ log["Codigo"] if log and log["Codigo"] is not none else 'NULL' }},
                       {{ "'" + (log["JsonRetorno"] | string) + "'" if log and log["JsonRetorno"] else 'NULL' }},
                       '{{ log["Mensagem"] if log else "NULL" }}',
                       '{{ log["NIVEL_LOG"] }}'
                   );
               {% endif %}
           {% endfor %}
        """,
        dag=dag
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


    apagar_xcom = PythonOperator(
        task_id='clear_task',
        python_callable=clear_xcom,
    )

    inicio_dag >> tg_con >> tg_mun >> [inserir_logs_task_sucesso, inserir_logs_task_erros]
    inserir_logs_task_sucesso >> apagar_xcom >> fim_dag
    inserir_logs_task_erros >> apagar_xcom >> fim_dag
