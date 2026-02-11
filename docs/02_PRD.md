# PRD - Product Requirements Document
## Dashboard de Controle Orçamentário DAL/CBMAL

**Versão:** 1.0
**Data:** 11/02/2026
**Produto:** Dashboard Orçamentário Python/Streamlit
**Responsável:** Diretoria de Apoio Logístico - CBMAL

---

## 1. Visão Geral do Produto

### 1.1 Objetivo

Desenvolver um **dashboard interativo em Python** que substitua a planilha Excel atual (12 abas, 302 processos) por uma interface visual, dinâmica e intuitiva para controle e análise orçamentária da DAL/CBMAL.

### 1.2 Problema a Resolver

**Situação atual:**
- Planilha Excel complexa com 12 abas interligadas
- Atualização manual demorada e propensa a erros
- Dificuldade de visualizar rapidamente o status orçamentário
- Falta de gráficos dinâmicos para análise de tendências
- Comparativos orçado vs executado exigem cálculos manuais
- Dificuldade em identificar categorias em risco de estouro

**Solução proposta:**
Dashboard automatizado que:
- Carrega dados do Excel automaticamente
- Calcula saldos, percentuais e métricas em tempo real
- Apresenta visualizações interativas (gráficos, tabelas filtráveis)
- Permite análise por múltiplas dimensões (fonte, elemento, status)
- Exporta dados filtrados para análise externa

### 1.3 Benefícios Esperados

| Benefício | Impacto | Métrica de Sucesso |
|-----------|---------|-------------------|
| **Velocidade de análise** | Redução de 80% no tempo para gerar relatórios | < 5 minutos para análise completa |
| **Acurácia** | Eliminação de erros de cálculo manual | 100% de precisão nos cálculos |
| **Visualização** | Identificação rápida de riscos e oportunidades | < 30 segundos para identificar categorias em risco |
| **Acessibilidade** | Democratização do acesso aos dados | 3 perfis de usuário atendidos |
| **Aprendizado** | Material didático para curso de análise de dados | Projeto documentado e replicável |

---

## 2. Personas e User Stories

### Persona 1: Diretor de Apoio Logístico 👔

**Perfil:**
- Responsável pelas decisões estratégicas de alocação de recursos
- Pouco tempo disponível, precisa de informações consolidadas
- Foco em visão geral e alertas de risco

**User Stories:**

| ID | Como... | Quero... | Para que... | Prioridade |
|----|---------|----------|-------------|-----------|
| US-01 | Diretor | Visualizar saldo disponível total e por fonte em um único painel | Tomar decisões rápidas sobre novas demandas | P1 - CRÍTICA |
| US-02 | Diretor | Ver % de execução orçamentária em tempo real | Avaliar o ritmo de execução do orçamento | P1 - CRÍTICA |
| US-03 | Diretor | Receber alertas visuais de categorias com execução > 95% | Prevenir estouros orçamentários | P1 - CRÍTICA |
| US-04 | Diretor | Visualizar comparativo orçado vs executado por fonte | Entender desvios e realocações necessárias | P1 - CRÍTICA |
| US-05 | Diretor | Acessar dashboard em < 30 segundos | Consultar informações em reuniões urgentes | P2 - IMPORTANTE |

### Persona 2: Gestor Financeiro 💼

**Perfil:**
- Responsável pela execução operacional do orçamento
- Precisa de detalhamento médio para acompanhamento diário
- Foco em processos, empenhos e status

**User Stories:**

| ID | Como... | Quero... | Para que... | Prioridade |
|----|---------|----------|-------------|-----------|
| US-06 | Gestor | Visualizar status de todos os processos (empenhado, reservado, cancelado) | Acompanhar o andamento das contratações | P1 - CRÍTICA |
| US-07 | Gestor | Filtrar processos por fonte de recursos | Verificar execução específica de cada fonte | P1 - CRÍTICA |
| US-08 | Gestor | Buscar processos por número ou objeto | Localizar rapidamente informações específicas | P2 - IMPORTANTE |
| US-09 | Gestor | Visualizar execução do PCA 2025 por classe/grupo | Acompanhar metas do planejamento anual | P2 - IMPORTANTE |
| US-10 | Gestor | Exportar dados filtrados para CSV | Gerar relatórios personalizados para direção | P2 - IMPORTANTE |
| US-11 | Gestor | Ver distribuição de recursos por elemento de despesa | Entender composição dos gastos | P3 - DESEJÁVEL |

### Persona 3: Analista de Dados 📊

