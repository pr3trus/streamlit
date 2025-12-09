import streamlit as st
import pandas as pd

st.title("📅 AGENDA DA SEMANA")

# Verifica se tem estudos
if "estudos" not in st.session_state or not st.session_state.estudos:
    st.info("📭 Nenhum estudo agendado ainda.")
    st.write("Vá para **➕ Adicionar** para cadastrar seu primeiro estudo!")
    
else:
    st.write("### 📋 Seus Estudos Agendados:")
    
    # Ordem dos dias da semana
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    
    # Cria uma seção para cada dia
    for dia in dias_semana:
        # Filtra estudos deste dia
        estudos_do_dia = []
        
        for estudo in st.session_state.estudos:
            # Verifica se o estudo tem 'dia' e se é o dia correto
            if "dia" in estudo and estudo["dia"] == dia:
                estudos_do_dia.append(estudo)
        
        # Se tem estudos neste dia, mostra
        if estudos_do_dia:
            st.write(f"#### 📅 {dia}")
            
            # Mostra cada estudo deste dia
            for estudo in estudos_do_dia:
                # Pega os valores com segurança (usando .get() para não dar erro)
                materia = estudo.get("materia", "Matéria não especificada")
                horas = estudo.get("horas", 0)
                prioridade = estudo.get("prioridade", "Média")  # Valor padrão
                
                # Ícone de prioridade
                if prioridade == "Alta":
                    icon = "🔴"
                elif prioridade == "Média":
                    icon = "🟡"
                else:
                    icon = "🟢"
                
                # Mostra o estudo
                st.write(f"{icon} **{materia}**")
                st.write(f"   ⏰ **{horas}h** | Prioridade: **{prioridade}**")
                st.write("---")
    
    # ESTATÍSTICAS
    st.write("---")
    st.write("### 📊 Estatísticas:")
    
    # Calcula totais
    total_estudos = len(st.session_state.estudos)
    
    total_horas = 0
    for estudo in st.session_state.estudos:
        total_horas += estudo.get("horas", 0)
    
    # Mostra em colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Estudos", total_estudos)
    
    with col2:
        st.metric("Total de Horas", f"{total_horas:.1f}h")
    
    with col3:
        # Conta matérias diferentes
        materias = []
        for estudo in st.session_state.estudos:
            materia = estudo.get("materia", "")
            if materia and materia not in materias:
                materias.append(materia)
        st.metric("Matérias Diferentes", len(materias))
    
    # BOTÃO PARA CORRIGIR DADOS
    st.write("---")
    st.write("### ⚙️ Ferramentas:")
    
    # Verifica se tem estudos sem prioridade
    tem_sem_prioridade = False
    for estudo in st.session_state.estudos:
        if "prioridade" not in estudo:
            tem_sem_prioridade = True
            break
    
    if tem_sem_prioridade:
        st.warning("⚠️ Alguns estudos antigos não têm prioridade definida.")
        
        if st.button("🔧 Corrigir Estudos Antigos", type="secondary"):
            # Adiciona prioridade "Média" aos estudos que não têm
            estudos_corrigidos = []
            for estudo in st.session_state.estudos:
                if "prioridade" not in estudo:
                    estudo["prioridade"] = "Média"
                estudos_corrigidos.append(estudo)
            
            st.session_state.estudos = estudos_corrigidos
            st.success("✅ Estudos corrigidos! Atualize a página (F5).")
    
    # BOTÃO PARA LIMPAR TUDO
    if st.button("🗑️ Limpar Todos os Estudos", type="primary"):
        confirmar = st.checkbox("Tem certeza? Isso apaga TUDO!")
        if confirmar:
            st.session_state.estudos = []
            st.success("✅ Todos os estudos foram apagados!")
            st.rerun()