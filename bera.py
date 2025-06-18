import streamlit as st
import pandas as pd
import plotly.express as px

# --- Preço atual ---
preco_bera = 1.95
preco_eth = 2524.36

# --- Dados das coleções ---
colecoes = [
    {
        "Coleção": "Bong Bears", "NFTs na Coleção": 101, "BERA Garantido": 14531,
        "Custo em BERA": 1294.5436, "Custo em USD": 2524.36, "Retorno em USD": 28335.45
    },
    {
        "Coleção": "Bond Bears", "NFTs na Coleção": 126, "BERA Garantido": 11865,
        "Custo em BERA": 1294.5436, "Custo em USD": 2524.36, "Retorno em USD": 23136.75
    },
    {
        "Coleção": "Band Bears", "NFTs na Coleção": 1160, "BERA Garantido": 2264,
        "Custo em BERA": 381, "Custo em USD": 742.95, "Retorno em USD": 4414.8
    },
    {
        "Coleção": "Bit Bears", "NFTs na Coleção": 2279, "BERA Garantido": 1689,
        "Custo em BERA": 304, "Custo em USD": 592.8, "Retorno em USD": 3293.55
    },
    {
        "Coleção": "Baby Bears", "NFTs na Coleção": 569, "BERA Garantido": 3479,
        "Custo em BERA": 675, "Custo em USD": 1316.25, "Retorno em USD": 6784.05
    },
    {
        "Coleção": "Boo Bears", "NFTs na Coleção": 271, "BERA Garantido": 6102,
        "Custo em BERA": 1216, "Custo em USD": 2371.2, "Retorno em USD": 11898.9
    },
]

# --- Cálculos adicionais ---
for c in colecoes:
    c["Retorno %"] = round((c["Retorno em USD"] / c["Custo em USD"] - 1) * 100, 4)
    c["Preço por Token"] = round(c["Custo em USD"] / c["BERA Garantido"], 4)

df = pd.DataFrame(colecoes)

# --- Layout ---
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>🐻 Berachain NFT ROI Calculator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### 💰 Preço do <b>BERA</b> : <span style='color:#facc15;'>**${preco_bera:.2f}**</span>", unsafe_allow_html=True)
with col2:
    st.markdown(f"### 💎 Preço do ETH: <span style='color:#38bdf8;'>${preco_eth:,.2f}</span>", unsafe_allow_html=True)

# --- Tabela principal ---
st.dataframe(df, use_container_width=True)

# --- Simulação ---
st.sidebar.markdown("## 📈 Simulação de Investimento")
valor = st.sidebar.number_input("Valor para investir (USD)", min_value=100.0, value=3500.0, step=50.0)
colecao_sel = st.sidebar.selectbox("Coleção para simulação", df["Coleção"].tolist())

row = df[df["Coleção"] == colecao_sel].iloc[0]
qtd_nfts = valor / row["Custo em USD"]
retorno_estimado = qtd_nfts * row["Retorno em USD"]
roi_estimado = (retorno_estimado / valor - 1) * 100

st.sidebar.markdown("### 💡 Melhor Estratégia")
st.sidebar.write(f"**Coleção:** {colecao_sel}")
st.sidebar.write(f"**Qtd. NFTs:** {qtd_nfts:.2f}")
st.sidebar.write(f"**Investido:** ${valor:,.2f}")
st.sidebar.write(f"**Retorno:** ${retorno_estimado:,.2f}")
st.sidebar.write(f"**ROI:** {roi_estimado:.2f}%")

# --- Gráfico de ROI (sem Bong Bears) ---
st.markdown("### 📊 ROI por Coleção")
df_grafico = df[df["Coleção"] != "Bong Bears"].copy()
fig = px.bar(
    df_grafico.sort_values(by="Retorno %", ascending=False),
    x="Retorno %",
    y="Coleção",
    orientation="h",
    text="Retorno %",
    color="Coleção",
    color_discrete_sequence=px.colors.sequential.Plasma
)
fig.update_layout(height=450)
st.plotly_chart(fig, use_container_width=True)
