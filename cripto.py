# 3. MONITORAMENTO AUTOMÁTICO DO EIXO (11:30 - 18:00)
st.markdown('<div class="title-gold">ALPHA VISION CRYPTO</div>', unsafe_allow_html=True)

def calcular_eixo_automatico():
    try:
        ticker = yf.Ticker("BTC-USD")
        # Puxa dados de hoje com intervalo de 1 minuto para precisão
        hist = ticker.history(period="1d", interval="1m")
        if hist.empty: return 89795.0 # Valor de segurança caso falhe
        
        # Filtra o horário de Brasília (11:30 às 18:00)
        # Nota: YFinance usa UTC, Brasília é UTC-3
        hist.index = hist.index.tz_convert('America/Sao_Paulo')
        janela_alpha = hist.between_time('11:30', '18:00')
        
        if not janela_alpha.empty:
            maximo = janela_alpha['High'].max()
            minimo = janela_alpha['Low'].min()
            return (maximo + minimo) / 2
        return 89795.0
    except:
        return 89795.0

# EIXO CALCULADO PELO MOTOR ALPHA
EIXO_MESTRE = calcular_eixo_automatico()
ticker_id = "BTC-USD"
placeholder = st.empty()

while True:
    try:
        data = yf.Ticker(ticker_id).fast_info
        price = data['last_price']
        change_pct = ((price / EIXO_MESTRE) - 1) * 100
        
        with placeholder.container():
            st.markdown(f"""<div class="header-container">
                <div class="h-col" style="width:14%; text-align:left; padding-left:10px;">BTC/USDT</div>
                <div class="h-col" style="width:15%;">EIXO: {EIXO_MESTRE:,.2f}</div>
                <div class="h-col" style="width:9%;">EXAUSTÃO (1.22)</div>
                <div class="h-col" style="width:9%;">PRÓX. TOPO (0.83)</div>
                <div class="h-col" style="width:9%;">DECISÃO (0.61)</div>
                <div class="h-col" style="width:9%;">RESPIRO (0.40)</div>
                <div class="h-col" style="width:9%;">RESPIRO F. (-0.40)</div>
                <div class="h-col" style="width:9%;">DECISÃO F. (-0.61)</div>
                <div class="h-col" style="width:14%;">SINALIZADOR</div></div>""", unsafe_allow_html=True)

            def calc(p): return EIXO_MESTRE * (1 + (p/100))
            
            abs_c = abs(change_pct)
            s_txt, s_class = "ESTÁVEL", "bg-estavel"
            if abs_c >= 1.22: s_txt, s_class = "EXAUSTÃO", "target-blink-red" if change_pct > 0 else "target-blink-green"
            elif abs_c >= 0.83: s_txt, s_class = "PRÓX. TOPO", "bg-atencao"
            elif abs_c >= 0.61: s_txt, s_class = "REGIÃO DE DECISÃO", "bg-decisao"

            arrow = "▲" if price >= EIXO_MESTRE else "▼"
            t_color = "#00FF00" if price >= EIXO_MESTRE else "#FF0000"

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-ativo" style="color:#D4AF37;">BTC/USDT</div>
                    <div class="w-price">{price:,.2f} <span style="color:{t_color};">{arrow}</span>
                        <span class="perc-val" style="color:{t_color};">{change_pct:+.2f}% do Eixo</span></div>
                    <div class="w-target" style="color:#FF4444; width:9%;">{calc(1.22):,.2f}</div>
                    <div class="w-target" style="color:#FFA500; width:9%;">{calc(0.83):,.2f}</div>
                    <div class="w-target" style="color:#FFFF00; width:9%;">{calc(0.61):,.2f}</div>
                    <div class="w-target" style="color:#00CED1; width:9%;">{calc(0.40):,.2f}</div>
                    <div class="w-target" style="color:#00CED1; width:9%;">{calc(-0.40):,.2f}</div>
                    <div class="w-target" style="color:#FFFF00; width:9%;">{calc(-0.61):,.2f}</div>
                    <div class="w-sinal"><div class="status-box {s_class}">{s_txt}</div></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="footer-live">🟢 EIXO DINÂMICO (11:30-18:00 BR) | RESET 00:00 UTC</div>', unsafe_allow_html=True)
            
        time.sleep(2)
    except:
        time.sleep(5)
