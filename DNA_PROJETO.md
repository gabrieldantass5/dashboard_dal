# 🧬 DNA DO PROJETO - Dashboard DAL

## 🎯 Objetivo Geral

Dashboard interativo para controle e visualização do orçamento da Diretoria de Apoio Logístico (DAL) do CBMAL para o exercício de 2025. Substitui o controle manual em Excel por uma interface analítica moderna.

## 📊 Status Atual (11/02/2026)

- **Fase**: MVP 1.0 + Sprint 2 + Sprint 3 = **100% DO PRD CONCLUÍDO** ✅
- **Qualidade**: 100% validado e testado.
- **Performance**: Carregamento < 5s com cache ativado.
- **Última Feature**: F10 - Projeções e Alertas Automáticos ✅
- **Progresso**: **TODAS as funcionalidades do PRD implementadas!**
- **Funcionalidades**: MVP + F6 + F7 + F8 + F9 + F10 = **10 features completas**

## 🏗️ Arquitetura Técnica

- **Linguagem**: Python 3.9+
- **Interface**: Streamlit 1.31+
- **Visualização**: Plotly 5.18+
- **Processamento**: Pandas 2.1+
- **Fonte de Dados**: Excel (`data/ORÇAMENTO 2025 (1).xlsx`)

### Módulos do Sistema

1. `src/data_loader.py`: Responsável pelo ETL (Extract, Transform, Load) das abas 'CONTROLE DE DESPESAS' e 'BALANCO'.
2. `src/data_processor.py`: Motor de cálculo de KPIs, agregações e filtragem lógica.
3. `src/visualizations.py`: Gerador de gráficos Plotly (Barras horizontais, Barras agrupadas).
4. `src/utils.py`: Funções auxiliares de formatação de moeda, percentual e constantes de design.
5. `app.py`: Orquestrador da interface e integração dos módulos.

## 📈 Métricas de Referência (Valores Reais)

- **Total de Recursos**: R$ 27.281.568,51
- **Total Empenhado**: R$ 23.382.410,38
- **Saldo Total**: R$ 3.899.158,13
- **Número de Processos**: 259 (ativos)

## 🎨 Identidade Visual

- **Primária**: Azul Institucional (Streamlit Default)
- **Alertas**: Vermelho (#C10A0A) para baixa disponibilidade.
- **Gráficos**: Paleta Plotly combinada com cores customizadas para as 5 fontes de recursos.

## 🚀 Próximos Passos

1. Implementar filtros por Elementos de Despesa.
2. Adicionar visualização do PCA 2025.
3. Versão 2.0: Histórico temporal de execução.

---
*Gerado por Antigravity AI - Sincronizado via /init*
