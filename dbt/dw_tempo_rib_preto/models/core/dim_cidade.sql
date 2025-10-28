{{ config(
    materialized='incremental',
    database='DW_TEMPO',


    alias='DIM_CIDADE',
    unique_key='ID_CIDADE'
) }}

SELECT DISTINCT
    ID_CIDADE AS ID_CIDADE,
    NOME      AS NOME_CIDADE
FROM {{ source('stg_dw_tempo', 'STG_DADOS_TEMPO') }}

{% if is_incremental() %}
  -- Adiciona apenas novos registros
  WHERE ID_CIDADE NOT IN (
      SELECT ID_CIDADE FROM {{ this }}
  )
{% endif %}
