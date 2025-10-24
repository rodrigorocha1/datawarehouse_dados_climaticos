# Dockerfile otimizado para Airflow 2.10.4 com pacotes adicionais

ARG AIRFLOW_IMAGE_NAME=apache/airflow:2.10.4
FROM ${AIRFLOW_IMAGE_NAME}

# Variável com pacotes adicionais
ENV PIP_ADDITIONAL_REQUIREMENTS="apache-airflow-providers-microsoft-mssql[common.sql] paramiko<3.0 dbt-sqlserver"

# Troca para usuário airflow
USER airflow

# Atualiza pip de forma segura
RUN python -m pip install --upgrade pip

# Instala cada pacote separadamente para facilitar debug e reduzir chances de cancelamento
RUN pip install --no-cache-dir apache-airflow-providers-microsoft-mssql[common.sql] \
    && pip install --no-cache-dir dbt-sqlserver

# Volta para usuário airflow (por padrão já é airflow)
USER airflow
