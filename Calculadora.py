import streamlit as st

# 1. CONFIGURAÇÃO DA PÁGINA
URL_LOGO = "https://raw.githubusercontent.com/Adatech-hub/calculadora-mkt/main/Logo.png"

st.set_page_config(
    page_title="Adatech Calc",
    page_icon=URL_LOGO,
    layout="centered"
)

# 2. CSS PERSONALIZADO (Contornos Verdes para Entradas e Textos)
st.markdown("""
    <style>
    /* Estilo para campos de texto (Preço e Estorno) */
    div[data-testid="stTextInput"] :focus {
        border-color: #28a745 !important;
        box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25) !important;
    }
    /* Estilo para campos numéricos específicos caso necessário */
    div[data-testid="stNumberInput"] :focus {
        border-color: #28a745 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. TOPO COM LOGO ADATECH
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
    st.image(URL_LOGO, width=80)
with col_titulo:
    st.title("Precificação de Anúncios")

st.markdown("Calcule sua lucratividade considerando promoções e a carga tributária do seu e-commerce.")

# 4. ENTRADA DE DADOS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Aquisição")
    # Custo de aquisição
    custo_produto_raw = st.text_input("Preço de Custo (R$)", value="50,00")
    try:
        custo_produto = float(custo_produto_raw.replace(',', '.'))
    except ValueError:
        custo_produto = 0.0
    st.caption("Quanto você pagou pelo produto ao fornecedor.")

with col2:
    st.subheader("💰 Dados da Venda")
    
    # Campo de Preço Original (Aceita vírgula e ponto perfeitamente)
    preco_original_raw = st.text_input("Preço Original (R$)", value="120,00")
    try:
        preco_original = float(preco_original_raw.replace(',', '.'))
    except ValueError:
        st.error("Por favor, digite um preço válido (ex: 52,06)")
        preco_original = 0.0

    porcentagem_desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    
    # Cálculo do preço real após desconto
    preco_final = preco_original * (1 - (porcentagem_desconto / 100))
    st.info(f"**Preço de Venda Real: R$ {preco_final:.2f}**")
    
    custo_frete = st.number_input("Custo de Frete (R$)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    comissao_mkt_porcentagem = st.number_input("Comissão Marketplace (%)", min_value=0.0, value=16.5, step=0.1)
    taxa_fixa_venda = st.number_input("Taxa Fixa por Venda (R$)", min_value=0.0, value=6.00, step=0.01, format="%.2f")
    
    # Campo de Estorno/Bonificação (Valor positivo que entra para a ADATECH)
    estorno_ml_raw = st.text_input("Estorno/Bonificação ML (R$)", value="0,00")
    try:
        estorno_ml = float(estorno_ml_raw.replace(',', '.'))
    except ValueError:
        estorno_ml = 0.0
    
    # Imposto configurado conforme sua necessidade (7,3%)
    imposto_porcentagem = st.number_input("Imposto sobre NF (%)", min_value=0.0, value=7.3, step=0.1)

# 5. LÓGICA DE CÁLCULO
valor_comissao = preco_final * (comissao_mkt_porcentagem / 100)
valor_imposto = preco_final * (imposto_porcentagem / 100)
custo_total_saidas = custo_produto + custo_frete + valor_comissao + valor_imposto + taxa_fixa_venda

# Lucro Líquido considerando a bonificação (Estorno)
lucro_liquido = (preco_final + estorno_ml) - custo_total_saidas
margem_contribuicao = (lucro_liquido / preco_final) * 100 if preco_final > 0 else 0

st.divider()

# 6. MÉTRICAS DE RESULTADO
m1, m2, m3 = st.columns(3)
m1.metric("Lucro Líquido", f"R$ {lucro_liquido:.2f}")
m2.metric("Margem", f"{margem_contribuicao:.2f}%")
m3.metric("Custo Total", f"R$ {custo_total_saidas:.2f}")

# Alertas Visuais de Rentabilidade
if margem_contribuicao < 15:
    st.error("⚠️ Margem baixa! Verifique o desconto ou os custos.")
elif 15 <= margem_contribuicao <= 25:
    st.warning("⚖️ Margem aceitável para giro.")
else:
    st.success("✅ Margem excelente para o seu produto!")

# 7. TABELA DETALHADA PARA CONFERÊNCIA
st.write("### Detalhamento Financeiro")
detalhes = {
    "Descrição": [
        "Venda com Desconto", 
        "Estorno/Bonificação (+)", 
        "Custo do Produto (-)", 
        "Comissão Canal (-)", 
        "Taxa Fixa (-)", 
        "Imposto (7,3%) (-)", 
        "Logística/Frete (-)"
    ],
    "Valor": [
        f"R$ {preco_final:.2f}", 
        f"R$ {estorno_ml:.2f}", 
        f"R$ {custo_produto:.2f}", 
        f"R$ {valor_comissao:.2f}", 
        f"R$ {taxa_fixa_venda:.2f}", 
        f"R$ {valor_imposto:.2f}", 
        f"R$ {custo_frete:.2f}"
    ]
}
st.table(detalhes)
