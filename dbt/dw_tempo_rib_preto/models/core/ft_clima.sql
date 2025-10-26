{{
config(
    materialized='incremental',
    database='DW_TEMPO',
    alias='FT_CLIMA',
    unique_key=['ID_CIDADE', 'DATA_CONSULTA', 'HORA_CONSULTA']
)
}}

WITH base AS (
    SELECT
        stg.ID_CIDADE,
        CAST(stg.DATA_CONSULTA AS DATE) AS DATA_CONSULTA,
        CAST(stg.DATA_CONSULTA AS TIME) AS HORA_CONSULTA,
        stg.TEMPERATURA,
        stg.PRESSAO,
        stg.UMIDADE,
        stg.VELOCIDADE_VENTO,
        stg.ANGULO_VENTO
    FROM {{ source('stg_dw_tempo', 'STG_DADOS_TEMPO') }} stg
    LEFT JOIN {{ source('dw_tempo', 'DIM_CIDADE') }} cidade
        ON stg.ID_CIDADE = cidade.ID_CIDADE
)

SELECT *
FROM base

{% if is_incremental() %}
WHERE NOT EXISTS (
    SELECT 1
    FROM {{ this }} t
    WHERE t.ID_CIDADE = base.ID_CIDADE
      AND t.DATA_CONSULTA = base.DATA_CONSULTA
      AND t.HORA_CONSULTA = base.HORA_CONSULTA
)
{% endif %}

