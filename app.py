
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# =====================================================
# CONFIGURAÇÕES BÁSICAS
# =====================================================

st.set_page_config(
    page_title="Clima INMET Oeste SC 2024",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ Classificação de Faixa Climática – Oeste de SC (INMET 2024)")
st.write(
    """
    Este aplicativo utiliza dados horários do INMET da região Oeste de Santa Catarina (estações de Chapecó, 
    São Miguel do Oeste e Dionísio Cerqueira) para **classificar a faixa climática** de acordo com:

    - Temperatura (Frio / Ameno / Quente)  
    - Condição de chuva (Seco / Chuvoso)

    O modelo foi treinado com **Random Forest** usando variáveis meteorológicas reais.
    """
)

# =====================================================
# CARREGAR DADOS
# =====================================================

DATA_PATH = "clima_inmet_oeste_2024.csv"


@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho)
    return df


try:
    df = carregar_dados(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"Arquivo `{DATA_PATH}` não encontrado.\n\n"
        "Coloque o CSV tratado na mesma pasta do `app.py` ou ajuste o caminho na variável DATA_PATH."
    )
    st.stop()

st.sidebar.header("📁 Dados")
st.sidebar.success(f"Dataset carregado com {df.shape[0]:,} linhas e {df.shape[1]} colunas.")

# Mostra um pedacinho dos dados (opcional)
with st.expander("👀 Ver amostra dos dados tratados"):
    st.dataframe(df.head())

# =====================================================
# PREPARAR DADOS PARA O MODELO
# =====================================================

# Colunas usadas como features (as mesmas do notebook, sem cidade)
FEATURES = [
    "temp_c",
    "umidade_pct",
    "precipitacao_mm",
    "radiacao_kj",
    "vento_vel_ms",
    "pressao_mb",
    "hora"
]

TARGET = "faixa_climatica"

# Versão reduzida das features, sem temperatura e precipitação,
# para usar como "validação alternativa"
FEATURES_REDUZIDAS = [
    "umidade_pct",
    "radiacao_kj",
    "vento_vel_ms",
    "pressao_mb",
    "hora"
]

# Garante que não haja NaN nas features/target
df_model = df[FEATURES + [TARGET]].dropna().copy()

X = df_model[FEATURES]
y = df_model[TARGET]


# =====================================================
# TREINAR MODELO (PIPELINE: SCALER + RANDOM FOREST)
# =====================================================

@st.cache_resource
def treinar_modelo(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    # Pipeline: normalização + RandomForest
    modelo = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        ))
    ])

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    relatorio = classification_report(y_test, y_pred, output_dict=True)

    return modelo, acc, relatorio


@st.cache_resource
def treinar_modelo_com_features(df_model, feature_list):
    X = df_model[feature_list]
    y = df_model[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    modelo = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        ))
    ])

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    return acc


modelo, acc, relatorio = treinar_modelo(X, y)

# =====================================================
# ABA 1: RESUMO DO MODELO
# =====================================================

aba_resumo, aba_pred, aba_importancias = st.tabs(
    ["📊 Desempenho do Modelo", "🤖 Previsão Interativa", "📈 Importância das Variáveis"]
)

with aba_resumo:
    st.subheader("📊 Desempenho do Modelo Random Forest")

    st.write(f"**Acurácia no conjunto de teste:** `{acc:.3f}`")

    # Transformar classification_report em tabela
    relatorio_df = pd.DataFrame(relatorio).transpose()
    st.dataframe(relatorio_df.style.format({"precision": "{:.3f}", "recall": "{:.3f}", "f1-score": "{:.3f}"}))

    st.markdown(
        """
        **Interpretação rápida:**
        - A acurácia indica a proporção de horas corretamente classificadas em sua faixa climática.
        - As métricas por classe mostram como o modelo se comporta para cada categoria 
          (ex.: *Ameno Seco*, *Quente Chuvoso* etc.).
        """
    )

    st.markdown("---")
    st.subheader("🧪 Validação adicional: modelo sem temperatura e precipitação")

    acc_reduzido = treinar_modelo_com_features(df_model, FEATURES_REDUZIDAS)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Acurácia modelo completo", f"{acc:.3f}")
    with col2:
        st.metric("Acurácia sem temp/chuva", f"{acc_reduzido:.3f}")

    st.markdown(
        """
        Aqui comparamos dois modelos:

        - **Modelo completo**: usa temperatura, umidade, precipitação, radiação, vento, pressão e hora.
        - **Modelo reduzido**: *não* usa temperatura nem precipitação.

        A queda de desempenho no modelo reduzido mostra que **temperatura** e **chuva** são
        variáveis fundamentais para definir a faixa climática, o que reforça a coerência física do modelo.
        """
    )


