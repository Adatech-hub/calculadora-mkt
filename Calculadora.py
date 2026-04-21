import streamlit as st

# Configuração da página
st.set_page_config(page_title="Simulador de Margem - ADATECH", layout="centered")

st.title("📊 Simulador de Custos e Margem")
st.markdown("Calcule sua lucratividade considerando promoções e a carga tributária da ADATECH.")

# Sidebar com custo fixo padrão em 0
with st.sidebar:
    st.header("Configurações Fixas")
    taxa_fixa_venda = st.number_input("Taxa Fixa por Venda (R$)", value=0.00, step=0.50)
    st.info("Altere este valor se houver taxa fixa por item vendido (Ex: R$ 6,00 no ML).")

# Layout principal
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Aquisição")
    custo_produto = st.number_input("Preço de Custo (R$)", min_value=0.0, value=50.0, step=1.0)
    st.caption("Quanto você pagou pelo produto ao fornecedor.")

with col2:
    st.subheader("💰 Dados da Venda")
    preco_original = st.number_input("Preço Original (R$)", min_value=0.0, value=120.0, step=1.0)
    porcentagem_desconto = st.number_input("Desconto (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
    
    # Cálculo do preço final após desconto
    preco_final = preco_original * (1 - (porcentagem_desconto / 100))
    
    # Exibição do preço final em destaque
    st.info(f"**Preço de Venda Real: R$ {preco_final:.2f}**")
    
    custo_frete = st.number_input("Custo de Frete (R$)", min_value=0.0, value=0.0, step=1.0)
    comissao_mkt_porcentagem = st.number_input("Comissão Marketplace (%)", min_value=0.0, value=16.5, step=0.1)
    
    # Novo padrão de imposto solicitado: 7.3%
    imposto_porcentagem = st.number_input("Imposto sobre NF (%)", min_value=0.0, value=7.3, step=0.1)

# --- LÓGICA DE CÁLCULO BASEADA NO PREÇO FINAL ---
valor_comissao = preco_final * (comissao_mkt_porcentagem / 100)
valor_imposto = preco_final * (imposto_porcentagem / 100)

# Custo total (Aquisição + Saídas baseadas no preço de venda real)
custo_total = custo_produto + custo_frete + valor_comissao + valor_imposto + taxa_fixa_venda

# Resultados Finais
lucro_liquido = preco_final - custo_total
margem_contribuicao = (lucro_liquido / preco_final) * 100 if preco_final > 0 else 0

st.divider()

# --- PAINEL DE RESULTADOS ---
m1, m2, m3 = st.columns(3)

m1.metric("Lucro Líquido", f"R$ {lucro_liquido:.2f}")
m2.metric("Margem de Contribuição", f"{margem_contribuicao:.2f}%")
m3.metric("Custo Total Operacional", f"R$ {custo_total:.2f}")

# Feedback Visual para tomada de decisão
if margem_contribuicao < 15:
    st.error("⚠️ Margem baixa! O desconto ou o imposto de 7,3% estão comprimindo o lucro.")
elif 15 <= margem_contribuicao <= 25:
    st.warning("⚖️ Margem dentro da média de mercado para marketplaces.")
else:
    st.success("✅ Margem excelente para a ADATECH!")

# Tabela Detalhada
st.write("### Resumo de Fluxo (Deduções)")
detalhes = {
    "Item": ["Recebimento Real", "Custo do Produto (CMV)", "Comissão Canal", "Imposto (7,3%)", "Logística + Taxas"],
    "Valor": [
        f"R$ {preco_final:.2f}",
        f"R$ {custo_produto:.2f}", 
        f"R$ {valor_comissao:.2f}", 
        f"R$ {valor_imposto:.2f}", 
        f"R$ {custo_frete + taxa_fixa_venda:.2f}"
    ]
}
st.table(detalhes)