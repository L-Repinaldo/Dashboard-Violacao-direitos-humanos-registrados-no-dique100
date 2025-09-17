from NormalizacaoDados.Operacoes.carrega_os_dados_do_ano import carrega_os_dados_por_ano
from NormalizacaoDados.Operacoes.cria_csv_para_cada_grupo_vulneravel import cria_csv_para_cada_grupo_vulneravel


def init(year):

    df_dask_primerio_semestre, df_dask_segundo_semestre = carrega_os_dados_por_ano(year)

    pasta_saida = "NormalizacaoDados/CSV_Gerados"

    cria_csv_para_cada_grupo_vulneravel(df_dask_primerio_semestre, df_dask_segundo_semestre, year, pasta_saida)

    return True

years = [2020, 2021, 2022, 2023, 2024]

for year in years:
    init(year)
