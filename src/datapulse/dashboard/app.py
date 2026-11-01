
import os

import pandas as pd
import requests
import streamlit as st


# ==========================================
# CONFIGURAÇÕES
# ==========================================

def _get_api_url() -> str:
    """
    Obtém a URL da API nesta ordem:
    1. Variável de ambiente
    2. Streamlit Secrets
    3. API publicada no Render
    """

    url = os.getenv("DATAPULSE_API_URL")

    if not url:
        try:
            url = st.secrets.get("DATAPULSE_API_URL")
        except Exception:
            url = None

    if not url:
        url = "https://datapulse-api-omhv.onrender.com"

    return url.rstrip("/")


API_URL = _get_api_url()


st.set_page_config(
    page_title="DataPulse | Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# ESTILO VISUAL
# ==========================================

st.title("📊 DataPulse")

st.subheader("Plataforma de análise de dados")

st.markdown(
    """
    Acompanhe indicadores de vendas, faturamento
    e desempenho dos produtos em tempo real.
    """
)

st.divider()


# ==========================================
# CONEXÃO COM A API
# ==========================================

@st.cache_data(ttl=30)
def get_sales_data(start_date=None, end_date=None, product=None):
    """
    Consulta vendas na API FastAPI.
    Permite filtros por período e produto.
    """

    params = {
        "limit": 500,
        "offset": 0,
    }

    if start_date:
        params["start_date"] = start_date

    if end_date:
        params["end_date"] = end_date

    if product:
        params["product"] = product

    response = requests.get(
        f"{API_URL}/sales",
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ==========================================
# CARREGAMENTO INICIAL
# ==========================================

try:
    sales_data = get_sales_data()

except requests.RequestException as error:
    st.error(
        "Não foi possível conectar à API DataPulse. "
        "Verifique a disponibilidade do servidor."
    )

    st.caption(f"API configurada: {API_URL}")
    st.code(str(error))

    st.stop()


# ==========================================
# PREPARAÇÃO DOS DADOS
# ==========================================

df = pd.DataFrame(sales_data)

if df.empty:
    st.warning(
        "Nenhuma venda encontrada no banco de dados. "
        "Execute o pipeline e importe os dados."
    )
    st.stop()


df["data"] = pd.to_datetime(
    df["data"],
    errors="coerce",
)

df["faturamento"] = pd.to_numeric(
    df["faturamento"],
    errors="coerce",
)

df["quantidade"] = pd.to_numeric(
    df["quantidade"],
    errors="coerce",
)

df = df.dropna(
    subset=["data", "faturamento", "quantidade"]
)

if df.empty:
    st.warning("Não existem vendas com dados válidos.")
    st.stop()


# ==========================================
# FILTROS
# ==========================================

st.sidebar.header("🔎 Filtros")

min_date = df["data"].min().date()
max_date = df["data"].max().date()


date_range = st.sidebar.date_input(
    "Período das vendas",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)


products = sorted(
    df["produto"].dropna().unique().tolist()
)


selected_product = st.sidebar.selectbox(
    "Produto",
    options=["Todos"] + products,
)


if st.sidebar.button("🔄 Atualizar dados"):
    get_sales_data.clear()
    st.rerun()


# ==========================================
# CONSULTA FILTRADA À API
# ==========================================

start_date = None
end_date = None

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:

    start_date = date_range[0].isoformat()
    end_date = date_range[1].isoformat()


product_filter = (
    selected_product
    if selected_product != "Todos"
    else None
)


try:
    filtered_sales = get_sales_data(
        start_date=start_date,
        end_date=end_date,
        product=product_filter,
    )

except requests.RequestException as error:

    st.error(
        "Erro ao consultar os filtros na API DataPulse."
    )

    st.code(str(error))

    st.stop()


# ==========================================
# PREPARAÇÃO DOS DADOS FILTRADOS
# ==========================================

filtered_df = pd.DataFrame(filtered_sales)


if not filtered_df.empty:

    filtered_df["data"] = pd.to_datetime(
        filtered_df["data"],
        errors="coerce",
    )

    filtered_df["faturamento"] = pd.to_numeric(
        filtered_df["faturamento"],
        errors="coerce",
    )

    filtered_df["quantidade"] = pd.to_numeric(
        filtered_df["quantidade"],
        errors="coerce",
    )

    filtered_df = filtered_df.dropna(
        subset=["data", "faturamento", "quantidade"]
    )


# ==========================================
# INDICADORES PRINCIPAIS
# ==========================================

total_sales = len(filtered_df)

total_revenue = (
    filtered_df["faturamento"].sum()
    if not filtered_df.empty
    else 0
)

average_ticket = (
    total_revenue / total_sales
    if total_sales > 0
    else 0
)

total_units = (
    filtered_df["quantidade"].sum()
    if not filtered_df.empty
    else 0
)


st.markdown("### Indicadores de desempenho")

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Faturamento",
    f"R$ {total_revenue:,.2f}",
)

col2.metric(
    "Vendas",
    f"{total_sales:,}",
)

col3.metric(
    "Ticket médio",
    f"R$ {average_ticket:,.2f}",
)

col4.metric(
    "Unidades vendidas",
    f"{total_units:,.0f}",
)


st.divider()


# ==========================================
# GRÁFICOS
# ==========================================

st.markdown("### Análise de faturamento")

left, right = st.columns(2)


# FATURAMENTO POR PRODUTO

with left:

    st.markdown("#### Faturamento por produto")

    if not filtered_df.empty:

        product_chart = (
            filtered_df.groupby("produto")["faturamento"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(product_chart)

    else:

        st.info(
            "Nenhuma venda encontrada para os filtros selecionados."
        )


# EVOLUÇÃO DAS VENDAS

with right:

    st.markdown("#### Evolução das vendas")

    if not filtered_df.empty:

        daily_chart = (
            filtered_df.groupby(
                filtered_df["data"].dt.date
            )["faturamento"]
            .sum()
        )

        st.line_chart(daily_chart)

    else:

        st.info(
            "Não há dados para exibir no período selecionado."
        )


# ==========================================
# DESEMPENHO DOS PRODUTOS
# ==========================================

st.divider()

st.markdown("### Desempenho dos produtos")


if not filtered_df.empty:

    product_table = (
        filtered_df.groupby("produto")
        .agg(
            quantidade_vendas=("id_venda", "count"),
            unidades_vendidas=("quantidade", "sum"),
            faturamento=("faturamento", "sum"),
        )
        .reset_index()
        .sort_values(
            "faturamento",
            ascending=False,
        )
    )

    product_table["faturamento"] = (
        product_table["faturamento"].round(2)
    )

    st.dataframe(
        product_table,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info("Nenhum produto encontrado.")


# ==========================================
# HISTÓRICO DE VENDAS
# ==========================================

st.divider()

st.markdown("### Histórico de vendas")


if not filtered_df.empty:

    st.dataframe(
        filtered_df.sort_values(
            "data",
            ascending=False,
        ),
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "Nenhuma venda encontrada para os filtros selecionados."
    )


# ==========================================
# RODAPÉ
# ==========================================

st.caption(
    "DataPulse | Dados consultados pela API FastAPI "
    "e armazenados no banco Neon PostgreSQL."
)
