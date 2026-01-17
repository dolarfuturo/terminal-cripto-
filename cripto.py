import streamlit as st
import pandas as pd
import time
import yfinance as yf

# 1. CONFIGURAÇÃO DE INTERFACE
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;900&display=swap');
    
    .block-container { padding: 0.5rem !important; }
    .stApp { background-color: #000000; font-family: 'JetBrains Mono', monospace; }
    
    /* CABEÇALHO PRINCIPAL ALPHA VISION */
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; text-align: center; margin-bottom: 0px; text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.5); }
    .subtitle-vision { color: #C0C0C0; font-size: 16px; text-align: center; margin-top: -5px; letter-spacing: 7px; margin-bottom: 20px; font-weight: 700; }
    
    /* CABEÇALHO DAS COLUNAS */
    .header-container { display: flex; width: 100%; padding: 10px 0; border-bottom: 2px solid #D4AF37; background-color: #080808; position: sticky; top: 0; z-index: 99; }
    .h-col { font-size: 9px; font-weight: 800; color: #BBB; text-transform: uppercase; text-align: center; }
    
    /* LINHAS ALINHADAS */
    .row-container { display: flex; width: 100%; align-items: center; padding: 6px 0; border-bottom: 1px solid #151515; gap: 0px; }
    
    /* LARGURAS E FONTES AJUSTADAS */
    .w-ativo { width: 14%; text-align: left; padding-left: 10px; color: #EEE; font-size: 14px; font-weight: 700; }
    .w-price { width: 12%; text-align: center; color: #FF8C00; font-size: 15px; font-weight: 900; }
    .w-target { width: 10%; text-align: center; font-size: 14px; font-weight: 800; }
    .w-sinal { width: 14%; text-align: center; padding-right: 5px; }

    /* ESTILOS DE ALVO ATIVO */
    .t-active { border-radius: 2px; padding: 2px 4px; }
    .t-y { background-color: #FFFF00; color: #000 !important; }
    .t-o { background-color: #FFA500; color: #000 !important; }
    .t-r { background-color: #FF0000; color: #FFF !important; animation: blinker 0.4s linear infinite; }
    .t-g { background-color: #00FF00; color: #000 !important; animation: blinker 0.4s linear infinite; }
    
    @keyframes blinker { 50% { opacity: 0.2; } }

    .status-box { padding: 8px 2px; border-radius: 2px; font-weight: 900; font-size: 9px; width: 100%; text-align: center; text-transform: uppercase; }
    .bg-estavel { background-color: #00CED1; color: #000; } 
    .bg-yellow { background-color: #FFFF00; color: #000; }
    .bg-orange { background-color: #FFA500; color: #000; }
    .bg-ex-red { background-color: #FF0000; color: #FFF; animation: blinker 0.4s linear infinite; }
    .bg-ex-green { background-color: #00FF00; color: #000; animation: blinker 0.4s linear infinite; }
    </style>
    """, unsafe_allow_html=True)

assets = {
    'BTC-USD':'BTC/USDT','ETH-USD':'ETH/USDT','SOL-USD':'SOL/USDT','BNB-USD':'BNB/USDT','XRP-USD':'XRP/USDT',
    'DOGE-USD':'DOGE/USDT','ADA-USD':'ADA/USDT','AVAX-USD':'AVAX/USDT','DOT-USD':'DOT/USDT','LINK-USD':'LINK/USDT',
    'NEAR-USD':'NEAR/USDT','PEPE-USD':'PEPE/USDT','EGLD-USD':'EGLD/USDT','GALA-USD':'GALA/USDT','FET-USD':'FET/USDT'
}

# TÍTULOS DE COMANDO
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-vision">VISÃO DE TUBARÃO</div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        tickers = yf.Tickers(' '.join(assets.keys()))
        with placeholder.container():
            st.markdown("""
                <div class="header-container">
                    <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">ATIVO</div>
                    <div class="h-col" style="width:12%;">PREÇO ATUAL</div>
                    <div class="h-col" style="width:10%; color:#FFFF00;">RESISTÊNCIA</div>
                    <div class="h-col" style="width:10%; color:#FFA500;">PRÓX AO TOPO</div>
                    <div class="h-col" style="width:10%; color:#FF0000;">TETO EXAUSTÃO</div>
                    <div class="h-col" style="width:10%; color:#FFFF00;">SUPORTE</div>
                    <div class="h-col" style="width:10%; color:#FFA500;">PRÓX FUNDO</div>
                    <div class="h-col" style="width:10%; color:#00FF00;">CHÃO EXAUSTÃO</div>
                    <div class="h-col" style="width:14%;">SINALIZADOR</div>
                </div>
                """, unsafe_allow_html=True)

            for tid, name in assets.items():
                try:
                    info = tickers.tickers[tid].fast_info
                    price = info.last_price
                    open_p = info.open
                    if price is None: continue
                    
                    change = ((price - open_p) / open_p) * 100
                    v4, v8, v10 = open_p*1.04, open_p*1.08, open_p*1.10
                    c4, c8, c10 = open_p*0.96, open_p*0.92, open_p*0.90
                    
                    s_txt, s_class = "ESTÁVEL", "bg-estavel"
                    v4_c, v8_c, v10_c, c4_c, c8_c, c10_c = "", "", "", "", "", ""

                    if price >= v10: s_txt, s_class, v10_c = "EXAUSTÃO", "bg-ex-red", "t-active t-r"
                    elif price >= v8: s_txt, s_class, v8_c = "CUIDADO ALTA VOL", "bg-orange", "t-active t-o"
                    elif price >= v4: s_txt, s_class, v4_c = "PONTO DECISAO ATENÇÃO", "bg-yellow", "t-active t-y"
                    elif price <= c10: s_txt, s_class, c10_c = "EXAUSTÃO", "bg-ex-green", "t-active t-g"
                    elif price <= c8: s_txt, s_class, c8_c = "CUIDADO ALTA VOL", "bg-orange", "t-active t-o"
                    elif price <= c4: s_txt, s_class, c4_c = "PONTO DECISAO ATENÇÃO", "bg-yellow", "t-active t-y"

                    prec = 6 if price < 0.1 else (4 if price < 10 else 2)
                    seta = '▲' if price >= open_p else '▼'
                    seta_c = '#00FF00' if price >= open_p else '#FF0000'

                    st.markdown(f"""
                        <div class="row-container">
                            <div class="w-ativo">{name}</div>
                            <div class="w-price">{price:.{prec}f}<br><span style="font-size:9px; color:{seta_c};">{seta}{change:+.2f}%</span></div>
                            <div class="w-target" style="color:#FFFF00;"><span class="{v4_c}">{v4:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FFA500;"><span class="{v8_c}">{v8:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FF0000;"><span class="{v10_c}">{v10:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FFFF00;"><span class="{c4_c}">{c4:.{prec}f}</span></div>
                            <div class="w-target" style="color:#FFA500;"><span class="{c8_c}">{c8:.{prec}f}</span></div>
                            <div class="w-target" style="color:#00FF00;"><span class="{c10_c}">{c10:.{prec}f}</span></div>
                            <div class="w-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                        </div>
                    """, unsafe_allow_html=True)
                except: continue
        time.sleep(10)
    except: time.sleep(10)
