### ✔ Escolha e descrição do dataset

- Dataset meteorológico do INMET (estações Chapecó, São Miguel do Oeste e Dionísio Cerqueira).  
- Dados horários de 2024, com mais de 17.000 registros.  
- Atributos principais: temperatura, umidade, precipitação, radiação, vento, pressão, hora.  
- Descrição detalhada no notebook e no Data Card do Kaggle.

### ✔ Análise exploratória (EDA)

- Estatísticas descritivas (`describe`).  
- Histogramas de variáveis numéricas.  
- Mapas de correlação.  
- Análise de distribuição das faixas climáticas.

### ✔ Pré-processamento

- Remoção de cabeçalhos textuais do INMET.  
- Renomeação e padronização de colunas.  
- Conversão de vírgula para ponto em valores numéricos.  
- Tratamento de nulos e precipitação ausente.  
- Criação da variável alvo `faixa_climatica`.  
- Seleção de atributos relevantes para o modelo.  
- Normalização com `StandardScaler` no pipeline.

### ✔ Tipo de aprendizagem e algoritmo

- Aprendizagem **supervisionada**.  
- Algoritmo: **Random Forest Classifier**.

### ✔ Treinamento e avaliação

- Divisão treino/teste (70%/30%) com `train_test_split` e `stratify`.  
- Avaliação com:
  - Acurácia  
  - Precision  
  - Recall  
  - F1-score por classe  
- Interpretação dos resultados no notebook.

### ✔ Discussão de resultados e limitações

- Justificativa para a acurácia elevada (classes definidas a partir de temperatura e chuva).  
- Validação adicional com remoção de variáveis-chave (modelo sem `temp_c` e `precipitacao_mm`).  
- Comentários sobre importância das variáveis e coerência física.

### ✔ Notebook documentado

- Contém:
  - Identificação da dupla.  
  - Descrição do problema e dos dados.  
  - EDA, pré-processamento, modelagem, avaliação e conclusões.  
- Organizado em células com textos explicativos.

### ✔ Interface de teste do modelo (Streamlit)

- Permite inserir/ajustar valores de:
  - Temperatura  
  - Umidade  
  - Precipitação  
  - Radiação  
  - Vento  
  - Pressão  
  - Hora do dia  
- Exibe:
  - Faixa climática prevista.  
  - Probabilidade por classe.  
  - Acurácia e relatório de classificação.  
  - Importância das variáveis.  
- Contém uma breve explicação no topo do aplicativo.
s