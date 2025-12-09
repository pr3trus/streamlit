import streamlit as st

st.title("📅 AGENDA DA SEMANA")

if "estudos" not in st.session_state or not st.session_state.estudos:
    st.info("📭 Nenhum estudo agendado ainda.")
    st.write("Vá para **➕ Adicionar** para cadastrar seu primeiro estudo!")
else:
    # Dias da semana
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
    # Mostra estudos por dia
    for dia in dias:
        estudos_dia = [e for e in st.session_state.estudos if e.get("dia") == dia]
        if estudos_dia:
            st.write(f"#### 📅 {dia}")
            
            for estudo in estudos_dia:
                materia = estudo.get("materia", "Sem nome")
                horas = estudo.get("horas", 0)
                prioridade = estudo.get("prioridade", "Média")
                
                # Ícone da prioridade
                icon = {"Alta": "🔴", "Média": "🟡", "Baixa": "🟢"}.get(prioridade, "🟡")
                
                # Editar prioridade
                col1, col2, col3 = st.columns([3, 1, 2])
                with col1:
                    st.write(f"{icon} **{materia}**")
                with col2:
                    st.write(f"⏰ **{horas}h**")
                with col3:
                    nova = st.selectbox(
                        "Prioridade",
                        ["Baixa", "Média", "Alta"],
                        index=["Baixa", "Média", "Alta"].index(prioridade),
                        key=f"prio_{dia}_{materia}",
                        label_visibility="collapsed"
                    )
                    if nova != prioridade:
                        estudo["prioridade"] = nova
                        st.rerun()
                st.write("---")
    
    # Estatísticas
    st.write("---")
    st.write("### 📊 Estatísticas:")
    
    total = len(st.session_state.estudos)
    horas = sum(e.get("horas", 0) for e in st.session_state.estudos)
    materias = len(set(e.get("materia", "") for e in st.session_state.estudos))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Estudos", total)
    col2.metric("Horas", f"{horas}h")
    col3.metric("Matérias", materias)
    
    # Prioridades
    contagem = {"Alta": 0, "Média": 0, "Baixa": 0}
    for e in st.session_state.estudos:
        p = e.get("prioridade", "Média")
        contagem[p] = contagem.get(p, 0) + 1
    
    st.write("##### Prioridades:")
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Alta", contagem["Alta"])
    col2.metric("🟡 Média", contagem["Média"])
    col3.metric("🟢 Baixa", contagem["Baixa"])
    
    # Ferramentas
    st.write("---")
    if st.button("🗑️ Limpar Tudo", type="primary"):
        if st.checkbox("Confirmar"):
            st.session_state.estudos = []
            st.rerun()