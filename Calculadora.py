import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA (Ícone da aba e título do navegador)
URL_LOGO = "https://raw.githubusercontent.com/Adatech-hub/calculadora-mkt/main/Up%20logo.png"

st.set_page_config(
    page_title="Calculadora ADATECH",
    page_icon=URL_LOGO,
    layout="centered"
)

# 2. TOPO PERSONALIZADO COM A SUA LOGO
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    st.image(URL_LOGO, width=80)

with col_titulo:
    st.title("Precificação de Anúncios")

st.markdown("Calcule sua lucratividade considerando promoções e a carga tributária da sua loja Online.")

# 3. BARRA LATERAL (CONFIGURAÇÕES FIXAS)
with st.sidebar:
    st.header("Configurações Fixas")
    taxa_fixa_venda = st.number_input("Taxa Fixa por Venda (R$)", value=0.00, step=0.50)
    st.info("Altere se houver taxa fixa por item (ex: R$ 6,00 no ML).")

# 4. ENTRADA DE DADOS (COLUNAS PRINCIPAIS)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Aquisição")
    custo_produto = st.number_input("Preço de Custo (R$)", min_value=0.0, value=50.0, step=1.0)
    st.caption("Quanto você pagou pelo produto ao fornecedor.")

with col2:
    st.subheader("💰 Dados da Venda")
    preco_original = st.number_input("Preço Original (R$)", min_value=0.0, value=120.0, step=1.0)
    porcentagem_desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
    
    # Cálculo imediato do preço com desconto
    preco_final = preco_original * (1 - (porcentagem_desconto / 100))
    st.info(f"**Preço de Venda Real: R$ {preco_final:.2f}**")
    
    custo_frete = st.number_input("Custo de Frete (R$)", min_value=0.0, value=0.0, step=1.0)
    comissao_mkt_porcentagem = st.number_input("Comissão Marketplace (%)", min_value=0.0, value=16.5, step=0.1)
    imposto_porcentagem = st.number_input("Imposto sobre NF (%)", min_value=0.0, value=7.3, step=0.1)

# 5. LÓGICA DE CÁLCULO FINANCEIRO
valor_comissao = preco_final * (comissao_mkt_porcentagem / 100)
valor_imposto = preco_final * (imposto_porcentagem / 100)

# Custo total operacional
custo_total = custo_produto + custo_frete + valor_comissao + valor_imposto + taxa_fixa_venda

# Resultados Finais
lucro_liquido = preco_final - custo_total
margem_contribuicao = (lucro_liquido / preco_final) * 100 if preco_final > 0 else 0

st.divider()

# 6. EXIBIÇÃO DOS RESULTADOS (MÉTRICAS)
m1, m2, m3 = st.columns(3)
m1.metric("Lucro Líquido", f"R$ {lucro_liquido:.2f}")
m2.metric("Margem", f"{margem_contribuicao:.2f}%")
m3.metric("Custo Total", f"R$ {custo_total:.2f}")

# Alertas de Margem
if margem_contribuicao < 15:
    st.error("⚠️ Margem baixa! Verifique o desconto ou os custos.")
elif 15 <= margem_contribuicao <= 25:
    st.warning("⚖️ Margem aceitável para giro.")
else:
    st.success("✅ Margem excelente para a ADATECH!")

# 7. TABELA DETALHADA
st.write("### Detalhamento de Saídas")
detalhes = {
    "Descrição": ["Recebimento Real", "Custo do Produto", "Comissão Canal", "Imposto (7,3%)", "Logística + Taxas"],
    "Valor": [
        f"R$ {preco_final:.2f}",
        f"R$ {custo_produto:.2f}", 
        f"R$ {valor_comissao:.2f}", 
        f"R$ {valor_imposto:.2f}", 
        f"R$ {custo_frete + taxa_fixa_venda:.2f}"
    ]
}
st.table(detalhes)
