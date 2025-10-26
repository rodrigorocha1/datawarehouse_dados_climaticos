{{ config(
    materialized='incremental',
    database='DW_TEMPO',

    alias='DIM_CALENDARIO',
    unique_key=['DATA_CALENDARIO', 'HORA']
) }}

WITH calendario_base AS (
    SELECT DISTINCT
        CAST(DATA_CONSULTA AS DATE) AS DATA_CALENDARIO,
        CAST(DATA_CONSULTA AS TIME) AS HORA,
        YEAR(DATA_CONSULTA) AS ANO,
        MONTH(DATA_CONSULTA) AS MES,
        DAY(DATA_CONSULTA) AS DIA,
        DATEPART(QUARTER, DATA_CONSULTA) AS TRIMESTRE,
        DATEPART(WEEK, DATA_CONSULTA) AS SEMANA_DO_ANO,
        DATEPART(WEEKDAY, DATA_CONSULTA) AS DIA_DA_SEMANA,
        DATENAME(MONTH, DATA_CONSULTA) AS NOME_MES,
        DATENAME(WEEKDAY, DATA_CONSULTA) AS NOME_DIA_SEMANA,
        FORMAT(DATA_CONSULTA, 'yyyy-MM') AS ANO_MES,
        CASE
            WHEN CAST(DATA_CONSULTA AS TIME) BETWEEN '06:00:00' AND '11:59:59' THEN 'MANHÃ'
            WHEN CAST(DATA_CONSULTA AS TIME) BETWEEN '12:00:00' AND '17:59:59' THEN 'TARDE'
            ELSE 'NOITE'
        END AS TURNO
    FROM {{ source('stg_dw_tempo', 'STG_DADOS_TEMPO') }}
)

SELECT *
FROM calendario_base

{% if is_incremental() %}
WHERE NOT EXISTS (
    SELECT 1
    FROM {{ this }} AS existing
    WHERE existing.DATA_CALENDARIO = CAST(calendario_base.DATA_CALENDARIO AS DATE)
      AND existing.HORA = CAST(calendario_base.HORA AS TIME)
)
{% endif %}
