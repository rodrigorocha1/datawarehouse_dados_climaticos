CREATE TABLE dbo.LogOperacoesBanco (
    IdLog INT IDENTITY(1,1) PRIMARY KEY,

    Consulta NVARCHAR(MAX)  NULL,
    Nome VARCHAR(200),
    NomeArquivo VARCHAR(200),
    Funcao VARCHAR(200),
    NumeroLinha SMALLINT,
    url NVARCHAR(MAX) NULL,
    Codigo INT NULL,
    JsonRetorno NVARCHAR(MAX) NULL,
    Mensagem VARCHAR(100),
    NIVEL_LOG NVARCHAR(20) NULL DEFAULT 'INFO',
    DataInsercao DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT CHK_NIVEL_LOG CHECK (NIVEL_LOG IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'))

);

SELECT *
FROm LogOperacoesBanco;

TRUNCATE TABLE LogOperacoesBanco;

DROP TABLE LogOperacoesBanco;

SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'LogOperacoesBanco';



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
                   NULL,
                   'tempo_api.py',
                   'TempoApi.buscar_dados_tempo',
                   43,
                   'https://api.openweathermap.org/data/2.5/weather/data/2.5/weather?appid=9c2080633e0fb909505abc4da0d94e7a&units=metric&lang=pt_br&q=Santa+Rita+do+Passa+Quatro%2C+BR%2C+BR',
                   200,
                   '{"coord": {"lon": -47.4781, "lat": -21.7103}, "weather": [{"id": 803, "main": "Clouds", "description": "nublado", "icon": "04n"}], "base": "stations", "main": {"temp": 28.27, "feels_like": 27.08, "temp_min": 28.27, "temp_max": 28.27, "pressure": 1009, "humidity": 25, "sea_level": 1009, "grnd_level": 934}, "visibility": 10000, "wind": {"speed": 2.1, "deg": 147, "gust": 2.04}, "clouds": {"all": 60}, "dt": 1761515701, "sys": {"country": "BR", "sunrise": 1761467383, "sunset": 1761513464}, "timezone": -10800, "id": 3449851, "name": "Santa Rita do Passa Quatro", "cod": 200}',
                   'Sucesso ao Conectar na API',
                   'INFO'
               );



               