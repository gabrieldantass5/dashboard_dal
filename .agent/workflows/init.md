---
description: Inicializa o ecossistema Antigravity no projeto, sincroniza contexto e valida o ambiente.
---

// turbo-all

# 🦅 COMANDO: /init (Dashboard DAL v1.0)

Este workflow prepara o **Antigravity AI** para operar no projeto Dashboard de Controle Orçamentário da DAL/CBMAL.

## 🎯 Objetivos do Init

1. **Mapear** o estado atual do projeto.
2. **Sincronizar** as diretrizes técnicas e visuais (CLAUDE.md + Identidade Visual).
3. **Validar** o ambiente de execução (Python, Streamlit, Data).
4. **Estabelecer** a memória de curto prazo para a sessão.

## 🛠️ Passos da Execução

### 1. 🔍 Descoberta e Contexto

O agente deve ler os arquivos fundamentais para se situar:

- `CLAUDE.md`: Convenções de código e estrutura.
- `LEIA-ME-PRIMEIRO.md`: Status atual e instruções de início rápido.
- `docs/04_SPECS_TECNICAS.md`: Detalhes da implementação.

### 2. 🧪 Validação de Infraestrutura

- Verificar se a pasta `venv` existe.
- Verificar se `data/ORÇAMENTO 2025 (1).xlsx` está presente.
- Validar se `app.py` é o ponto de entrada principal.

### 3. 🧠 Sincronização da Memória (DNA do Projeto)

- Criar ou atualizar o arquivo `DNA_PROJETO.md` na raiz com:
  - **Objetivo**: Dashboard Orçamentário DAL.
  - **Status**: 100% Funcional (MVP).
  - **Stack**: Python 3.9+, Streamlit, Plotly, Pandas.
  - **Últimas Verificações**: 11/02/2026.

### 4. 🏁 Boas-Vindas e Status Report

Apresentar ao usuário um resumo executivo:

- **Projeto**: Dashboard DAL/CBMAL
- **Ambiente**: [OK/Erro]
- **Dados**: [Sim/Não]
- **Sugestão**: "Comandante, o sistema está pronto. Deseja executar o dashboard ou iniciar uma nova feature?"

---
*Powered by Antigravity AI - Colaboração 7ª Seção EMG.*