# =====================================================
# ABA 2: PREVISÃO INTERATIVA
# =====================================================

with aba_pred:
    st.subheader("🤖 Previsão Interativa de Faixa Climática")

    st.write("Ajuste os controles na barra lateral e clique em **Prever** para ver a classificação do modelo.")

    # SIDEBAR – ENTRADA DO USUÁRIO
    st.sidebar.header("🔧 Parâmetros para previsão")


    def slider_num(col, label, step=0.1):
        minimo = float(df_model[col].min())
        maximo = float(df_model[col].max())
        medio = float(df_model[col].median())
        return st.sidebar.slider(
            label,
            min_value=minimo,
            max_value=maximo,
            value=medio,
            step=step
        )


    temp_user = slider_num("temp_c", "Temperatura (°C)", step=0.1)
    umidade_user = slider_num("umidade_pct", "Umidade relativa (%)", step=1.0)
    chuva_user = slider_num("precipitacao_mm", "Precipitação na última hora (mm)", step=0.1)
    radiacao_user = slider_num("radiacao_kj", "Radiação global (kJ/m²)", step=1.0)
    vento_user = slider_num("vento_vel_ms", "Velocidade do vento (m/s)", step=0.1)
    pressao_user = slider_num("pressao_mb", "Pressão atmosférica (mB)", step=0.1)

    hora_user = st.sidebar.slider(
        "Hora do dia (0–23)",
        min_value=0,
        max_value=23,
        value=12,
        step=1
    )

    if st.button("🔮 Prever faixa climática"):
        # Montar DataFrame com uma única linha
        entrada = pd.DataFrame([{
            "temp_c": temp_user,
            "umidade_pct": umidade_user,
            "precipitacao_mm": chuva_user,
            "radiacao_kj": radiacao_user,
            "vento_vel_ms": vento_user,
            "pressao_mb": pressao_user,
            "hora": hora_user
        }])

        predicao = modelo.predict(entrada)[0]
        probs = modelo.predict_proba(entrada)[0]
        classes = modelo.named_steps["rf"].classes_

        st.success(f"🌡️ **Faixa climática prevista:** `{predicao}`")

        # Mostrar probabilidades por classe
        prob_df = pd.DataFrame({
            "faixa_climatica": classes,
            "probabilidade": probs
        }).sort_values("probabilidade", ascending=False)

        st.write("Distribuição de probabilidade entre as classes:")
        st.bar_chart(prob_df.set_index("faixa_climatica"))

        st.markdown(
            """
            > **Obs.:** A previsão é feita com base em um modelo treinado sobre os dados horários de 2024. 
            > Pequenas variações de temperatura, umidade e chuva podem alterar a faixa climática prevista.
            """
        )

# =====================================================
# ABA 3: IMPORTÂNCIA DAS VARIÁVEIS
# =====================================================

with aba_importancias:
    st.subheader("📈 Importância das Variáveis no Modelo")

    # Extrair importâncias do RandomForest dentro do pipeline
    rf_model = modelo.named_steps["rf"]
    importancias = pd.DataFrame({
        "variavel": FEATURES,
        "importancia": rf_model.feature_importances_
    }).sort_values("importancia", ascending=False)

    st.write("As variáveis mais importantes para a decisão do modelo são:")
    st.dataframe(importancias)

    st.bar_chart(importancias.set_index("variavel"))
    st.markdown(
        """
        Em geral, espera-se que **temperatura**, **umidade** e **radiação solar** sejam as variáveis mais relevantes 
        para definir as faixas de *Frio/Ameno/Quente* e as condições de *Seco/Chuvoso*, o que está alinhado com 
        a interpretação física do clima.
        """
    )
