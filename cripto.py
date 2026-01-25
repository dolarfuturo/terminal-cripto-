import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuração de Página e Estilo "Visão de Tubarão"
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    .title { color: #D4AF37; text-align: center; font-family: 'serif'; font-weight: bold; }
    .subtitle { color: #FFFFFF; text-align: center; letter-spacing: 5px; font-size: 14px; }
    th { color: #D4AF37 !important; background-color: #111 !important; }
    td { color: #FFFFFF !important; font-family: 'monospace'; }
    .stMetric { background-color: #0a0a0a; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>ALPHA VISION CRYPTO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>VISÃO DE TUBARÃO</p>", unsafe_allow_html=True)

# Lista de Ativos do Terminal
ativos = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD"]

# Eixo Mestre (Referência da sua Imagem 2)
EIXO = 89795.0 

def get_data():
    lista_final = []
    for ticker in ativos:
        try:
            # Puxa dados do Yahoo Finance
            data = yf.Ticker(ticker).fast_info
            preco = data['last_price']
            
            # Cálculos de Alvos (Baseados no EIXO para BTC, ou Preço para os outros)
            # Para manter o seu setup, usamos o EIXO fixo no BTC
            ref = EIXO if ticker == "BTC-USD" else preco
            
            def calc(p): return ref * (1 + (p/100))
            
            lista_final.append({
                "ATIVO": ticker.replace("-USD", "/USDT"),
                "PREÇO ATUAL": f"{preco:,.2f}",
                "1.22% EXAUSTÃO": f"{calc(1.22):,.2f}",
                "0.83% TOPO": f"{calc(0.83):,.2f}",
                "0.61% PARCIAL": f"{calc(0.61):,.2f}",
                "0.40% RESPIRO": f"{calc(0.40):,.2f}",
                "SINALIZADOR": "ESTÁVEL"
            })
        except:
            continue
    return pd.DataFrame(lista_final)

# Exibição da Tabela "Tubarão"
df = get_data()
st.table(df)

# Footer com relógio para confirmar tempo real
st.markdown(f"<p style='color:#333; text-align:center;'>Sincronizado: {time.strftime('%H:%M:%S')} - Reset VWAP 00:00 UTC</p>", unsafe_allow_html=True)

# Motor de atualização (A cada 5 segundos para não travar o Yahoo)
time.sleep(5)
st.rerun()
