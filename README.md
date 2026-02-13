# Dashboard-denuncias-direitos-humanos-registrados no-disque100


Este repositório contém a aplicação em Streamlit desenvolvida para uma análise experimental de denúncias registradas no Disque 100 (2020 - 2024), com foco em grupos vulneráveis.
O objetivo da aplicação é facilitar a visualização, comparação e exploração interativa de padrões de denúncias a partir de dados públicos tratados.

## Funcionalidades

- Dashboard anual e histórico com dados de denúncias
  
- Exploração assistida com IA (Gemini) para geração de insigths, com base na interpretação dos dados apresentados no dashboard

- Visualização de categorias de violência por grupo vulnerável

- Exploração interativa dos dados para análise e comparação

## Estrutura dos Dados

- Fonte: Disque 100 (Ouvidoria Nacional de Direitos Humanos).

- Período: 2020 a 2024.

- Organização: dados separados por grupo vulnerável em múltiplos CSVs.

- Obs: Os dados disponibilizados foram tratados e normalizados para atender ao foco desta pesquisa.
Para acesso aos dados originais, visite: [dados.gov.br](https://dados.gov.br/dados/conjuntos-dados/ouvidoria-nacional-de-direitos-humanos--ondh) . 

## Execução Local

### Dependências
  - dask==2025.2.0
  - google-generativeai==0.8.4
  - pandas==2.2.3
  - plotly==5.24.1
  - streamlit==1.47.1

### Instalação 

     git clone https://github.com/seu-usuario/Dashboard-denuncias-direitos-humanos-disque100.git
     cd Dashboard-denuncias-direitos-humanos-disque100
     pip install -r requirements.txt
     
### Execução Local

     streamlit run "Streamlit\app.py"
     
##  Demonstração


<img width="1366" height="768" alt="Captura de tela 2025-10-20 143324" src="https://github.com/user-attachments/assets/8037e47c-2ab9-4614-a886-749a8f25c835" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 143758" src="https://github.com/user-attachments/assets/7459adf1-3bfc-4ded-8ef4-fba566918965" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 143402" src="https://github.com/user-attachments/assets/59c9aaf9-b417-4924-8b75-d29922ac23a1" />

<img width="1358" height="450" alt="Captura de tela 2025-10-20 150059" src="https://github.com/user-attachments/assets/21bfce2c-6a8e-474b-ac0b-403529590656" />

<img width="1363" height="546" alt="Captura de tela 2025-10-20 150132" src="https://github.com/user-attachments/assets/9ceaa350-54ee-4e48-9d56-c545fc938ff2" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150044" src="https://github.com/user-attachments/assets/6035e627-ff4a-47ac-b2d3-6f6fdb119202" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150211" src="https://github.com/user-attachments/assets/26165a81-704d-404a-9c40-db86e10f2aaa" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150225" src="https://github.com/user-attachments/assets/6a78d497-d85f-48f8-aae3-f5f54ac03a0f" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150247" src="https://github.com/user-attachments/assets/192a61d9-b665-43fc-bf22-d22625e2817a" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150305" src="https://github.com/user-attachments/assets/4c76f299-42f7-4a7f-8616-ab3ba7cce495" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150333" src="https://github.com/user-attachments/assets/14f541f1-ae18-4928-ae95-581ae36fd29f" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150535" src="https://github.com/user-attachments/assets/4658d6e7-5c26-487d-9594-92827f5e9a3e" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150626" src="https://github.com/user-attachments/assets/cd37cab8-cde7-4b8c-ae9f-b2f7dde4db65" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150640" src="https://github.com/user-attachments/assets/afbc2aaf-3b72-4638-922b-98ec88ac2b3b" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 150714" src="https://github.com/user-attachments/assets/e1490138-e559-4959-b9a7-8c2ec8af1416" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 151034" src="https://github.com/user-attachments/assets/d0b75291-f5ad-420e-94af-e83f05f936ac" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 151132" src="https://github.com/user-attachments/assets/593970df-31db-4103-aea6-47f37717c0ea" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 151147" src="https://github.com/user-attachments/assets/3ed4c4e8-54fd-4790-9d68-198427d12ace" />

<img width="1366" height="768" alt="Captura de tela 2025-10-20 151158" src="https://github.com/user-attachments/assets/5eed80c7-ccb5-4629-9a20-deadbc065717" />
