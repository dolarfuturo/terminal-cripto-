import streamlit as st
import pandas as pd
from datetime import time

st.title("Alpha Vision - Eixo Institucional")

# Simulando a entrada de dados (No seu terminal, aqui entra a API da Exchange)
# Vamos usar o valor que você validou no gráfico
preco_atual = 89235.0  # Conforme seu print
eixo_referencia = 89790.0 # Eixo de Quinta/Sexta que você achou

def calcular_alvos(eixo):
    return {
        "Alvo Final (1.22%)": eixo * 1.0122,
        "Aviso Topo (0.80%)": eixo * 1.008,
        "Parcial (0.61%)": eixo * 1.0061,
        "Respiro (0.40%)": eixo * 1.004,
        "EIXO MESTRE": eixo,
        "Respiro Baixa (-0.40%)": eixo * 0.996,
        "Parcial Baixa (-0.61%)": eixo * 0.9939,
        "Alvo Final Baixa (-1.22%)": eixo * 0.9878
    }

alvos = calcular_alvos(eixo_referencia)

# Exibição no Terminal para o Cliente
st.subheader(f"Eixo Travado: ${eixo_referencia:,.2f}")

col1, col2 = st.columns(2)

with col1:
    st.success("🎯 ALVOS DE ALTA")
    st.write(f"Final (1.22%): **${alvos['Alvo Final (1.22%)']:,.2f}**")
    st.write(f"Aviso Topo (0.8%): ${alvos['Aviso Topo (0.80%)']:,.2f}")
    st.write(f"Respiro (0.4%): ${alvos['Respiro (0.40%)']:,.2f}")

with col2:
    st.error("📉 ALVOS DE BAIXA")
    st.write(f"Final (-1.22%): **${alvos['Alvo Final Baixa (-1.22%)']:,.2f}**")
    st.write(f"Aviso Topo (-0.8%): ${alvos['Alerta de Topo (0.80%) (Venda)']:,.2f}" if 'Alerta de Topo (0.80%) (Venda)' in alvos else "")
    st.write(f"Respiro (-0.4%): ${alvos['Respiro Baixa (-0.40%)']:,.2f}")

st.divider()
st.info("O Eixo é calculado diariamente entre 11:30 e 18:00 (Brasília).")
