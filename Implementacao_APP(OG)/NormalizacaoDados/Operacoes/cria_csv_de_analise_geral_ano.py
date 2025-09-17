# gerar_frequencias_por_ano_por_grupo.py
import os
import pandas as pd

# ----- CONFIG -----
BASE_DIR = r"C:\Users\lucas\Artigo IC\Artigo Violência\Dados csv\Dados por Grupos Vulneráveis"
OUTPUT_FILENAME_TEMPLATE = "frequencias_{}.csv"
TOTALS_SUMMARY_NAME = "totais_por_ano.csv"
INVALID_TOKENS = {"", "nan", "nd", "<na>"}  # tokens inválidos (comparação em lower)
# ------------------

def encontrar_pasta_grupos(year_path):
    """Retorna caminho da pasta que contém 'Grupos' (case-insensitive) ou None."""
    for nome in os.listdir(year_path):
        caminho = os.path.join(year_path, nome)
        if os.path.isdir(caminho) and "grupo" in nome.lower():
            return caminho
    return None

def coletar_csvs_do_grupo(group_dir):
    """Retorna lista de CSVs encontrados dentro da pasta do grupo (direto e em subpastas)."""
    arquivos = []
    # arquivos diretamente na pasta do grupo
    for f in os.listdir(group_dir):
        p = os.path.join(group_dir, f)
        if os.path.isfile(p) and f.lower().endswith(".csv"):
            arquivos.append(p)
    # arquivos em subpastas (ex.: Primeiro_semestre, Segundo_semestre)
    for entry in os.listdir(group_dir):
        sub = os.path.join(group_dir, entry)
        if os.path.isdir(sub):
            for f in os.listdir(sub):
                p = os.path.join(sub, f)
                if os.path.isfile(p) and f.lower().endswith(".csv"):
                    arquivos.append(p)
    return sorted(set(arquivos))

def ler_csv_tolerante(path):
    """Tenta ler CSV com separador ';' ou ',' e encodings comuns. Retorna DataFrame ou None."""
    tries = [
        {'sep': ';', 'encoding': 'utf-8-sig'},
        {'sep': ',', 'encoding': 'utf-8-sig'},
        {'sep': ';', 'encoding': 'latin1'},
        {'sep': ',', 'encoding': 'latin1'}
    ]
    for t in tries:
        try:
            return pd.read_csv(path, sep=t['sep'], encoding=t['encoding'], dtype=str)
        except Exception:
            continue
    # se falhar, retorna None
    return None

def contar_linhas_validas_em_df(df):
    """
    Considera uma linha válida se **nem todas** as células forem tokens inválidos.
    Converte tudo para string, faz strip/lower e verifica .
    """
    if df is None or df.shape[1] == 0:
        return 0
    df_str = df.astype(str).applymap(lambda x: x.strip().lower() if isinstance(x, str) else str(x).strip().lower())
    # True quando célula é um token inválido
    mask_invalid_cells = df_str.isin(INVALID_TOKENS)
    # linha inválida quando todas as células são inválidas
    linhas_todas_invalidas = mask_invalid_cells.all(axis=1)
    # linha válida = not todas inválidas
    n_validas = (~linhas_todas_invalidas).sum()
    return int(n_validas)

def processar_ano(ano_dir, ano):
    grupos_dir = encontrar_pasta_grupos(ano_dir)
    if not grupos_dir:
        print(f"[PULAR] {ano}: pasta 'Grupos Vulneráveis' não encontrada em {ano_dir}")
        return None

    grupos = [d for d in os.listdir(grupos_dir) if os.path.isdir(os.path.join(grupos_dir, d))]
    if not grupos:
        print(f"[PULAR] {ano}: não há subpastas de grupos em {grupos_dir}")
        return None

    resultados = []  # lista de (grupo, contagem)
    total_ano = 0

    for grupo in sorted(grupos):
        group_dir = os.path.join(grupos_dir, grupo)
        csvs = coletar_csvs_do_grupo(group_dir)
        if not csvs:
            # sem arquivos CSV nessa subpasta — considera zero e continua
            print(f"  [AVISO] {ano} / {grupo}: nenhum CSV encontrado (contagem = 0).")
            continue

        count_grupo = 0
        for csv_path in csvs:
            df = ler_csv_tolerante(csv_path)
            if df is None:
                print(f"    [ERRO] Não foi possível ler {csv_path}. Pulando arquivo.")
                continue
            # remove colunas totalmente vazias para acelerar (opcional)
            df = df.dropna(how="all", axis=1)
            n_valid = contar_linhas_validas_em_df(df)
            count_grupo += n_valid

        if count_grupo > 0:
            resultados.append((grupo, count_grupo))
            total_ano += count_grupo
        else:
            print(f"  [INFO] {ano} / {grupo}: 0 registros válidos.")

    if not resultados:
        print(f"[AVISO] {ano}: nenhum registro válido em nenhum grupo.")
        return 0  # ano processado mas sem registros

    # monta DataFrame ordenado
    df_freq = pd.DataFrame(resultados, columns=["Grupo vulnerável", "Frequência absoluta"])
    df_freq = df_freq.sort_values("Frequência absoluta", ascending=False).reset_index(drop=True)
    df_freq["Frequência relativa (%)"] = (df_freq["Frequência absoluta"] / total_ano * 100).round(2)

    # adiciona linha TOTAL GERAL
    linha_total = pd.DataFrame([{
        "Grupo vulnerável": "TOTAL GERAL",
        "Frequência absoluta": total_ano,
        "Frequência relativa (%)": 100.0
    }])
    df_saida = pd.concat([df_freq, linha_total], ignore_index=True)

    # salva arquivo de saída na pasta 'Grupos Vulneráveis' do ano
    output_path = os.path.join(grupos_dir, OUTPUT_FILENAME_TEMPLATE.format(ano))
    df_saida.to_csv(output_path, sep=";", index=False, encoding="utf-8-sig")
    print(f"[OK] {ano}: frequências salvas em {output_path} (total = {total_ano})")
    return total_ano

def gerar_frequencias_por_ano(base_dir=BASE_DIR, salvar_resumo_totais=True):
    anos = [d for d in sorted(os.listdir(base_dir)) if os.path.isdir(os.path.join(base_dir, d))]
    if not anos:
        print(f"[ERRO] Nenhuma pasta de ano encontrada em {base_dir}")
        return

    resumo_totais = []
    for ano in anos:
        ano_dir = os.path.join(base_dir, ano)
        try:
            total = processar_ano(ano_dir, ano)
            if total is not None:
                resumo_totais.append((ano, int(total)))
        except Exception as e:
            print(f"[ERRO] Falha ao processar {ano}: {e}")

    if salvar_resumo_totais and resumo_totais:
        df_resumo = pd.DataFrame(resumo_totais, columns=["Ano", "Total denúncias"])
        df_resumo = df_resumo.sort_values("Ano")
        caminho_resumo = os.path.join(base_dir, TOTALS_SUMMARY_NAME)
        df_resumo.to_csv(caminho_resumo, sep=";", index=False, encoding="utf-8-sig")
        print(f"[OK] Resumo de totais por ano salvo em: {caminho_resumo}")

if __name__ == "__main__":
    gerar_frequencias_por_ano()
