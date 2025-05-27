import pandas as pd 
from collections import Counter

def Maiores_Ocorrências_por_valor(yearData,  releventCategories, selected_category ):

    print("Entrou em maiores_ocorrencias_por_valor_com_counter")
    data_por_grupo = {}

    try:

        for semestre, semestre_data in yearData.items():

            if semestre in ['primeiro_semestre', 'segundo_semestre']:

                for row in semestre_data:

                    grupo = row.get(selected_category, '').upper()

                    if grupo:

                        if grupo not in data_por_grupo:

                            data_por_grupo[grupo] = []

                        relevant_data = {k: row.get(k) for k in releventCategories}
                        data_por_grupo[grupo].append(relevant_data)

        processed_data = {}

        for grupo, lista_de_dados in data_por_grupo.items():

            frequencias_por_categoria = {}

            for categoria in releventCategories:

                valores = [
                    item.get(categoria) 
                    for item in lista_de_dados 
                    if item.get(categoria) is not None and item.get(categoria).upper() != "N/D"]
                
                if valores:

                    contador = Counter(valores)
                    valor_mais_frequente = contador.most_common(1)[0][0]
                    frequencias_por_categoria[categoria] = valor_mais_frequente
                
                else:
                    frequencias_por_categoria[categoria] = None
            
            processed_data[grupo] = frequencias_por_categoria

        all_rows = []
        
        for grupo, frequencias in processed_data.items():
            
            row = {selected_category: grupo}
            row.update(frequencias)
            all_rows.append(row)

        df = pd.DataFrame(all_rows)
        
        #print(f"DataFrame final (head):\n{df.head().to_string() if df is not None else None}")
        
        return df

    except Exception as e:
       
        print(f'Erro ao adquirir os dados para a tabela em maiores_ocorrencias_por_valor_com_counter: {e}')
       
        return pd.DataFrame()