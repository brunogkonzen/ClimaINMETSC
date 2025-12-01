## 🌤️ Clima INMET – Região Oeste de Santa Catarina (2024)

Este repositório contém o projeto da disciplina de Ciência de Dados, cujo objetivo é aplicar o processo completo de Ciência de Dados sobre um conjunto de dados real e regional, além de desenvolver uma interface interativa para teste do modelo em Streamlit.

## 👥 Equipe

Arthur Borger Kochem

Bruno Gabriel Konzen

## 📦 Descrição do Projeto

O projeto utiliza dados meteorológicos horários do INMET (Instituto Nacional de Meteorologia) referentes ao ano de 2024, para três estações da região Oeste de Santa Catarina:

Chapecó (A895)

São Miguel do Oeste – SMO (A857)

Dionísio Cerqueira (A848)

A partir dessas medições (temperatura, umidade, precipitação, pressão, radiação, vento etc.), o objetivo é classificar automaticamente faixas climáticas combinando:

Temperatura → Frio / Ameno / Quente

Condição de chuva → Seco / Chuvoso

## 🗂 Estrutura do Repositório
.
├── app.py                       # Aplicação Streamlit
├── clima_inmet_oeste_2024.csv   # Dataset tratado (dados de 2024 unificados)
├── requirements.txt             # Dependências do projeto
├── README.md                    # Este arquivo
└── INSTRUCOES_TRABALHO.md       # Especificações da atividade

## 📊 Dataset

Fonte: INMET – Estações Automáticas (dados públicos)
Período: 01/01/2024 a 31/12/2024
Cobertura geográfica: Oeste de Santa Catarina (Chapecó, SMO, Dionísio Cerqueira)
Registros: ~17.000 observações horárias

Principais atributos

temp_c – Temperatura do ar (°C)

umidade_pct – Umidade relativa do ar (%)

precipitacao_mm – Precipitação na última hora (mm)

radiacao_kj – Radiação global (kJ/m²)

vento_vel_ms – Velocidade do vento (m/s)

pressao_mb – Pressão atmosférica (mB)

hora – Hora do dia (0–23)

faixa_climatica – Classe alvo (Frio/Ameno/Quente + Seco/Chuvoso)

A coluna faixa_climatica foi construída a partir de regras sobre temperatura e precipitação e é utilizada como alvo para o modelo de classificação.

## 🧠 Modelagem de Dados
Tipo de aprendizagem:

Supervisionada – Classificação multiclasse

Algoritmo:

RandomForestClassifier (scikit-learn)

Pipeline

Normalização com StandardScaler

Modelo RandomForestClassifier

Divisão dos dados

70% treino / 30% teste

train_test_split com stratify para manter proporção das classes

Métricas

Acurácia

Precision

Recall

F1-score (por classe)

O modelo atinge acurácia próxima de 100%, o que é esperado porque as classes foram definidas diretamente a partir das variáveis de entrada (regras climáticas).
Isso demonstra que o modelo aprende corretamente a lógica de classificação proposta.

Também foi treinado um modelo reduzido sem temperatura e precipitação, mostrando uma queda na acurácia — reforçando a importância dessas variáveis na definição da faixa climática.

## 🌐 Aplicação Streamlit

O arquivo app.py implementa uma interface gráfica que permite:

✔ Visualizar desempenho do modelo

Acurácia

Relatório de classificação

✔ Comparar modelos

Modelo completo

Modelo reduzido (sem temp/chuva)

✔ Fazer previsão interativa

O usuário ajusta:

Temperatura

Umidade

Precipitação

Radiação

Vento

Pressão

Hora

E o app retorna:

A faixa climática prevista

A probabilidade para cada classe

Um gráfico de barras

✔ Mostrar importância das variáveis

Feature importance do Random Forest

## ▶️ Como executar localmente
1. Clonar o repositório
git clone https://github.com/brunogkonzen/ClimaINMETSC

2. Criar ambiente virtual (opcional, recomendado)
python -m venv venv
venv\Scripts\activate   # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Rodar o Streamlit
streamlit run app.py

## 🔗 Links importantes

📘 Notebook (experimento completo):
https://www.kaggle.com/code/brunokonzen/dataset-clima-inmet

📂 Dataset no Kaggle:
https://www.kaggle.com/datasets/brunokonzen/clima-inmet-sc-regio-oeste-2024/data

🌐 Aplicação Streamlit publicada:
https://climainmetsc.streamlit.app/

## S📌 Licença

Este projeto utiliza dados públicos do INMET.
O código pode ser reutilizado para fins acadêmicos, desde que a fonte seja citada.