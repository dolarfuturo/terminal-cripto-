import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configuração de Estilo "Tubarão" (Preto e Dourado)
st.set_page_config(page_title="ALPHA VISION CRYPTO", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; }
    .title { color: #D4AF37; text-align: center; font-family: 'serif'; font-weight: bold; margin-bottom: 0px; }
    .subtitle { color: #FFFFFF; text-align: center; letter-spacing: 5px; font-size: 12px; margin-bottom: 30px; }
    
    /* Tabela Profissional */
    .reportview-container .main .block-container { padding-top: 1rem; }
    table { width: 100%; border-collapse: collapse; background-color: #000; color: white; }
    th { color: #D4AF37 !important; background-color: #111 !important; padding: 10px; border-bottom: 1px solid #333; text-align: center; font-size: 11px; }
    td { padding: 10px; border-bottom: 1px solid #222; font-family: 'monospace'; font-size: 13px; text-align: center; }
    
    .up { color: #00ff00; font-weight: bold; }
    .down { color: #ff0000; font-weight: bold; }
    .stApp { background-color: #000000; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title'>ALPHA VISION CRYPTO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>VISÃO DE TUBARÃO</p>", unsafe_allow_html=True)

# Lista de Ativos e Eixo Mestre
ativos = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD"]
EIXO_BTC = 89795.0

def render_table():
    html_rows = ""
    for ticker in ativos:
        try:
            # Coleta de dados via YFinance (Sinal estável)
            data = yf.Ticker(ticker).fast_info
            preco = data['last_price']
            pc = data['previous_close']
            var = ((preco / pc) - 1) * 100
            
            cor = "up" if var >= 0 else "down"
            seta = "▲" if var >= 0 else "▼"
            
            # Referência para os cálculos da planilha
            ref = EIXO_BTC if ticker == "BTC-USD" else preco
            def c(p): return f"{ref * (1 + (p/100)):,.2f}"

            html_rows += f"""
                <tr>
                    <td style='font-weight:bold;'>{ticker.replace("-USD", "/USDT")}</td>
                    <td class='{cor}'>{preco:,.2f}<br><small>{seta} {var:.2f}%</small></td>
                    <td>{c(1.22)}</td>
                    <td>{c(0.83)}</td>
                    <td>{c(0.61)}</td>
                    <td>{c(0.40)}</td>
                    <td>{c(-0.40)}</td>
                    <td>{c(-0.61)}</td>
                    <td>{c(-0.83)}</td>
                    <td>{c(-1.22)}</td>
                </tr>
            """
        except:
            continue
    return html_rows

# Estrutura da Tabela baseada na sua Planilha (Imagem 1000027192)
tabela_completa = f"""
    <table>
        <thead>
            <tr>
                <th>CÓDIGO</th>
                <th>PREÇO ATUAL</th>
                <th>EXAUSTÃO<br>(1.22%)</th>
                <th>PRÓX. TOPO<br>(0.83%)</th>
                <th>DECISÃO<br>(0.61%)</th>
                <th>RESPIRO<br>(0.40%)</th>
                <th>RESPIRO FUNDO<br>(-0.40%)</th>
                <th>DECISÃO FUNDO<br>(-0.61%)</th>
                <th>PRÓX. FUNDO<br>(-0.83%)</th>
                <th>EXAUSTÃO FUNDO<br>(-1.22%)</th>
            </tr>
        </thead>
        <tbody>
            {render_table()}
        </tbody>
    </table>
"""

st.markdown(tabela_completa, unsafe_allow_html=True)

# Motor de Tempo Real
time.sleep(5)
st.rerun()
