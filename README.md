# Dashboard-denuncias-direitos-humanos-registrados no-disque100


Este repositório contém a aplicação em Streamlit desenvolvida para apoiar o artigo científico:
“Dashboards e Inteligência Artificial na Proteção de Grupos Vulneráveis: Análise de Dados do Disque 100”.

  O objetivo é disponibilizar painéis interativos que permitem explorar os dados de denúncias registradas no Disque 100, com foco em grupos vulneráveis.

Embora o artigo tenha como ênfase principal o grupo dos idosos, a aplicação vai além e possibilita análises para diversos grupos, nos anos de 2020 a 2024.

## Funcionalidades

-Dashboard anual e histórico com dados de denúncias.

-Visualização de categorias de violência por grupo vulnerável.

-Foco em exploração interativa dos dados, facilitando análises e comparações.

## Estrutura dos Dados

- Fonte: Disque 100 (Ouvidoria Nacional de Direitos Humanos).

-Período: 2020 a 2024.

-Organização: dados separados por grupo vulnerável em múltiplos CSVs.

-Obs: Os dados disponibilizados foram tratados e normalizados para atender ao foco desta pesquisa.
Para acessar os dados originais, visite: [dados.gov.br](https://dados.gov.br/dados/conjuntos-dados/ouvidoria-nacional-de-direitos-humanos--ondh) . 

## Execução Local

- dask==2025.2.0
- google-generativeai==0.8.4
- pandas==2.2.3
- plotly==5.24.1
- streamlit==1.47.1

## Instalação 

     git clone https://github.com/seu-usuario/Dashboard-denuncias-direitos-humanos-disque100.git
     cd Dashboard-denuncias-direitos-humanos-disque100
     pip install -r requirements.txt
     
## Execução Local

     streamlit run "Streamlit\app.py"
     
##  Demonstração



<img width="1366" height="768" alt="Captura de tela 2025-10-20 143324" src="https://github.com/user-attachments/assets/8037e47c-2ab9-4614-a886-749a8f25c835" />

    