**Perfil:**
- Responsável pela atualização e análise detalhada dos dados
- Precisa de acesso a dados granulares e opções de filtro avançadas
- Foco em qualidade dos dados e análises profundas

**User Stories:**

| ID | Como... | Quero... | Para que... | Prioridade |
|----|---------|----------|-------------|-----------|
| US-12 | Analista | Visualizar tabela completa de despesas com ordenação | Analisar dados em detalhes e identificar padrões | P1 - CRÍTICA |
| US-13 | Analista | Aplicar múltiplos filtros simultaneamente (fonte + elemento + status) | Segmentar análises complexas | P2 - IMPORTANTE |
| US-14 | Analista | Ver evolução temporal da execução orçamentária | Identificar tendências e sazonalidades | P3 - DESEJÁVEL |
| US-15 | Analista | Comparar ano corrente com anos anteriores | Avaliar padrões históricos de execução | P3 - DESEJÁVEL |
| US-16 | Analista | Identificar dados inconsistentes ou nulos na planilha | Garantir qualidade dos dados antes da análise | P3 - DESEJÁVEL |

---

## 3. Funcionalidades Detalhadas

### 3.1 PRIORIDADE 1 - Features Essenciais (MVP)

#### F1: Painel de KPIs Principais

**Descrição:** Exibir 5 métricas-chave no topo do dashboard

**KPIs obrigatórios:**
1. **Total de Recursos:** R$ 27.281.568,51 (soma de todas as fontes)
2. **Total Empenhado:** R$ 23.382.410,38 (soma de empenhos)
3. **Saldo Disponível:** Recursos - Empenhado
4. **Processos Ativos:** 302 processos (excluindo cancelados)
5. **Taxa de Execução:** (Empenhado / Dotado) × 100

**Design:**
- Layout horizontal em 5 colunas
- Valores em destaque (fonte grande, negrito)
- Delta/variação quando aplicável
- Tooltips explicativos em cada métrica

**Critérios de Aceitação:**
- [ ] Valores calculados automaticamente dos dados
- [ ] Formatação em moeda brasileira (R$)
- [ ] Percentuais com 1 casa decimal
- [ ] Tooltips informativos presentes

---

#### F2: Saldo Disponível por Fonte de Recursos

**Descrição:** Visualização detalhada dos saldos das 5 fontes de recursos

**Fontes de recursos:**
- 500 - Recursos do Tesouro
- 501 - Recursos Tesouro (outras modalidades)
- 753 - Recursos Convênios/Transferências
- 759 - Outros Convênios
- 622 - Recursos Próprios/Outras Fontes

**Componentes:**
1. **Gráfico de barras agrupadas:**
   - Eixo X: Fontes de recursos
   - Eixo Y: Valores em R$
   - 4 barras por fonte: Recursos, Dotado, Empenhado, Saldo
   - Cores diferenciadas para cada categoria
   - Tooltips com valores formatados

2. **Tabela detalhada:**
   - Colunas: Fonte | Recursos | Dotado | Empenhado | Saldo | % Execução
   - Formatação condicional (% execução > 95% = vermelho)
   - Totalizadores na última linha

**Critérios de Aceitação:**
- [ ] Gráfico é interativo (hover, zoom, pan)
- [ ] Saldo calculado corretamente (Recursos - Empenhado)
- [ ] % Execução = (Empenhado / Dotado) × 100
- [ ] Alerta visual para fontes com saldo < 5%
- [ ] Dados da tabela exportáveis

---

#### F3: Comparativo Orçado vs Executado

**Descrição:** Análise comparativa entre o planejado e o executado

**Opções de granularidade:**
- Por **Elemento de Despesa** (Material de Consumo, Permanente, Serviço PJ, Serviço PF)
- Por **Fonte de Recursos** (500, 501, 753, 759, 622)
- Por **Ação do PCA** (ações do planejamento anual)

**Componentes:**
1. **Seletor de granularidade:** Radio buttons horizontais

2. **Gráfico de barras horizontais:**
   - Eixo Y: Categorias (elementos, fontes ou ações)
   - Eixo X: Valores em R$
   - 2 barras lado a lado: Orçado (azul) | Executado (verde)
   - Linha de referência vertical em 100%
   - Destaque visual para sobre-execução (> 100%)

3. **Alertas automáticos:**
   - Card de aviso quando categorias têm execução > 95%
   - Lista expansível com categorias em risco
   - Recomendação de ação (bloquear novos processos nessa categoria)

