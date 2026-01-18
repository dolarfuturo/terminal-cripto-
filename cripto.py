# 2. LOGIN ROBUSTO COM NÍVEL DE ACESSO E SUPORTE
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.role = None

if not st.session_state.autenticado:
    st.markdown('<div class="title-gold">ALPHA VISION</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        
        # LINK DE SUPORTE FIXO
        st.markdown("""
            <div style="text-align: center; margin-top: -10px; margin-bottom: 15px;">
                <a href="https://wa.me/SEU_NUMERO_AQUI" target="_blank" 
                   style="color: #C0C0C0; font-size: 11px; text-decoration: none; font-weight: 500;">
                   PRECISA DE SUPORTE? CLIQUE AQUI
                </a>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("LIBERAR ACESSO", use_container_width=True):
            try:
                st.cache_data.clear() 
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_users = conn.read(ttl=0) 
                df_users.columns = [str(c).strip().lower() for c in df_users.columns]
                user_row = df_users[df_users['user'].astype(str) == u]
                
                if not user_row.empty and str(p) == str(user_row.iloc[0]['password']).strip():
                    st.session_state.autenticado = True
                    st.session_state.role = str(user_row.iloc[0].get('role', 'user')).strip().lower()
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")
            except Exception as e:
                st.error("Erro de sincronização. Tente novamente.")
    st.stop()
