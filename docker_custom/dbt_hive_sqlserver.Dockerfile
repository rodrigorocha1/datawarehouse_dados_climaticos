# Imagem base do dbt-core
FROM ghcr.io/dbt-labs/dbt-core:1.10.0b2

LABEL maintainer="Rodrigo Rocha <rodrigo@example.com>"
LABEL description="Imagem personalizada do dbt-core com suporte a SQL Server (ODBC Driver 18)"

# Instalar dependências e ODBC Driver 18
USER root

RUN apt-get update && apt-get install -y curl gnupg2 apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list -o /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar o adaptador dbt-sqlserver
RUN pip install --no-cache-dir dbt-sqlserver==1.9.0

# Diretório de trabalho do projeto dbt
WORKDIR /usr/app/dbt



# Ajustar permissões
RUN chmod -R 755 /usr/app/dbt

# Usuário padrão
USER dbt

# Comando padrão
ENTRYPOINT ["dbt"]
