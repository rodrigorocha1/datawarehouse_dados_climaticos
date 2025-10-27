# Estimativa do tamanho do Data Warehouse em MB

# Número de linhas esperadas
num_cidades = 1000
anos_calendario = 10
registros_por_dia = 24  # 1 registro por hora
num_cidades_ft = 1000

# DIM_CIDADE
tamanho_dim_cidade = 4 + 255*2  # ID_CIDADE (INT=4 bytes) + NOME_CIDADE NVARCHAR(255)=510 bytes
tamanho_total_dim_cidade = tamanho_dim_cidade * num_cidades / (1024*1024)  # MB

# DIM_CALENDARIO
tamanho_dim_calendario = (
    3 +  # DATA_CALENDARIO DATE
    3 +  # HORA TIME
    4*6 +  # 6 INTs
    20 + 20 + 7 + 20  # VARCHARs
)
linhas_dim_calendario = anos_calendario * 365 * registros_por_dia
tamanho_total_dim_calendario = tamanho_dim_calendario * linhas_dim_calendario / (1024*1024)  # MB

# FT_CLIMA
tamanho_ft_clima = (
    4 +  # ID_CIDADE INT
    3 +  # DATA_CONSULTA DATE
    3 +  # HORA_CONSULTA TIME
    5 +  # TEMPERATURA DECIMAL(5,2)
    9 +  # PRESSAO DECIMAL(7,2)
    2 +  # UMIDADE SMALLINT
    5 +  # VELOCIDADE_VENTO DECIMAL(5,2)
    5 +  # ANGULO_VENTO DECIMAL(5,2)
    255*2  # NOME_CIDADE NVARCHAR(255)
)
linhas_ft_clima = num_cidades_ft * registros_por_dia * 365 * anos_calendario
tamanho_total_ft_clima = tamanho_ft_clima * linhas_ft_clima / (1024*1024)  # MB

# Total estimado
tamanho_total_dw = tamanho_total_dim_cidade + tamanho_total_dim_calendario + tamanho_total_ft_clima

# Exibe resultados
print(f"Tamanho DIM_CIDADE: {tamanho_total_dim_cidade:.4f} MB")
print(f"Tamanho DIM_CALENDARIO: {tamanho_total_dim_calendario:.4f} MB")
print(f"Tamanho FT_CLIMA: {tamanho_total_ft_clima/1024:.4f} GB")  # Convertendo para GB
print(f"Tamanho total estimado do DW: {tamanho_total_dw/1024:.4f} GB")
