# 🌤️ Clima INMET – Região Oeste de Santa Catarina (2024)

Este repositório contém o projeto da disciplina de **Ciência de Dados**, cujo objetivo é aplicar o processo completo de Ciência de Dados sobre um conjunto de dados **real** e **regional**, construindo também uma interface interativa para teste do modelo em **Streamlit**.

## 👥 Equipe

- Arthur Borger Kochem
- Bruno Gabriel Konzen

---

## 📦 Descrição do Projeto

O projeto utiliza dados meteorológicos horários do **INMET** (Instituto Nacional de Meteorologia) referentes ao ano de **2024** para três estações da região Oeste de Santa Catarina:

- Chapecó (A895)  
- São Miguel do Oeste (A857)  
- Dionísio Cerqueira (A848)  

A partir dessas medições (temperatura, umidade, precipitação, pressão, radiação, vento etc.), o objetivo é **classificar automaticamente faixas climáticas**, combinando:

- Temperatura: **Frio / Ameno / Quente**  
- Condição de chuva: **Seco / Chuvoso**

---

## 🗂 Estrutura do Repositório

```text
.
├── app.py                       # Aplicação Streamlit
├── clima_inmet_oeste_2024.csv   # Dataset tratado (dados de 2024 unificados)
├── requirements.txt             # Dependências do projeto
├── README.md                    # Este arquivo
└── INSTRUCOES_TRABALHO.md       


📊 Dataset


Fonte: INMET – Estações Automáticas (dados públicos)

Período: 01/01/2024 a 31/12/2024

Cobertura geográfica: Oeste de Santa Catarina (Chapecó, SMO, Dionísio Cerqueira)

Registros: ~17.000 observações horárias

Principais atributos:

temp_c – Temperatura do ar (°C)

umidade_pct – Umidade relativa do ar (%)

precipitacao_mm – Precipitação na última hora (mm)

radiacao_kj – Radiação global (kJ/m²)

vento_vel_ms – Velocidade do vento (m/s)

pressao_mb – Pressão atmosférica (mB)

hora – Hora do dia (0–23)

faixa_climatica – Classe alvo (Frio/Ameno/Quente + Seco/Chuvoso)

A coluna faixa_climatica é construída a partir de regras sobre temperatura e precipitação e é usada como alvo para o modelo de classificação.


## 🧠 Modelagem de Dados


Tipo de aprendizagem: Supervisionada – Classificação multiclasse

Algoritmo: RandomForestClassifier (scikit-learn)

Pipeline:

Normalização com StandardScaler

Classificação com RandomForestClassifier

Divisão treino/teste: 70% / 30% (train_test_split com stratify)

Métricas de avaliação:

Acurácia

Precision

Recall

F1-score (por classe)
O modelo atinge acurácia próxima de 100%, o que é esperado, pois as classes foram definidas diretamente a partir de variáveis de entrada (temperatura e precipitação). Isso significa que o modelo aprende corretamente a regra de classificação proposta.

Além disso, é feita uma validação adicional treinando um segundo modelo sem temperatura e precipitação, mostrando a queda de desempenho e reforçando a importância dessas variáveis para a definição da faixa climática.


## 🌐 Aplicação Streamlit


O arquivo app.py implementa uma interface gráfica para:

Visualizar o desempenho do modelo (acurácia e relatório de classificação);

Comparar o modelo completo com um modelo reduzido (sem temp/chuva);

Fazer previsão interativa, ajustando:

Temperatura

Umidade

Precipitação

Radiação

Velocidade do vento

Pressão atmosférica

Hora do dia

Visualizar a distribuição de probabilidades entre as classes;

Visualizar a importância das variáveis (feature importance da Random Forest).


## ▶️ Como executar localmente


1. Clonar o repositório
git clone https://github.com/brunogkonzen/ClimaINMETSC

2. Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate     # Windows

3. Instalar dependências
pip install -r requirements.txt

4. Rodar o Streamlit
streamlit run app.py


## 🔗 Links importantes


Notebook com o experimento completo:
https://www.kaggle.com/code/brunokonzen/dataset-clima-inmet

Dataset no Kaggle:
https://www.kaggle.com/datasets/brunokonzen/clima-inmet-sc-regio-oeste-2024/data

Aplicação publicada no Streamlit Cloud:
https://climainmetsc.streamlit.app/


## 📌 Licença


Este projeto utiliza dados públicos do INMET. O código pode ser reutilizado para fins acadêmicos, desde que citada a fonte original.
