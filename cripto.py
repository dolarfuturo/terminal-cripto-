# 2. MOTOR PRINCIPAL
placeholder = st.empty()

while True:
    # Reset Automático às 00:00 UTC (Binance)
    agora_utc = datetime.now(pytz.utc)
    if agora_utc.hour == 0 and agora_utc.minute == 0 and agora_utc.second < 5:
        for t in COINS_CONFIG:
            st.session_state[f'mp_{t}'] = yf.Ticker(t).fast_info['last_price']
            st.session_state[f'rv_{t}'] = st.session_state[f'mp_{t}']
        st.rerun()

    placeholder.empty()
    with placeholder.container():
        # RECOLOQUEI O TÍTULO QUE SUMIU
        st.markdown('<div class="title-container"><div class="title-gold">ALPHA VISION CRYPTO</div><div class="subtitle-white">visão de tubarão</div></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="header-container">
                <div class="h-col">CÓDIGO</div>
                <div class="h-col">PREÇO ATUAL</div>
                <div class="h-col" style="color: #FF4444;">EXAUSTÃO T.</div>
                <div class="h-col">PRÓX. TOPO</div>
                <div class="h-col" style="color: #FFFF00;">DECISÃO</div>
                <div class="h-col">RESPIRO</div>
                <div class="h-col">PRÓX. AO F.</div>
                <div class="h-col" style="color: #00FF00;">EXAUSTÃO F.</div>
            </div>
        """, unsafe_allow_html=True)

        for ticker, info in COINS_CONFIG.items():
            price = yf.Ticker(ticker).fast_info['last_price']
            mp = st.session_state[f'mp_{ticker}']
            rv = st.session_state[f'rv_{ticker}']
            
            # CÁLCULO CORRETO: Preço vs ResetVision
            var_reset = ((price / rv) - 1) * 100
            cor_v, seta_v = ("#00FF00", "▲") if var_reset >= 0 else ("#FF4444", "▼")
            
            # Variação da Escada (Preço vs Âncora)
            abs_var = abs(((price / mp) - 1) * 100)
            fundo_p = "background: rgba(255, 255, 0, 0.2);" if 0.59 <= abs_var <= 0.65 else ""

            st.markdown(f"""
                <div class="row-container">
                    <div class="w-col" style="font-size: 18px;">{info['label']}</div>
                    <div class="w-col" style="{fundo_p}">
                        <div style="font-size: 20px; font-weight: bold;">{f"{price:,.{info['dec']}f}"}</div>
                        <div style="font-size: 12px; color: {cor_v}; font-weight: 800;">{seta_v} {var_reset:.2f}%</div>
                    </div>
                    <div class="w-col" style="color: #FF4444;">{f"{(mp * 1.0135):,.{info['dec']}f}"}</div>
                    <div class="w-col">{f"{(mp * 1.0122):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #FFFF00;">{f"{(mp * 1.0062):,.{info['dec']}f}"}</div>
                    <div class="w-col">{f"{(mp * 0.9938):,.{info['dec']}f}"}</div>
                    <div class="w-col">{f"{(mp * 0.9878):,.{info['dec']}f}"}</div>
                    <div class="w-col" style="color: #00FF00;">{f"{(mp * 0.9865):,.{info['dec']}f}"}</div>
                </div>
                <div style="display: flex; justify-content: center; gap: 100px; padding: 10px 0 20px 0; border-bottom: 2px solid #111;">
                    <div style="text-align: center;">
                        <div style="font-size: 9px; color: #555;">RESETVISION</div>
                        <div style="font-size: 15px; font-weight: bold; color: #FFF;">{f"{rv:,.{info['dec']}f}"}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="text-align: center;">
                        <div style="font-size: 9px; color: #555;">ÂNCORAVISION</div>
                        <div style="font-size: 15px; font-weight: bold; color: #00FFFF;">{f"{mp:,.{info['dec']}f}"}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    time.sleep(1)
