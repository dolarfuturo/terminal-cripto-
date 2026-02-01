import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - VISUAL REFINADO
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")
COINS_CONFIG = {
    "BTC-USD":  {"label": "BTC/USDT",  "fb": 82000, "dec": 0},
    "ETH-USD":  {"label": "ETH/USDT",  "fb": 2400,  "dec": 0},
    "SOL-USD":  {"label": "SOL/USDT",  "fb": 160,   "dec": 2},
    "BNB-USD":  {"label": "BNB/USDT",  "fb": 600,   "dec": 2},
    "XRP-USD":  {"label": "XRP/USDT",  "fb": 2.50,  "dec": 4},
    "DOGE-USD": {"label": "DOGE/USDT", "fb": 0.35,  "dec": 4}
}
# --- COPIE DAQUI ---
def get_midpoint_v13(ticker, fallback):
    try:
        import yfinance as yf
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if not data.empty:
            return float(data['Close'].iloc[0])
        return float(fallback)
    except:
        return float(fallback)

for ticker in COINS_CONFIG:
    if f'mp_{ticker}' not in st.session_state:
        val = get_midpoint_v13(ticker, COINS_CONFIG[ticker]['fb'])
        st.session_state[f'mp_{ticker}'] = val
        st.session_state[f'rv_{ticker}'] = val
