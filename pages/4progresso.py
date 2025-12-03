import streamlit as st

st.title("📊 PROGRESSO E ESTATÍSTICAS")

if "estudos" not in st.session_state or not st.session_state.estudos:
    st.info("📭 Adicione estudos para ver o progresso.")
else:
    # Calcula horas por matéria
    horas_mat = {}
    for estudo in st.session_state.estudos:
        mat = estudo["materia"]
        horas = estudo["horas"]
        horas_mat[mat] = horas_mat.get(mat, 0) + horas
    
    # Mostra progresso
    st.subheader("⏱️ Total de Horas por Matéria")
    
    for mat, horas in horas_mat.items():
        st.write(f"### {mat}")
        st.write(f"**{horas:.1f} horas** estudadas")
        
        # Barra de progresso se tiver meta
        if "metas" in st.session_state and mat in st.session_state.metas:
            meta = st.session_state.metas[mat]
            
            if horas >= meta:
                st.success(f"🎉 **Meta de {meta}h ATINGIDA!**")
                st.progress(1.0)
            else:
                progresso = horas / meta
                st.write(f"**Progresso:** {horas:.1f}h / {meta}h")
                st.progress(progresso)
                st.write(f"Faltam **{meta-horas:.1f}h**")
        else:
            st.info("ℹ️ Meta não definida para esta matéria")
        
        st.markdown("---")
    
    # Estatísticas gerais
    st.subheader("📈 Estatísticas Gerais")
    
    total_estudado = sum(horas_mat.values())
    total_metas = sum(st.session_state.metas.values()) if "metas" in st.session_state else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de horas", f"{total_estudado:.1f}h")
    with col2:
        st.metric("Matérias diferentes", len(horas_mat))
    with col3:
        if total_metas > 0:
            st.metric("Meta total", f"{total_metas}h")