**Critérios de Aceitação:**
- [ ] Seletor de granularidade funcional
- [ ] Gráfico atualiza automaticamente ao mudar granularidade
- [ ] Alertas só aparecem quando há categorias > 95%
- [ ] Valores ordenados decrescentemente
- [ ] Sobre-execução claramente destacada

---

#### F4: Filtros Globais (Sidebar)

**Descrição:** Painel lateral com filtros que afetam todo o dashboard

**Filtros disponíveis:**
1. **Fontes de Recursos:** Multiselect (500, 501, 753, 759, 622)
2. **Elementos de Despesa:** Multiselect (Consumo, Permanente, Serviço PJ, Serviço PF)
3. **Status:** Multiselect (Empenhado, Reservado, Em análise, Cancelado)

**Comportamento:**
- Valores padrão: todos selecionados
- Aplicação em tempo real (sem botão "Aplicar")
- Atualização de todos os gráficos e tabelas simultaneamente
- Indicador visual de quantos filtros estão ativos

**Critérios de Aceitação:**
- [ ] Filtros persistem durante a sessão
- [ ] Mudanças aplicam em < 1 segundo
- [ ] Todos os gráficos refletem os filtros
- [ ] Possível limpar todos os filtros com 1 clique

---

#### F5: Tabela Detalhada de Despesas

**Descrição:** Tabela completa e pesquisável com todos os processos

**Colunas principais:**
- Processo | Objeto | Fonte | Elemento | Status | Dotado | Empenhado | Saldo | % Exec

**Funcionalidades:**
- **Busca textual:** Campo de busca por processo ou objeto
- **Ordenação:** Clicar no cabeçalho para ordenar
- **Formatação condicional:**
  - Saldo negativo = vermelho
  - % Execução > 95% = amarelo
  - Status "Cancelado" = cinza/riscado
- **Paginação:** 50 linhas por página (performance)
- **Exportação CSV:** Botão de download dos dados filtrados

**Critérios de Aceitação:**
- [ ] Busca funciona em tempo real
- [ ] Ordenação funciona em todas as colunas numéricas
- [ ] Formatação condicional aplicada corretamente
- [ ] CSV exportado mantém filtros aplicados
- [ ] Encoding UTF-8 com BOM para Excel

---

### 3.2 PRIORIDADE 2 - Features Importantes

#### F6: Status de Processos e Empenhos

**Componentes:**
1. **Gráfico de barras empilhadas:**
   - Processos por status (Empenhado, Reservado, Em análise, Cancelado)
   - Valores absolutos e percentuais
   - Cores padronizadas (Verde, Amarelo, Azul, Cinza)

2. **Gráfico de pizza:**
   - Distribuição de recursos empenhados por fonte
   - Interativo com drill-down (se tempo permitir)

**Critérios de Aceitação:**
- [ ] Contagens corretas por status
- [ ] Percentuais somam 100%
- [ ] Legenda clara e posicionada adequadamente

---

#### F7: Execução do PCA 2025

**Descrição:** Acompanhamento das metas do Plano de Contratações Anual

**Componentes:**
- **Bullet chart ou barras horizontais:**
  - Classe/Grupo do PCA no eixo Y
  - % de execução no eixo X
  - Linha de meta (100%)
  - Indicador visual de meta atingida/não atingida

**Dados da aba "PCA 2025":**
- Comparar planejado vs executado por classe
- Calcular % de execução

**Critérios de Aceitação:**
- [ ] Dados do PCA carregados corretamente
- [ ] % execução calculado como (Executado / Planejado) × 100
- [ ] Metas não atingidas destacadas visualmente

---

### 3.3 PRIORIDADE 3 - Features Desejáveis (Pós-MVP)

#### F8: Evolução Temporal
- Gráfico de linha com execução mês a mês
- Requer dados históricos (não disponíveis no Excel atual)

#### F9: Comparativos com Anos Anteriores
- Análise de tendências multi-ano
- Benchmarking com exercícios passados

#### F10: Projeções e Alertas Automáticos
- Projeção de esgotamento de recursos
- Notificações automáticas por email

#### F11: Deploy em Servidor/Nuvem
- Acesso remoto via web
- Autenticação de usuários
- Sincronização automática com Google Sheets

---

## 4. Wireframes e Mockups

