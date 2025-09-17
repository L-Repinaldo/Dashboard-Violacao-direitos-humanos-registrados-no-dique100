import os
import dask.dataframe as dd

def cria_csv_para_cada_grupo_vulneravel(df_primeiro_semestre, df_segundo_semestre, year, pasta_saida):

    cria_csv_primeiro_semestre(df_primeiro_semestre, year, pasta_saida)
    cria_csv_segundo_semestre(df_segundo_semestre, year, pasta_saida)

    

def cria_csv_primeiro_semestre(df_first, year, pasta_saida):
    """
    Cria CSVs do primeiro semestre, organizados por ano e grupo vulnerável.
    """
    try:
        year = str(year)

        # Padroniza strings: remove espaços e coloca tudo em minúsculo
        df_first['Grupo vulnerável'] = df_first['Grupo vulnerável'].str.strip().str.lower()

        # Obtém grupos únicos do primeiro semestre
        grupos = df_first['Grupo vulnerável'].dropna().unique().compute()

        for grupo in grupos:
            # Caminho completo: pasta base / ano / grupo
            grupo_dir = os.path.join(pasta_saida, year, grupo.replace("/", "_"))
            os.makedirs(grupo_dir, exist_ok=True)

            # Filtra o grupo
            df_grupo = df_first[df_first['Grupo vulnerável'] == grupo].compute()

            # Salva o CSV
            arquivo_csv = os.path.join(grupo_dir, f"Primeiro_semestre_{year}.csv")
            df_grupo.to_csv(arquivo_csv, sep=";", index=False, encoding="utf-8-sig")

            print(f"[OK] {grupo} → Primeiro semestre salvo em {grupo_dir}")

        print(f"\nProcesso finalizado para o primeiro semestre de {year}!")

    except Exception as e:
        print(f"Erro ao criar CSV do primeiro semestre: {e}")


def cria_csv_segundo_semestre(df_second, year, pasta_saida):
    """
    Cria CSVs do segundo semestre, organizados por ano e grupo vulnerável.
    """
    try:
        year = str(year)

        # Padroniza strings: remove espaços e coloca tudo em minúsculo
        df_second['Grupo vulnerável'] = df_second['Grupo vulnerável'].str.strip().str.lower()

        # Obtém grupos únicos do segundo semestre
        grupos = df_second['Grupo vulnerável'].dropna().unique().compute()

        for grupo in grupos:
            # Caminho completo: pasta base / ano / grupo
            grupo_dir = os.path.join(pasta_saida, year, grupo.replace("/", "_"))
            os.makedirs(grupo_dir, exist_ok=True)

            # Filtra o grupo
            df_grupo = df_second[df_second['Grupo vulnerável'] == grupo].compute()

            # Salva o CSV
            arquivo_csv = os.path.join(grupo_dir, f"Segundo_semestre_{year}.csv")
            df_grupo.to_csv(arquivo_csv, sep=";", index=False, encoding="utf-8-sig")

            print(f"[OK] {grupo} → Segundo semestre salvo em {grupo_dir}")

        print(f"\nProcesso finalizado para o segundo semestre de {year}!")

    except Exception as e:
        print(f"Erro ao criar CSV do segundo semestre: {e}")
