FROM ghcr.io/dbt-labs/dbt-core:1.10.0b2

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Sao_Paulo

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
        curl \
        gnupg2 \
        apt-transport-https \
        lsb-release \
        ca-certificates \
        unixodbc-dev \
        software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Adicionar repositório Microsoft e instalar ODBC Driver 18
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
       > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Instalar dbt-sqlserver
RUN python -m pip install --no-cache-dir dbt-sqlserver

WORKDIR /usr/app/dbt
ENTRYPOINT ["/bin/sh"]