### 4.1 Layout Geral do Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 Dashboard de Controle Orçamentário                               │
│ Diretoria de Apoio Logístico - CBMAL | Orçamento 2025              │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐                                                    │
│ │ 🔍 FILTROS   │  ┌────────────────────────────────────────────────┐│
│ │              │  │ 📈 VISÃO GERAL                                 ││
│ │ Fontes:      │  │                                                ││
│ │ ☑ 500        │  │ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ││
│ │ ☑ 501        │  │ │27.28M│ │23.38M│ │ 3.9M │ │ 302  │ │85.7% │ ││
│ │ ☑ 753        │  │ │RECUR.│ │EMPENH│ │SALDO │ │PROCES│ │EXEC. │ ││
│ │ ☑ 759        │  │ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ ││
│ │ ☑ 622        │  └────────────────────────────────────────────────┘│
│ │              │                                                    │
│ │ Elementos:   │  ┌────────────────────────────────────────────────┐│
│ │ ☑ Consumo    │  │ 💰 SALDO POR FONTE                             ││
│ │ ☑ Permanente │  │                                                ││
│ │ ☑ Serv. PJ   │  │  [GRÁFICO DE BARRAS AGRUPADAS]                 ││
│ │ ☑ Serv. PF   │  │                                                ││
│ │              │  │  [TABELA DETALHADA]                            ││
│ │ Status:      │  └────────────────────────────────────────────────┘│
│ │ ☑ Empenhado  │                                                    │
│ │ ☑ Reservado  │  ┌────────────────────────────────────────────────┐│
│ │ ☐ Cancelado  │  │ 📊 ORÇADO vs EXECUTADO                         ││
│ │              │  │                                                ││
│ └──────────────┘  │  ( ) Elemento  (•) Fonte  ( ) Ação PCA        ││
│                   │                                                ││
│                   │  [GRÁFICO DE BARRAS HORIZONTAIS]               ││
│                   │                                                ││
│                   │  ⚠️ 3 categorias com execução acima de 95%    ││
│                   └────────────────────────────────────────────────┘│
│                                                                     │
│  ┌──────────────────────────┐  ┌─────────────────────────────────┐ │
│  │ 📋 STATUS DE PROCESSOS   │  │ 🎯 EXECUÇÃO PCA 2025            │ │
│  │                          │  │                                 │ │
│  │  [GRÁFICO BARRAS EMPILH] │  │  [BULLET CHART / BARRAS HORIZ]  │ │
│  │  [GRÁFICO PIZZA]         │  │                                 │ │
│  └──────────────────────────┘  └─────────────────────────────────┘ │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ 🔎 DETALHAMENTO DE DESPESAS                                     ││
│  │                                                                 ││
│  │  Buscar: [____________]  ⬇️ Baixar CSV                          ││
│  │                                                                 ││
│  │  [TABELA INTERATIVA COM DADOS COMPLETOS]                        ││
│  │                                                                 ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Paleta de Cores

**Cores principais:**
- **Azul primário:** #1f77b4 (Orçado, Recursos, Headers)
- **Verde executado:** #2ca02c (Executado, Empenhado)
- **Amarelo alerta:** #ffbb33 (Alertas, 80-95% execução)
- **Vermelho crítico:** #d62728 (> 95%, Saldo negativo)
- **Cinza neutro:** #7f7f7f (Cancelado, Texto secundário)

**Fontes de recursos (diferenciação):**
- 500: #1f77b4 (Azul)
- 501: #ff7f0e (Laranja)
- 753: #2ca02c (Verde)
- 759: #d62728 (Vermelho)
- 622: #9467bd (Roxo)

---

## 5. Requisitos Técnicos

### 5.1 Performance

| Requisito | Meta | Crítico |
|-----------|------|---------|
| Tempo de carregamento inicial | < 5 segundos | < 10 segundos |
| Resposta a filtros | < 1 segundo | < 2 segundos |
| Renderização de gráficos | < 1 segundo | < 3 segundos |
| Exportação CSV | < 2 segundos | < 5 segundos |
| Tamanho do dataset | 302 linhas (atual) | Até 1000 linhas |

### 5.2 Compatibilidade

- **Python:** 3.9+
- **Navegadores:** Chrome 90+, Firefox 88+, Edge 90+
- **Resolução:** Mínimo 1366x768 (laptop), otimizado para 1920x1080
- **Sistema Operacional:** Windows 10/11 (ambiente CBMAL)

### 5.3 Segurança e Privacidade

- **Dados sensíveis:** Planilha Excel com dados financeiros do CBMAL
- **NÃO** incluir planilha no controle de versão (Git)
- **NÃO** fazer deploy público sem autenticação
- Executar localmente por padrão (localhost:8501)
- Para acesso remoto futuro: implementar autenticação (Streamlit Auth ou OAuth)

### 5.4 Manutenibilidade

- Código modularizado (separação de responsabilidades)
- Docstrings em todas as funções (padrão Google Style)
- Type hints para clareza de parâmetros
- README.md com instruções detalhadas
- Comentários explicativos em lógicas complexas

