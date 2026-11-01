# ⚡ DocAudit AI — Agente de Grounding & Governança de Custos de LLM

Microsserviço experimental de inteligência artificial generativa desenvolvido como protótipo ágil ("jet-ski") focado em auditoria documental, mitigação de alucinações e telemetria de consumo de tokens.

---

## 🎯 Problema de Negócio & Contexto
A utilização ingênua de Large Language Models (LLMs) em rotinas corporativas de alta precisão (contratos, regulação, operações) apresenta dois riscos centrais:
1. **Alucinações e Extrapolações Fatuais**: Modelos generativos tendem a assumir premissas ausentes do texto original quando não submetidos a ancoragem (*grounding*) estrita.
2. **Descontrole Financeiro ("Tokens são dinheiro")**: Chamadas extensas e prompts não otimizados geram consumo desnecessário de orçamento computacional.

O **DocAudit AI** resolve esse gargalo aplicando engenharia de contexto determinística e telemetria por requisição, espelhando os princípios de ambidestria e foco em 80/20.

---

## 🛠️ Funcionalidades & Arquitetura
* **Grounding Estrito**: Prompt estruturado para confrontar documentos extensos contra critérios normativos, forçando a detecção de omissões sem gerar falsos positivos.
* **Telemetria de Tokens & Latência**: Medição em tempo real do tempo de processamento, estimativa de tokens consumidos e projeção do custo de inferência por execução.
* **Saída Estruturada**: Geração automática de diagnóstico executivo e matriz de riscos acionável.

---

## 💻 Stack Tecnológica
* **Linguagem**: Python
* **Interface**: Streamlit
* **Modelo**: Google Gemini API (`gemini-1.5-flash` / `gemini-1.5-pro`)
* **Engenharia de Prompt**: Few-shot / Constraint prompting para ancoragem factual