# --- ATÉ AQUI ---

 

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    
    /* Ajuste Preciso do Subtítulo (H até Y) */
    .subtitle-white { 
        color: #FFFFFF; 
        font-size: 16px; 
        font-weight: 300; 
        letter-spacing: 5.5px; /* Calibrado para largura média H-Y */
        margin-top: 2px;
        text-transform: lowercase;
    }
            /* Configuração das Colunas Principais */
        .header-container, .row-container {
            display: grid;
            grid-template-columns: 1.5fr 1.2fr 1fr 1fr 1fr 1fr 1fr 1fr;
            width: 100%;
            padding: 10px 0;
            border-bottom: 1px solid #222;
            align-items: center;
            text-align: center;
        }
        .h-col { font-size: 10px; color: #888; font-weight: bold; text-transform: uppercase; }
        .w-col { font-size: 18px; font-weight: bold; color: #FFF; }

        /* ESTE BLOCO CENTRALIZA O RESET E ÂNCORA */
        .vision-block {
            display: flex;
            justify-content: center; /* Centraliza horizontalmente */
            gap: 80px;               /* Espaço entre Reset e Âncora */
            width: 100%;             /* Ocupa a largura total da tela */
            padding: 5px 0 20px 0;
            margin-top: -10px;       /* Traz para mais perto da linha de cima */
            border-bottom: 2px solid #111;
        }
        .v-item { 
            display: flex; 
            flex-direction: column; 
            align-items: center;     /* Centraliza o texto interno */
        }
        .v-label { font-size: 9px; color: #666; font-weight: bold; margin-bottom: 2px; }
        .v-val { font-size: 14px; font-weight: 900; }

                        padding: 5px 0 15px 0;
            margin-top: -10px;
            border-bottom: 2px solid #111;
        }
        .v-item { display: flex; flex-direction: column; align-items: center; }
        .v-label { font-size: 9px; color: #555; font-weight: bold; }
        .v-val { font-size: 13px; font-weight: bold; }

    
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO
def get_midpoint_v13():
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        if now_br.weekday() >= 5 or (now_br.weekday() == 0 and now_br.hour < 18):
            return 82632
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download("BTC-USD", start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        df.index = df.index.tz_convert(br_tz)
        df_window = df.between_time('11:30', '18:00')
        if not df_window.empty:
            return int((float(df_window['High'].max()) + float(df_window['Low'].min())) / 2)
        return 82632
    except:
        return 82632

# 3. INTERFACE REAL-TIME
st.markdown("""
    <div class="title-container">
        <div class="title-gold">ALPHA VISION CRYPTO</div>
        <div class="subtitle-white">visão de tubarão</div>
    </div>
    """, unsafe_allow_html=True)

if 'mp_current' not in st.session_state:
     valor_base = get_midpoint_v13()
     st.session_state.mp_current = valor_base
     st.session_state.rv_fixed = valor_base


placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br, now_ny, now_lon = datetime.now(br_tz), datetime.now(ny_tz), datetime.now(lon_tz)
        
        # Auto-Reset Binance (18:00 BR)
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
           novo_valor = get_midpoint_v13()
           st.session_state.mp_current = novo_valor
           st.session_state.rv_fixed = novo_valor
           st.rerun()

        ticker = yf.Ticker("BTC-USD")
        price = ticker.fast_info['last_price']
        mp = st.session_state.mp_current
        var = ((price / mp) - 1) * 100
                    # --- LÓGICA DE ESCADA: GATILHO 1.35% | MOVIMENTO 1.22% ---
        if var >= 1.35:
            st.session_state.mp_current = int(mp * 1.0122)
             
            
        elif var <= -1.35:
            st.session_state.mp_current = int(mp * 0.9878)
            

        cor_var = "#00FF00" if var >= 0 else "#FF0000"
        seta = "▲" if var >= 0 else "▼"
        
        with placeholder.container():
                   st.markdown("""
            <div class="header-container">
                <div class="h-col">CÓDIGO</div><div class="h-col">PREÇO ATUAL</div>
                <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
            </div>
        """, unsafe_allow_html=True)
        for ticker, info in COINS_CONFIG.items():
            # Coleta de dados individual
            price = yf.Ticker(ticker).fast_info['last_price']
            mp = st.session_state[f'mp_{ticker}']
            rv = st.session_state[f'rv_{ticker}']
            # 1. Cálculo da Variação para a Escada
            var_escada = ((price / mp) - 1) * 100
            if var_escada >= 1.35:
                st.session_state[f'mp_{ticker}'] = mp * 1.0122
            elif var_escada <= -1.35:
                st.session_state[f'mp_{ticker}'] = mp * 0.9878
            
            # 2. Lógica dos Alarmes (PISCAR)
            abs_var = abs(var_escada)
            fundo_decisao = "background: rgba(255, 255, 0, 0.3);" if 0.59 <= abs_var <= 0.65 else ""
            estilo_ex_t = 'color: #FF4444; animation: blink 0.4s infinite;' if 1.20 <= abs_var <= 1.35 else "color: #FF4444;"
            estilo_ex_f = 'color: #00FF00; animation: blink 0.4s infinite;' if -1.35 <= var_escada <= -1.20 else "color: #00FF00;"
            
            # 3. Variação do ResetVision
            var_reset = ((price / rv) - 1) * 100
            cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")
            # HTML da Linha de Dados (Repete para cada moeda)
            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="color: #FFFFFF;">{info['label']}</div>
                    <div class="w-col" style="color: #FFFFFF; {fundo_decisao}">{f"{price:,.{info['dec']}f}"}</div>
                    <div class="w-col" style="{estilo_ex_t}">{f"{(mp * 1.0135):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #FFFFFF;">{f"{(mp * 1.0122):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #FFFF00;">{f"{(mp * 1.0062):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #FFFFFF;">{f"{(mp * 0.9938):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #FFFFFF;">{f"{(mp * 0.9878):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="{estilo_ex_f}">{f"{(mp * 0.9865):,.{info['dec']}f}"}</div>
                </div>
                
                <div class="vision-block">
                    <div class="v-item">
                        <span class="v-label">RESETVISION</span>
                        <span class="v-val" style="color: {cor_v};">{seta_v} {var_reset:.2f}%</span>
                    </div>
                    <div class="v-item">
                        <span class="v-label">ÂNCORAVISION</span>
                        <span class="v-val" style="color: #00FFFF;">{f"{mp:,.{info['dec']}f}"}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        # RODAPÉ (COLE FORA DO LOOP FOR - ALINHADO COM O FOR)
        st.markdown(f"""
            <div class="footer-container">
                <div class="footer-item">
                    <div class="f-label">LONDRES</div>
                    <div class="f-time">{(datetime.now() + timedelta(hours=3)).strftime('%H:%M')}</div>
                </div>
                <div class="footer-item">
                    <div class="f-label">NEW YORK</div>
                    <div class="f-time">{(datetime.now() - timedelta(hours=2)).strftime('%H:%M')}</div>
                </div>
                <div class="footer-item">
                    <div class="f-label">SÃO PAULO</div>
                    <div class="f-time">{datetime.now().strftime('%H:%M')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1) # Delay de atualização
      
    except Exception as e:
        st.error(f"Erro na atualização: {e}")
   
            
