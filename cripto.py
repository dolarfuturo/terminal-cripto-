import streamlit as st
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta
import pytz

# 1. SETUP ALPHA - MANTIDO ORIGINAL
st.set_page_config(page_title="ALPHA VISION LIVE", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .title-container { text-align: center; padding: 15px; }
    .title-gold { color: #D4AF37; font-size: 34px; font-weight: 900; letter-spacing: 2px; margin-bottom: 0px; }
    .subtitle-white { color: #FFFFFF; font-size: 16px; font-weight: 300; letter-spacing: 5.5px; margin-top: 2px; text-transform: lowercase; }
    .header-container { display: flex; width: 100%; padding: 12px 0; border-bottom: 2px solid #D4AF37; background: #080808; justify-content: space-between; margin-top: 30px; }
    .h-col { font-size: 10px; color: #FFF; text-transform: uppercase; text-align: center; font-weight: 800; flex: 1; }
    .row-container { display: flex; width: 100%; align-items: center; padding: 25px 0; border-bottom: 1px solid #151515; justify-content: space-between; }
    .w-col { flex: 1; text-align: center; font-family: 'monospace'; font-size: 22px; font-weight: 800; color: #FFF; white-space: nowrap; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; color: #FFF; text-align: center; padding: 15px; font-size: 13px; border-top: 1px solid #333; display: flex; justify-content: center; align-items: center; gap: 35px; z-index: 1000; }
    .dot { height: 10px; width: 10px; background-color: #00FF00; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 12px #00FF00; animation: blink 1.2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE CÁLCULO - ADAPTADO PARA MÚLTIPLOS ATIVOS
def get_midpoint_v13(symbol):
    try:
        br_tz = pytz.timezone('America/Sao_Paulo')
        now_br = datetime.now(br_tz)
        # Reset automático conforme sua regra (18:00 BRT / 00:00 UTC Binance)
        target_date = now_br if now_br.hour >= 18 else now_br - timedelta(days=1)
        df = yf.download(symbol, start=target_date.strftime('%Y-%m-%d'), interval="1m", progress=False)
        if not df.empty:
            return int((float(df['High'].max()) + float(df['Low'].min())) / 2)
        return 82632 # Fallback original
    except:
        return 82632

# Configurações de ativos: [ExaustãoT, PróxTopo, Decisão, Respiro, PróxFundo, ExaustãoF]
# BTC/ETH: 1.22%, 0.83%, 0.61%, 0.40%... | ALTS: 12%, 6%, 4%...
ativos_config = {
    "BTC-USD": {"alvos": [1.0122, 1.0083, 1.0061, 1.0040, 0.9939, 0.9878], "escada": 1.0122, "gatilho": 1.35},
    "ETH-USD": {"alvos": [1.0122, 1.0083, 1.0061, 1.0040, 0.9939, 0.9878], "escada": 1.0122, "gatilho": 1.35},
    "BNB-USD": {"alvos": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88], "escada": 1.12, "gatilho": 13.0},
    "SOL-USD": {"alvos": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88], "escada": 1.12, "gatilho": 13.0},
    "XRP-USD": {"alvos": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88], "escada": 1.12, "gatilho": 13.0},
    "DOGE-USD": {"alvos": [1.12, 1.06, 1.04, 1.02, 0.96, 0.88], "escada": 1.12, "gatilho": 13.0}
}

# Inicialização do Estado (Sessão)
if 'ativos_data' not in st.session_state:
    st.session_state.ativos_data = {}
    for symbol in ativos_config:
        valor_base = get_midpoint_v13(symbol)
        st.session_state.ativos_data[symbol] = {'mp_current': valor_base, 'rv_fixed': valor_base}

# 3. INTERFACE REAL-TIME
st.markdown('<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>', unsafe_allow_html=True)

placeholder = st.empty()

while True:
    try:
        br_tz, ny_tz, lon_tz = pytz.timezone('America/Sao_Paulo'), pytz.timezone('America/New_York'), pytz.timezone('Europe/London')
        now_br, now_ny, now_lon = datetime.now(br_tz), datetime.now(ny_tz), datetime.now(lon_tz)
        
        # Auto-Reset Binance (18:00 BR) para todos os ativos
        if now_br.hour == 18 and now_br.minute == 0 and now_br.second < 2:
           for symbol in ativos_config:
               novo_valor = get_midpoint_v13(symbol)
               st.session_state.ativos_data[symbol]['mp_current'] = novo_valor
               st.session_state.ativos_data[symbol]['rv_fixed'] = novo_valor
           st.rerun()

        with placeholder.container():
            for symbol, config in ativos_config.items():
                ticker = yf.Ticker(symbol)
                price = ticker.fast_info['last_price']
                
                mp = st.session_state.ativos_data[symbol]['mp_current']
                rv_valor = st.session_state.ativos_data[symbol]['rv_fixed']
                
                var = ((price / mp) - 1) * 100
                
                # LÓGICA DE ESCADA ORIGINAL
                if var >= config['gatilho']:
                    st.session_state.ativos_data[symbol]['mp_current'] = int(mp * config['escada'])
                elif var <= -config['gatilho']:
                    st.session_state.ativos_data[symbol]['mp_current'] = int(mp * (2 - config['escada']))

                # Variação ResetVision (Preço vs Fixo 24h)
                var_reset = ((price / rv_valor) - 1) * 100
                cor_v = "#00FF00" if var_reset >= 0 else "#FF4444"
                seta_v = "▲" if var_reset >= 0 else "▼"
                
                # Alvos e Estilos Dinâmicos
                abs_var = abs(var)
                fundo_decisao = "background: rgba(255, 255, 0, 0.3);" if 0.59 <= abs_var <= 0.65 else ""
                
                # Alerta de Exaustão (Animação Blink)
                estilo_ex_t = "color: #FF4444; animation: blink 0.4s infinite;" if (var >= (config['gatilho']-0.15)) else "color: #FF4444;"
                estilo_ex_f = "color: #00FF00; animation: blink 0.4s infinite;" if (var <= -(config['gatilho']-0.15)) else "color: #00FF00;"

                st.markdown(f"""
                    <div class="header-container">
                        <div class="h-col">{symbol.split('-')[0]}</div><div class="h-col">PREÇO ATUAL</div>
                        <div class="h-col" style="color:#FF4444;">EXAUSTÃO T.</div><div class="h-col">PRÓX. TOPO</div>
                        <div class="h-col" style="color:#FFFF00;">DECISÃO</div><div class="h-col">RESPIRO</div>
                        <div class="h-col">PRÓX. AO F.</div><div class="h-col" style="color:#00FF00;">EXAUSTÃO F.</div>
                    </div>
                    <div class="row-container">
                        <div class="w-col" style="color:#D4AF37; font-weight:bold;">{symbol.replace('-USD','/USDT')}</div>
                        <div class="w-col">
                            <div style="font-weight: bold; line-height: 1.1;">{int(price):,}</div>
                            <div style="color:{cor_v}; font-size:11px; font-weight:bold; margin-top: 2px;">{seta_v} {var_reset:+.2f}%</div>
                        </div>
                        <div class="w-col" style="{estilo_ex_t}">{int(mp * config['alvos'][0]):,}</div>
                        <div class="w-col" style="color:#FFA500;">{int(mp * config['alvos'][1]):,}</div>
                        <div class="w-col" style="{fundo_decisao}">{int(mp * config['alvos'][2]):,}</div>
                        <div class="w-col" style="color:#00CED1;">{int(mp * config['alvos'][3]):,}</div>
                        <div class="w-col" style="color:#FFA500;">{int(mp * config['alvos'][4]):,}</div>
                        <div class="w-col" style="{estilo_ex_f}">{int(mp * config['alvos'][5]):,}</div>
                    </div>
                    <div style="display: flex; justify-content: center; gap: 80px; margin-top: 10px; border-bottom: 2px solid #333; padding-bottom: 10px;">
                        <div style="text-align: center;">
                            <div style="color: #888; font-size: 10px; text-transform: uppercase;">ResetVision (Fixo)</div>
                            <div style="color: #ffffff; font-size: 16px; font-weight: bold;">{int(rv_valor):,}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888; font-size: 10px; text-transform: uppercase;">ÂncoraVision (Móvel)</div>
                            <div style="color: #00e6ff; font-size: 16px; font-weight: bold;">{int(mp):,}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Footer original mantido no final
            st.markdown(f"""
                <div class="footer">
                    <div><span class="dot"></span> LIVESTREAM ATIVO</div>
                    <div>LONDRES: {now_lon.strftime('%H:%M:%S')}</div>
                    <div>BRASÍLIA: {now_br.strftime('%H:%M:%S')}</div>
                    <div>NEW YORK: {now_ny.strftime('%H:%M:%S')}</div>
                </div>
            """, unsafe_allow_html=True)
            
        time.sleep(1)
    except Exception as e:
        time.sleep(5)
