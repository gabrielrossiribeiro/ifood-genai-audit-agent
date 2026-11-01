import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(
    page_title="DocAudit AI | iFood GenAI Engine",
    page_icon="⚡",
    layout="wide"
)

# Estilização visual limpa
st.markdown("""
    <style>
    .main-title { font-size: 2.1rem; font-weight: 700; color: #0F172A; }
    .sub-title { font-size: 1rem; color: #64748B; margin-bottom: 1.5rem; }
    .metric-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ DocAudit AI: Grounding & Governança de LLMs</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Protótipo funcional de auditoria factual, mitigação de alucinações e telemetria de tokens ("Tokens são dinheiro").</div>', unsafe_allow_html=True)

# Barra Lateral - Governança e Custos
with st.sidebar:
    st.header("⚙️ Configurações & Custos")
    api_key = st.text_input("Gemini API Key:", type="password", help="Obtenha gratuitamente em aistudio.google.com")
    modelo_escolhido = st.selectbox("Modelo:", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    st.markdown("---")
    st.markdown("### 🎯 Princípio 80/20 & Eficiência")
    st.write("A arquitetura prioriza chamadas estruturadas e prompts compactados para minimizar latência e evitar sobrecusto em inferências repetitivas.")

# Área Principal - Inputs
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
        placeholder="Ex: Identificar omissões sobre SLA de entrega, responsabilidade por perda e cláusulas de rescisão sem aviso prévio de 30 dias..."
    )

# Execução
if st.button("Executar Análise Crítica com Grounding"):
    if not api_key:
        st.error("Informe uma API Key do Google Gemini na barra lateral para processar.")
    elif not documento.strip() or not diretriz.strip():
        st.warning("Preencha tanto o documento quanto a diretriz de validação.")
    else:
        with st.spinner("Processando com Grounding estrito..."):
            try:
                start_time = time.time()
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(modelo_escolhido)

                prompt = f"""
                Você é um auditor rigoroso de conformidade, operações e integridade de dados.
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

                # Cálculo de métricas de telemetria ("Tokens são dinheiro")
                tokens_entrada = int(len(prompt.split()) * 1.33)
                tokens_saida = int(len(response.text.split()) * 1.33)
                total_tokens = tokens_entrada + tokens_saida

                # Custo aproximado com base na tabela do Gemini 1.5 Flash ($0.075 / 1M tokens)
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
