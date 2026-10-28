
import streamlit as st

st.set_page_config(
    page_title="DataPulse",
    page_icon="📊",
    layout="wide",
)

st.title("DataPulse")
st.subheader("Plataforma de análise de dados")

st.info(
    "Ambiente inicial configurado. "
    "A integração com dados reais será implementada nas próximas etapas."
)

col1, col2, col3 = st.columns(3)

col1.metric("Registros processados", "—")
col2.metric("Faturamento", "—")
col3.metric("Ticket médio", "—")

st.markdown(
    """
    ### Próximas funcionalidades

    - Importação de arquivos CSV
    - Validação e limpeza de dados
    - Armazenamento em banco SQL
    - Indicadores e gráficos interativos
    """
)
