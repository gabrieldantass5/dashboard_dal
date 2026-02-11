# 📋 PLANO DE VOO - Dashboard DAL

## 🏗️ 1. Arquitetura/Estrutura

O projeto segue o padrão modular em Python:

- `app.py` (Core)
- `src/` (Lógica de Negócio e Dados)
- `data/` (Repositório de Planilhas)
- `docs/` (Memória Técnica)

## 🎯 2. Passo a Passo Pormenorizado

- [x] **Preparação**: Criar ecossistema `.agent` e `DNA_PROJETO.md`.
- [ ] **Feature A**: Implementar filtros de Elemento de Despesa.
- [ ] **Feature B**: Integrar aba PCA 2025.
- [ ] **Documentação**: Atualizar manual com FAQ de filtros.

## ⚠️ 3. Pontos de Risco

- **Inconsistência de Dados**: Se o Excel for alterado drasticamente, o parser pode quebrar (KeyError).
- **Performance**: Aumento de volume de dados pode impactar o tempo de renderização (Mitigação: @st.cache_data).
- **Ambiente**: Dependência de bibliotecas externas (Streamlit, Plotly) em versões específicas.

---
*Plano gerado em 11/02/2026 às 18:45.*
