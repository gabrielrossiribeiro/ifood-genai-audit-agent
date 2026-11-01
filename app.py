import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
    page_title="DocAudit AI | iFood GenAI Engine",
    page_icon="⚡",
    layout="wide"
)

# Estilização visual executiva
st.markdown("""
    <style>
    .main-title { font-size: 2.1rem; font-weight: 700; color: #0F172A; }
    .sub-title { font-size: 1rem; color: #64748B; margin-bottom: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ DocAudit AI: Grounding & Governança de LLMs</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Protótipo funcional de auditoria factual, mitigação de alucinações e telemetria de tokens ("Tokens são dinheiro").</div>', unsafe_allow_html=True)

# Barra Lateral - Governança e Configurações
with st.sidebar:
    st.header("⚙️ Configurações & Custos")
    api_key = st.text_input("Gemini API Key:", type="password", help="Chave gerada em aistudio.google.com")

    # Lista padrão alinhada com as versões ativas do Google Gemini
    modelos_disponiveis = ["gemini-3.8-flash", "gemini-3.8-pro", "gemini-1.5-flash"]
    
    if api_key.strip():
        try:
            genai.configure(api_key=api_key.strip())
            models_list = [
                m.name.replace("models/", "")
                for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
                and "2.5" not in m.name  # Filtra modelos descontinuados
            ]
            if models_list:
                # Prioriza gemini-3.8-flash no topo
                modelos_disponiveis = sorted(
                    models_list,
                    key=lambda x: (not ("3.8-flash" in x), not ("flash" in x), not ("pro" in x), x)
                )
        except Exception:
            pass

    modelo_escolhido = st.selectbox("Modelo:", modelos_disponiveis)
    
    st.markdown("---")
    st.markdown("### 🎯 Princípio 80/20 & Eficiência")
    st.write("A arquitetura prioriza chamadas estruturadas e prompts compactados para minimizar latência e evitar sobrecusto em inferências repetitivas.")

# Área Principal - Entradas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Documento para Auditoria")
    documento = st.text_area(
        "Minuta, Contrato ou Regulamento:",
        height=320,
        placeholder="Cole o texto que precisa ser conferido com rigor factual..."
    )

with col2:
    st.subheader("📋 Diretriz / Critério de Validação")
    diretriz = st.text_area(
        "Regra de Grounding ou Compliance:",
        height=320,
        placeholder="Ex: Identificar omissões sobre SLA de entrega, multas rescisórias sem aviso prévio e responsabilidade civil..."
    )

# Execução da Análise
if st.button("Executar Análise Crítica com Grounding"):
    if not api_key.strip():
        st.error("Informe uma API Key do Google Gemini na barra lateral para processar.")
    elif not documento.strip() or not diretriz.strip():
        st.warning("Preencha tanto o documento quanto a diretriz de validação.")
    else:
        with st.spinner("Processando auditoria com Grounding estrito..."):
            try:
                start_time = time.time()
                genai.configure(api_key=api_key.strip())
                model = genai.GenerativeModel(modelo_escolhido)

                prompt = f"""
                Você é um auditor sênior de operações, integridade de dados e conformidade regulatória.
                Sua tarefa é auditar o documento fornecido exclusivamente sob a ótica da diretriz especificada.

                DIRETRIZ DE VERIFICAÇÃO:
                \"\"\"{diretriz}\"\"\"

                DOCUMENTO ANALISADO:
                \"\"\"{documento}\"\"\"

                REGRAS ESTRITAS DE GROUNDING:
                1. Seja brutal com os fatos. Aponte lacunas, riscos contratuais/operacionais e omissões textuais.
                2. NUNCA extrapole nem alucine fatos que não estejam presentes no documento. Se algo não constar expressamente, declare: "Informação não constante do documento".
                3. Estruture sua resposta estritamente nas seguintes seções Markdown:
                   - ### 1. Diagnóstico Executivo (Síntese objetiva em até 3 linhas)
                   - ### 2. Tabela de Riscos e Inconsistências Detectadas (Colunas: Ponto Analisado | Risco Operacional / Desvio | Recomendação Direta)
                   - ### 3. Classificação de Risco Geral (Baixo, Médio ou Crítico, justificando a decisão)
                """

                response = model.generate_content(prompt)
                tempo_execucao = round(time.time() - start_time, 2)

                # Telemetria ("Tokens são dinheiro")
                tokens_entrada = int(len(prompt.split()) * 1.33)
                tokens_saida = int(len(response.text.split()) * 1.33)
                total_tokens = tokens_entrada + tokens_saida

                # Custo de referência de modelos Flash ($0.075 por 1M tokens)
                custo_estimado = (total_tokens / 1_000_000) * 0.075

                st.markdown("---")
                st.subheader("📊 Métricas de Eficiência da Execução")
                m1, m2, m3 = st.columns(3)
                m1.metric("Tempo de Resposta", f"{tempo_execucao}s")
                m2.metric("Tokens Consumidos", f"~{total_tokens}")
                m3.metric("Custo Estimado", f"${custo_estimado:.6f} USD")

                st.markdown("---")
                st.subheader("📑 Relatório de Auditoria Factually Grounded")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Erro ao processar chamada: {str(e)}")
