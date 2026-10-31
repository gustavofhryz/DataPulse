
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


import requests
import pandas as pd
import streamlit as st


# ==========================================
# CONFIGURAÇÕES
# ==========================================

API_URL = "http://127.0.0.1:8000"

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
def get_api_data():
    sales_response = requests.get(
        f"{API_URL}/sales",
        params={"limit": 500, "offset": 0},
        timeout=10,
    )
    sales_response.raise_for_status()

    summary_response = requests.get(
        f"{API_URL}/analytics/summary",
        timeout=10,
    )
    summary_response.raise_for_status()

    products_response = requests.get(
        f"{API_URL}/analytics/products",
        timeout=10,
    )
    products_response.raise_for_status()

    return (
        sales_response.json(),
        summary_response.json(),
        products_response.json(),
    )


try:
    sales_data, summary_data, products_data = get_api_data()

except requests.RequestException as error:
    st.error(
        "Não foi possível conectar à API DataPulse. "
        "Verifique se o servidor FastAPI está funcionando."
    )
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

df["data"] = pd.to_datetime(df["data"], errors="coerce")
df["faturamento"] = pd.to_numeric(
    df["faturamento"], errors="coerce"
)
df["quantidade"] = pd.to_numeric(
    df["quantidade"], errors="coerce"
)

df = df.dropna(
    subset=["data", "faturamento", "quantidade"]
)


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

if st.sidebar.button("🔄 Atualizar dados"):
    get_api_data.clear()
    st.rerun()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = df[
        (df["data"].dt.date >= start_date)
        & (df["data"].dt.date <= end_date)
    ].copy()
else:
    filtered_df = df.copy()


# ==========================================
# INDICADORES PRINCIPAIS
# ==========================================

total_sales = len(filtered_df)

total_revenue = filtered_df["faturamento"].sum()

average_ticket = (
    total_revenue / total_sales
    if total_sales > 0
    else 0
)

total_units = filtered_df["quantidade"].sum()

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

with left:
    st.markdown("#### Faturamento por produto")

    product_chart = (
        filtered_df.groupby("produto")["faturamento"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(product_chart)

with right:
    st.markdown("#### Evolução das vendas")

    daily_chart = (
        filtered_df.groupby(
            filtered_df["data"].dt.date
        )["faturamento"]
        .sum()
    )

    st.line_chart(daily_chart)


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
        .sort_values("faturamento", ascending=False)
    )

    product_table["faturamento"] = (
        product_table["faturamento"].round(2)
    )

    st.dataframe(
        product_table,
        use_container_width=True,
        hide_index=True,
    )


# ==========================================
# HISTÓRICO DE VENDAS
# ==========================================

st.divider()

st.markdown("### Histórico de vendas")

st.dataframe(
    filtered_df.sort_values(
        "data", ascending=False
    ),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "DataPulse | Dados consultados pela API FastAPI "
    "e armazenados no SQLite."
)