---

## 6. Métricas de Sucesso

### 6.1 Métricas de Adoção

| Métrica | Baseline (Excel) | Meta (Dashboard) | Como Medir |
|---------|------------------|------------------|------------|
| Tempo para gerar relatório completo | 30-45 minutos | < 5 minutos | Cronometragem comparativa |
| Erros de cálculo por mês | 2-3 (estimado) | 0 | Validação cruzada Excel vs Dashboard |
| Usuários ativos por semana | 1 (analista) | 3-5 (diretor, gestores, analista) | Log de acessos |
| Consultas de saldo por semana | 5-7 (via email/telefone) | 0 (autoatendimento) | Contagem de solicitações |

### 6.2 Métricas de Qualidade

- **Acurácia dos cálculos:** 100% de correspondência com planilha original
- **Disponibilidade:** 99% (falhas apenas por falta de energia/internet)
- **Satisfação do usuário:** NPS > 8 (escala 0-10)

### 6.3 Critérios de Aceitação do MVP

**Checklist de entrega:**
- [ ] Dashboard carrega todas as 12 abas do Excel sem erros
- [ ] 5 KPIs principais calculados corretamente
- [ ] Gráfico de saldo por fonte funcional e interativo
- [ ] Comparativo orçado vs executado implementado
- [ ] Filtros globais funcionam em todos os componentes
- [ ] Tabela detalhada permite busca e ordenação
- [ ] Exportação CSV funciona com encoding correto
- [ ] Performance atende requisitos (< 5s carregamento)
- [ ] Código está documentado (docstrings + README)
- [ ] Validação cruzada de pelo menos 10 valores com Excel

---

## 7. Roadmap e Priorização

### Sprint 1: MVP (Semanas 1-2)
- ✅ Documentação (PRD, MVP, Specs)
- ✅ Setup do projeto (estrutura, dependências)
- ✅ Carregamento e limpeza de dados
- ✅ Processamento e cálculos
- ✅ Visualizações principais (F1-F5)
- ✅ Testes e validação

### Sprint 2: Funcionalidades Secundárias (Semana 3)
- F6: Status de processos
- F7: Execução PCA 2025
- Refinamento de UX/UI
- Documentação de usuário final

### Sprint 3: Melhorias e Expansões (Semana 4+)
- F8: Evolução temporal (se dados disponíveis)
- F9: Comparativos multi-ano
- Otimizações de performance
- Deploy em servidor local (opcional)

### Backlog Futuro (Pós-MVP)
- F10: Projeções e alertas automáticos
- F11: Deploy em nuvem com autenticação
- Integração com Google Sheets API
- App mobile (Streamlit Mobile)

---

## 8. Stakeholders e Comunicação

| Stakeholder | Papel | Interesse | Comunicação |
|-------------|-------|-----------|-------------|
| **Diretor DAL** | Patrocinador | Decisões estratégicas | Demo semanal + relatório final |
| **Gestor Financeiro** | Usuário principal | Acompanhamento operacional | Testes de usabilidade (Sprint 1 e 2) |
| **Analista de Dados** | Usuário técnico + Desenvolvedor | Qualidade dos dados + Aprendizado | Daily updates + pair programming |
| **Diretoria Financeira** | Usuário secundário | Controle institucional | Demo final + treinamento |

---

## 9. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Dados inconsistentes no Excel | Alta | Médio | Implementar validações e logs de erros |
| Mudança na estrutura da planilha | Média | Alto | Criar mapeamento configurável de colunas |
| Performance inadequada com muitos dados | Baixa | Médio | Implementar paginação e lazy loading |
| Resistência à adoção pelos usuários | Média | Alto | Envolver usuários desde o início (testes) |
| Falta de tempo para implementar tudo | Média | Médio | Priorização clara (MVP enxuto) |

---

## 10. Aprovação e Próximos Passos

### Aprovação

Este PRD deve ser revisado e aprovado por:
- [ ] Diretor de Apoio Logístico
- [ ] Gestor Financeiro
- [ ] Analista de Dados (desenvolvedor)

### Próximos Passos

1. **Revisar e aprovar este PRD**
2. **Criar documento de MVP** (docs/03_MVP.md)
3. **Criar especificações técnicas** (docs/04_SPECS_TECNICAS.md)
4. **Iniciar desenvolvimento** (Sprint 1)

---

**Documento elaborado por:** Claude Code
**Revisão:** v1.0 - 11/02/2026
**Status:** 🟡 Aguardando aprovação
