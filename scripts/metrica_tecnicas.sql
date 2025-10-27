SELECT 
    t.NAME AS Tabela,
    s.NAME AS Esquema,
    p.rows AS Total_Linhas,
    CAST(ROUND((SUM(a.total_pages) * 8.0) / 1024, 4) AS DECIMAL(18,4)) AS Tamanho_MB,
    CAST(ROUND((SUM(a.used_pages) * 8.0) / 1024, 4) AS DECIMAL(18,4)) AS Usado_MB,
    CAST(ROUND((SUM(a.data_pages) * 8.0) / 1024, 4) AS DECIMAL(18,4)) AS Dados_MB
FROM 
    sys.tables t
INNER JOIN      
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN 
    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN 
    sys.allocation_units a ON p.partition_id = a.container_id
INNER JOIN 
    sys.schemas s ON t.schema_id = s.schema_id
WHERE 
    t.is_ms_shipped = 0
GROUP BY 
    t.Name, s.Name, p.Rows
ORDER BY 
    Tamanho_MB DESC;



/*


O que ele retorna:

Tabela: nome da tabela

Esquema: schema da tabela (ex.: dbo)

Total_Linhas: quantidade de registros

Tamanho_MB: tamanho total da tabela (dados + índices)

Usado_MB: espaço usado incluindo índices

*/

-- o tamanho total do Data Warehouse

SELECT 
    CAST(ROUND(SUM(a.total_pages) * 8.0 / 1024, 4) AS DECIMAL(18,4)) AS Tamanho_Total_MB,
    CAST(ROUND(SUM(a.used_pages) * 8.0 / 1024, 4) AS DECIMAL(18,4)) AS Usado_Total_MB,
    CAST(ROUND(SUM(a.data_pages) * 8.0 / 1024, 4) AS DECIMAL(18,4)) AS Dados_Total_MB
FROM 
    sys.tables t
INNER JOIN      
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN 
    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN 
    sys.allocation_units a ON p.partition_id = a.container_id
WHERE 
    t.is_ms_shipped = 0;




DECLARE @CARGAS_DIARIAS INT = 3;
DECLARE @DIAS_MES INT = 30;
DECLARE @DIAS_ANO INT = 365;

SELECT 
    t.NAME AS Tabela,
    s.NAME AS Esquema,
    p.rows AS Total_Linhas,
    CAST(ROUND((SUM(a.total_pages) * 8.0) / 1024, 4) AS DECIMAL(18,4)) AS Tamanho_MB,
    
    -- Crescimento estimado
    CAST(ROUND((SUM(a.total_pages) * 8.0 / 1024) * @CARGAS_DIARIAS, 4) AS DECIMAL(18,4)) AS Crescimento_Diario_MB,
    CAST(ROUND((SUM(a.total_pages) * 8.0 / 1024) * @CARGAS_DIARIAS * @DIAS_MES, 4) AS DECIMAL(18,4)) AS Crescimento_Mensal_MB,
    CAST(ROUND((SUM(a.total_pages) * 8.0 / 1024) * @CARGAS_DIARIAS * @DIAS_ANO, 4) AS DECIMAL(18,4)) AS Crescimento_Anual_MB

FROM 
    sys.tables t
INNER JOIN      
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN 
    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN 
    sys.allocation_units a ON p.partition_id = a.container_id
INNER JOIN 
    sys.schemas s ON t.schema_id = s.schema_id
WHERE 
    t.is_ms_shipped = 0
GROUP BY 
    t.Name, s.Name, p.Rows, s.Name
ORDER BY 
    Tamanho_MB DESC;

--- tamanho total do Data Warehouse e estima o crescimento diário, mensal e anual

DECLARE @CARGAS_DIARIAS INT = 3;
DECLARE @DIAS_MES INT = 30;
DECLARE @DIAS_ANO INT = 365;

SELECT 
    CAST(ROUND(SUM(a.total_pages) * 8.0 / 1024, 4) AS DECIMAL(18,4)) AS Tamanho_Total_MB,
    CAST(ROUND(SUM(a.used_pages) * 8.0 / 1024, 4) AS DECIMAL(18,4)) AS Usado_Total_MB,
    CAST(ROUND(SUM(a.data_pages) * 8.0 / 1024, 4) AS DECIMAL(18,4)) AS Dados_Total_MB,

    -- Crescimento estimado
    CAST(ROUND((SUM(a.total_pages) * 8.0 / 1024) * @CARGAS_DIARIAS, 4) AS DECIMAL(18,4)) AS Crescimento_Diario_MB,
    CAST(ROUND((SUM(a.total_pages) * 8.0 / 1024) * @CARGAS_DIARIAS * @DIAS_MES, 4) AS DECIMAL(18,4)) AS Crescimento_Mensal_MB,
    CAST(ROUND((SUM(a.total_pages) * 8.0 / 1024) * @CARGAS_DIARIAS * @DIAS_ANO, 4) AS DECIMAL(18,4)) AS Crescimento_Anual_MB

FROM 
    sys.tables t
INNER JOIN      
    sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN 
    sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN 
    sys.allocation_units a ON p.partition_id = a.container_id
WHERE 
    t.is_ms_shipped = 0;
