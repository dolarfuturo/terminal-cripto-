import streamlit as st
import pandas as pd
import time
import ccxt
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

# CSS ESTILO TERMINAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    .title-gold { color: #D4AF37; font-size: 35px; font-weight: 700; text-align: center; text-shadow: 0px 0px 10px rgba(212,175,55,0.5); }
    .header-container { display: flex; align-items: center; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .col-head { font-size: 9px; flex: 1; text-align: center; font-weight: 800; color: #BBB; text-transform: uppercase; }
    .row-container { display: flex; align-items: center; padding: 6px 0; border-bottom: 1px solid #111; }
    .col-ativo { color: #EEE; font-size: 12px; flex: 1.2; font-weight: 700; padding-left: 10px; }
    .col-price { color: #FF8C00; font-weight: 800; font-size: 13px; flex: 1.5; text-align: center; }
    .status-box { padding: 4px; border-radius: 4px; font-weight: 800; font-size: 9px; width: 90%; margin: auto; text-align: center; color: white; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-exaustao { background-color: #FF0000; animation: blinker 0.6s linear infinite; } 
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# Inicializa exchange com timeout longo
@st.cache_resource
def get_exchange():
    return ccxt.binance({'timeout': 30000, 'enableRateLimit': True})

ex = get_exchange()

st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
placeholder = st.empty()

while True:
    try:
        # Puxa tickers de forma otimizada
        tickers = ex.fetch_tickers()
        data = [t for t in tickers.values() if t['symbol'].endswith('/USDT')]
        top_data = sorted(data, key=lambda x: x['quoteVolume'], reverse=True)[:50]
        
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="col-head" style="flex:1.2;">ATIVO</div>
                    <div class="col-head" style="flex:1.5;">PREÇO (VAR%)</div>
                    <div class="col-head" style="color:#FFFF00;">PONTO DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX TOPO</div>
                    <div class="col-head" style="color:#FF0000;">TETO EXAUSTÃO</div>
                    <div class="col-head" style="color:#FFFF00;">SUPORTE DECISÃO</div>
                    <div class="col-head" style="color:#FFA500;">PRÓX FUNDO</div>
                    <div class="col-head" style="color:#00FF00;">CHÃO EXAUSTÃO</div>
                    <div class="col-head">SINAL</div>
                </div>
                """, unsafe_allow_html=True)

            for t in top_data:
                price = t['last']
                change = t['percentage']
                vwap = t['vwap'] if t['vwap'] else price
                seta = '▲' if price >= vwap else '▼'
                color_seta = "#00FF00" if price >= vwap else "#FF0000"
                color_var = "#00FF00" if change >= 0 else "#FF0000"
                prec = 6 if price < 1 else 2
                
                v4, v8, v10 = price*1.04, price*1.08, price*1.10
                c4, c8, c10 = price*0.96, price*0.92, price*0.90
                
                s_txt = "ESTÁVEL"; s_class = "bg-estavel"
                if abs(change) >= 10: s_txt = "EXAUSTÃO"; s_class = "bg-exaustao"

                st.markdown(f"""
                    <div class="row-container">
                        <div class="col-ativo">{t['symbol']}</div>
                        <div class="col-price">
                            {price:.{prec}f}<span style="color:{color_seta};">{seta}</span> 
                            <span style="color:{color_var}; font-size:9px;">({change:+.2f}%)</span>
                        </div>
                        <div style="flex:1; text-align:center; color:#FFFF00; font-size:11px;">{v4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500; font-size:11px;">{v8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FF0000; font-size:11px;">{v10:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFFF00; font-size:11px;">{c4:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#FFA500; font-size:11px;">{c8:.{prec}f}</div>
                        <div style="flex:1; text-align:center; color:#00FF00; font-size:11px;">{c10:.{prec}f}</div>
                        <div style="flex:1;"><div class="status-box {s_class}">{s_txt}</div></div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(10) # Frequência maior para evitar bloqueio de IP
    except Exception as e:
        st.write("Tentando restabelecer conexão...")
        time.sleep(15)
