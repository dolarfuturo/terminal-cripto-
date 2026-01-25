import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuração de Estilo Profissional
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    .title { color: #D4AF37; text-align: center; font-family: 'serif'; font-weight: bold; margin-bottom: 0px; }
    .subtitle { color: #FFFFFF; text-align: center; letter-spacing: 5px; font-size: 12px; margin-bottom: 30px; }
    
    /* Estilização da Tabela */
    table { background-color: #000 !important; color: white !important; width: 100%; border-collapse: collapse; }
    th { color: #D4AF37 !important; background-color: #111 !important; text-align: left !important; padding: 10px; border-bottom: 1px solid #333; }
    td { padding: 12px; border-bottom: 1px solid #222; font-family: 'monospace'; font-size: 16px; }
    
    .price-up { color: #00ff00; font-weight: bold; }
    .price-down { color: #ff0000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Cabeçalho
st.markdown("<h1 class='title'>ALPHA VISION CRYPTO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>VISÃO DE TUBARÃO</p>", unsafe_allow_html=True)

# Lista de Ativos e Eixo Mestre (BTC)
ativos = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD"]
EIXO_BTC = 89795.0

def get_market_data():
    rows = []
    for ticker in ativos:
        try:
            t = yf.Ticker(ticker)
            info = t.fast_info
            preco = info['last_price']
            prev_close = info['previous_close']
            var_pct = ((preco / prev_close) - 1) * 100
            
            # Seta e Cor
            seta = "▲" if var_pct >= 0 else "▼"
            cor = "price-up" if var_pct >= 0 else "price-down"
            
            # Referência para cálculo de alvos
            ref = EIXO_BTC if ticker == "BTC-USD" else preco
            
            def calc(p): return f"{ref * (1 + (p/100)):,.2f}"

            # Criando a linha com preços puros
            rows.append(f"""
                <tr>
                    <td>{ticker.replace("-USD", "/USDT")}</td>
                    <td><span class='{cor}'>{preco:,.2f} {seta} ({var_pct:.2f}%)</span></td>
                    <td>{calc(1.22)}</td>
                    <td>{calc(0.83)}</td>
                    <td>{calc(0.61)}</td>
                    <td>{calc(0.40)}</td>
                    <td><span style='color: #00d4ff;'>ESTÁVEL</span></td>
                </tr>
            """)
        except:
            continue
    return "".join(rows)

# Renderização da Tabela Manual (para controle total de cores)
tabela_html = f"""
    <table>
        <thead>
            <tr>
                <th>ATIVO</th>
                <th>PREÇO ATUAL</th>
                <th>1.22% EXAUSTÃO</th>
                <th>0.83% TOPO</th>
                <th>0.61% PARCIAL</th>
                <th>0.40% RESPIRO</th>
                <th>SINAL</th>
            </tr>
        </thead>
        <tbody>
            {get_market_data()}
        </tbody>
    </table>
"""

st.markdown(tabela_html, unsafe_allow_html=True)

# Motor de atualização em tempo real
time.sleep(3)
st.rerun()
