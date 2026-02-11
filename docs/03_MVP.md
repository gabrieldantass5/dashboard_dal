# MVP - Minimum Viable Product
## Dashboard de Controle Orçamentário DAL/CBMAL

**Versão:** 1.0
**Data:** 11/02/2026
**Objetivo:** Definir o escopo mínimo viável para a primeira versão do dashboard

---

## 1. Visão do MVP

### 1.1 Definição

O **MVP (Produto Mínimo Viável)** do Dashboard Orçamentário é a versão mais simples do produto que:
- Resolve os problemas mais críticos dos usuários
- Pode ser desenvolvido em 2-3 dias de trabalho focado
- Entrega valor imediato e mensurável
- Serve como base para iterações futuras

### 1.2 Princípio Norteador

> **"Melhor um dashboard simples funcionando hoje do que um dashboard completo daqui a 1 mês"**

Foco em:
- ✅ **Funcionalidades essenciais** que atendem 80% das necessidades
- ✅ **Qualidade sobre quantidade** - poucas funcionalidades bem feitas
- ✅ **Dados corretos** - validação rigorosa dos cálculos
- ✅ **Facilidade de uso** - interface intuitiva sem necessidade de treinamento

---

## 2. Funcionalidades do MVP

### 2.1 INCLUÍDO NO MVP ✅

#### MVP-F1: Painel de KPIs Principais (CRÍTICO)

**O que faz:**
- Exibe 5 métricas principais no topo do dashboard
- Valores atualizados automaticamente dos dados do Excel

**Métricas:**
1. Total de Recursos
2. Total Empenhado
3. Saldo Disponível
4. Processos Ativos
5. Taxa de Execução

**Critérios de aceitação:**
- [ ] Valores calculados corretamente (validar com Excel)
- [ ] Formatação em moeda brasileira (R$)
- [ ] Tooltips explicativos presentes

**Estimativa:** 2-3 horas

---

#### MVP-F2: Saldo Disponível por Fonte de Recursos (CRÍTICO)

**O que faz:**
- Gráfico de barras mostrando saldo de cada fonte
- Tabela com detalhamento numérico

**Componentes:**
- Gráfico de barras agrupadas (Recursos, Dotado, Empenhado, Saldo)
- Tabela com 5 linhas (uma por fonte) + linha de total

**Critérios de aceitação:**
- [ ] Gráfico interativo (hover mostra valores)
- [ ] Cálculo correto: Saldo = Recursos - Empenhado
- [ ] % Execução = (Empenhado / Dotado) × 100
- [ ] Cores diferenciadas por fonte

**Estimativa:** 3-4 horas

---

#### MVP-F3: Comparativo Orçado vs Executado (CRÍTICO)

**O que faz:**
- Compara planejado vs executado em formato visual

**Versão MVP (simplificada):**
- Granularidade fixa: **Por Elemento de Despesa**
- Gráfico de barras horizontais lado a lado
- Alerta quando categorias > 95% de execução

**Critérios de aceitação:**
- [ ] Gráfico mostra orçado e executado lado a lado
- [ ] Alerta visual quando execução > 95%
- [ ] Ordenação decrescente por valor executado

**Estimativa:** 3-4 horas

**Nota:** Seletor de granularidade (Fonte, PCA) fica para versão 2.0

---

#### MVP-F4: Filtros Globais (IMPORTANTE)

**O que faz:**
- Sidebar com filtros que afetam todas as visualizações

**Filtros MVP:**
1. **Fontes de Recursos:** Multiselect (500, 501, 753, 759, 622)
2. **Status:** Multiselect (Empenhado, Reservado, Cancelado)

**Critérios de aceitação:**
- [ ] Filtros aplicam em todos os gráficos e tabelas
- [ ] Resposta em < 1 segundo
- [ ] Valores padrão: todos selecionados

**Estimativa:** 2-3 horas

**Nota:** Filtro por "Elemento de Despesa" fica para v2.0

---

#### MVP-F5: Tabela Detalhada de Despesas (IMPORTANTE)

**O que faz:**
- Tabela completa com todos os processos
- Busca por processo ou objeto
- Exportação CSV

**Colunas MVP:**
- Processo | Objeto | Fonte | Elemento | Status | Empenhado | % Exec

**Funcionalidades:**
- Campo de busca textual
- Ordenação ao clicar no cabeçalho
- Botão de download CSV

**Critérios de aceitação:**
- [ ] Busca funciona em tempo real
- [ ] CSV exporta com encoding UTF-8-BOM
- [ ] Paginação se > 100 linhas

**Estimativa:** 3-4 horas

**Nota:** Formatação condicional (cores) fica para v2.0

---

### 2.2 FORA DO MVP ❌ (Roadmap Futuro)

#### Post-MVP 1: Granularidades Adicionais
- Comparativo orçado vs executado por **Fonte de Recursos**
- Comparativo orçado vs executado por **Ação do PCA**
- **Motivo:** Requer processamento adicional, não é crítico para v1.0
- **Previsão:** Versão 2.0 (Semana 3)

#### Post-MVP 2: Status de Processos (Gráficos)
- Gráfico de barras empilhadas (status)
- Gráfico de pizza (distribuição por fonte)
- **Motivo:** Informação já disponível na tabela, não é crítico
- **Previsão:** Versão 2.0 (Semana 3)

#### Post-MVP 3: Execução do PCA 2025
- Bullet chart com % de execução por classe/grupo
- **Motivo:** Dados do PCA precisam de análise prévia, complexidade média
- **Previsão:** Versão 2.0 (Semana 3)

#### Post-MVP 4: Filtro por Elemento de Despesa
- Adicionar 3º filtro na sidebar
- **Motivo:** Não é crítico para análise inicial, pode ser adicionado facilmente
- **Previsão:** Versão 1.1 (Semana 2)

#### Post-MVP 5: Formatação Condicional Avançada
- Cores na tabela (vermelho para saldo negativo, amarelo para > 95%)
- Ícones de alerta
- **Motivo:** "Nice to have", não afeta funcionalidade
- **Previsão:** Versão 1.1 (Semana 2)

#### Post-MVP 6: Evolução Temporal
- Gráfico de linha com execução mês a mês
- **Motivo:** Dados históricos não disponíveis no Excel atual
- **Previsão:** Versão 3.0 (após integração com Google Sheets)

#### Post-MVP 7: Comparativos com Anos Anteriores
- Análise multi-ano
- **Motivo:** Requer dados de 2024, 2023, etc.
- **Previsão:** Versão 3.0

#### Post-MVP 8: Projeções e Alertas Automáticos
- Projeção de esgotamento de recursos
- Notificações por email
- **Motivo:** Requer algoritmos de ML/estatística, complexo
- **Previsão:** Versão 4.0 (pós-MVP, após aprendizado avançado)

#### Post-MVP 9: Deploy em Servidor/Nuvem
- Acesso remoto via web
- Autenticação de usuários
- **Motivo:** Requer infraestrutura, não é necessário para uso local
- **Previsão:** Versão 5.0 (após aprovação da direção)

#### Post-MVP 10: Integração com Google Sheets API
- Atualização automática de dados
- **Motivo:** Requer migração de Excel para Google Sheets, processo organizacional
- **Previsão:** Versão 5.0

---

## 3. Escopo Técnico do MVP

### 3.1 Arquivos a Desenvolver

| Arquivo | Responsabilidade | Linhas (est.) | Prioridade |
|---------|------------------|---------------|-----------|
| `requirements.txt` | Dependências Python | 5 | MVP |
| `.gitignore` | Arquivos a ignorar | 10 | MVP |
| `README.md` | Documentação de uso | 80 | MVP |
| `CLAUDE.md` | Guia para Claude Code | 60 | MVP |
| `src/data_loader.py` | Carregamento de dados | 100 | MVP |
| `src/data_processor.py` | Processamento e cálculos | 120 | MVP |
| `src/visualizations.py` | Gráficos Plotly | 150 | MVP |
| `src/utils.py` | Utilidades e formatação | 50 | MVP |
| `app.py` | Aplicação Streamlit | 200 | MVP |
| **TOTAL** | | **~775 linhas** | |

### 3.2 Funcionalidades por Módulo

#### `data_loader.py` (MVP)
- ✅ `load_excel_data()`: Carregar Excel completo
- ✅ `clean_despesas()`: Limpar aba CONTROLE DE DESPESAS
- ✅ `clean_balanco()`: Processar aba BALANCO
- ❌ `clean_pca()`: Processar PCA 2025 (Post-MVP)
- ❌ `clean_despesas_recorrentes()`: Processar Despesas 2025 (Post-MVP)

#### `data_processor.py` (MVP)
- ✅ `calcular_saldos_por_fonte()`: Saldos e % execução
- ✅ `calcular_orcado_vs_executado()`: Comparativo por elemento
- ✅ `gerar_metricas_kpi()`: 5 KPIs principais
- ❌ `processar_status_processos()`: Contagem por status (Post-MVP)
- ❌ `calcular_execucao_pca()`: % execução PCA (Post-MVP)

#### `visualizations.py` (MVP)
- ✅ `grafico_saldo_por_fonte()`: Barras agrupadas
- ✅ `grafico_orcado_vs_executado()`: Barras horizontais
- ✅ `tabela_interativa_despesas()`: Tabela Streamlit
- ❌ `grafico_pizza_distribuicao()`: Pizza (Post-MVP)
- ❌ `grafico_status_processos()`: Barras empilhadas (Post-MVP)
- ❌ `grafico_execucao_pca()`: Bullet chart (Post-MVP)
- ❌ `grafico_execucao_temporal()`: Linha temporal (Post-MVP)

#### `utils.py` (MVP)
- ✅ `formatar_moeda()`: Formatação R$
- ✅ `formatar_percentual()`: Formatação %
- ✅ `aplicar_filtros()`: Aplicar filtros ao DataFrame
- ✅ Constantes: `CORES_PADRAO`, `FONTES_RECURSOS`

#### `app.py` (MVP - Interface)
- ✅ Configuração da página
- ✅ Sidebar com 2 filtros (Fontes, Status)
- ✅ Seção: KPIs principais
- ✅ Seção: Saldo por fonte
- ✅ Seção: Orçado vs executado
- ✅ Seção: Tabela detalhada
- ❌ Seção: Status de processos (Post-MVP)
- ❌ Seção: Execução PCA (Post-MVP)

---

## 4. Timeline de Desenvolvimento

### Fase 1: Documentação ✅ (Concluída)
- **Duração:** 2-3 horas
- **Entregáveis:**
  - ✅ docs/01_BRIEFING.md
  - ✅ docs/02_PRD.md
  - ✅ docs/03_MVP.md (este documento)
  - 🔄 docs/04_SPECS_TECNICAS.md (em andamento)

---

### Fase 2: Setup e Estrutura (Próxima)
- **Duração:** 1 hora
- **Atividades:**
  1. Criar `requirements.txt`
  2. Criar `.gitignore`
  3. Criar estrutura de pastas `src/` e `data/`
  4. Criar `README.md` básico
  5. Criar `CLAUDE.md`
  6. Inicializar ambiente virtual e instalar dependências

**Critérios de conclusão:**
- [ ] Comando `pip install -r requirements.txt` funciona
- [ ] Estrutura de pastas criada
- [ ] Git configurado (se aplicável)

---

### Fase 3: Backend - Carregamento de Dados
- **Duração:** 2-3 horas
- **Atividades:**
  1. Implementar `load_excel_data()`
  2. Implementar `clean_despesas()`
  3. Implementar `clean_balanco()`
  4. Testar carregamento das 2 abas principais
  5. Validar dados carregados (print/log)

**Critérios de conclusão:**
- [ ] Excel carrega sem erros
- [ ] DataFrames têm colunas corretas e tipos de dados adequados
- [ ] Dados nulos/inconsistentes tratados

---

### Fase 4: Backend - Processamento
- **Duração:** 2-3 horas
- **Atividades:**
  1. Implementar `calcular_saldos_por_fonte()`
  2. Implementar `gerar_metricas_kpi()`
  3. Implementar `calcular_orcado_vs_executado()`
  4. Implementar `utils.py` (formatações)
  5. Validar cálculos com Excel (comparação manual)

**Critérios de conclusão:**
- [ ] Saldos calculados corretamente (comparar com Excel)
- [ ] KPIs corretos (Total Recursos = ~R$ 27.281.568,51)
- [ ] Funções de formatação funcionam

---

### Fase 5: Frontend - Visualizações
- **Duração:** 3-4 horas
- **Atividades:**
  1. Implementar `grafico_saldo_por_fonte()`
  2. Implementar `grafico_orcado_vs_executado()`
  3. Implementar `tabela_interativa_despesas()`
  4. Testar gráficos individualmente (Jupyter/script)

**Critérios de conclusão:**
- [ ] Gráficos são interativos (hover funciona)
- [ ] Cores aplicadas corretamente
- [ ] Tabela exibe dados corretos

---

### Fase 6: Frontend - Interface Streamlit
- **Duração:** 3-4 horas
- **Atividades:**
  1. Configurar `app.py` (cabeçalho, layout)
  2. Implementar sidebar com filtros
  3. Implementar seção de KPIs
  4. Implementar seção de saldo por fonte
  5. Implementar seção de orçado vs executado
  6. Implementar tabela detalhada com busca
  7. Implementar exportação CSV
  8. Conectar filtros aos gráficos

**Critérios de conclusão:**
- [ ] Dashboard carrega em `streamlit run app.py`
- [ ] Filtros funcionam em todas as seções
- [ ] Exportação CSV funciona

---

### Fase 7: Testes e Validação
- **Duração:** 2-3 horas
- **Atividades:**
  1. Teste de funcionalidade (todos os componentes)
  2. Validação de dados (10+ valores vs Excel)
  3. Teste de performance (carregamento < 5s)
  4. Teste de filtros (combinações diversas)
  5. Teste de busca e ordenação
  6. Ajustes de UX/UI
  7. Documentação final (README, docstrings)

**Critérios de conclusão:**
- [ ] Checklist de aceitação 100% concluído (ver seção 7)
- [ ] Performance atende requisitos
- [ ] Código documentado

---

### Fase 8: Entrega e Treinamento
- **Duração:** 1-2 horas
- **Atividades:**
  1. Demo para usuários (Diretor, Gestor, Analista)
  2. Treinamento básico (como usar filtros, exportar CSV)
  3. Coleta de feedback inicial
  4. Ajustes rápidos se necessário
  5. Entrega oficial

**Critérios de conclusão:**
- [ ] Usuários conseguem usar o dashboard sem ajuda
- [ ] Feedback documentado para v2.0

---

### Resumo do Timeline

| Fase | Duração | Status |
|------|---------|--------|
| 1. Documentação | 2-3h | ✅ Concluída |
| 2. Setup | 1h | ⏳ Próxima |
| 3. Backend - Dados | 2-3h | ⏳ Pendente |
| 4. Backend - Processamento | 2-3h | ⏳ Pendente |
| 5. Frontend - Visualizações | 3-4h | ⏳ Pendente |
| 6. Frontend - Streamlit | 3-4h | ⏳ Pendente |
| 7. Testes | 2-3h | ⏳ Pendente |
| 8. Entrega | 1-2h | ⏳ Pendente |
| **TOTAL MVP** | **16-23h** | **~2-3 dias** |

---

## 5. Dados Necessários

### 5.1 Abas do Excel Utilizadas no MVP

| Aba | Utilização MVP | Campos Críticos |
|-----|----------------|----------------|
| **CONTROLE DE DESPESAS** | ✅ SIM | Processo, Objeto, Fonte, Elemento, Status, Dotado, Empenhado |
| **BALANCO** | ✅ SIM | Fonte, Recursos, Dotado, Empenhado |
| RECURSOS TESOURO 2025 | ❌ NÃO (v2.0) | - |
| PCA 2025 | ❌ NÃO (v2.0) | - |
| Despesas 2025 | ❌ NÃO (v2.0) | - |
| Outras (7 abas) | ❌ NÃO (futuro) | - |

**Apenas 2 abas são necessárias para o MVP!**

### 5.2 Transformações de Dados

**CONTROLE DE DESPESAS:**
- Remover linhas completamente vazias
- Renomear colunas "Unnamed: X" → nomes descritivos
- Converter colunas de valor para `float`
- Converter datas para `datetime`
- Preencher valores nulos em "Status" com "Em análise"

**BALANCO:**
- Extrair linhas específicas: "RECURSOS", "DOTADO", "EMPENHADO"
- Transpor dados (fontes como colunas → fontes como linhas)
- Calcular coluna "Saldo" = Recursos - Empenhado
- Calcular coluna "% Execução" = (Empenhado / Dotado) × 100

---

## 6. Critérios de Aceitação do MVP

### 6.1 Checklist Funcional

**Carregamento de Dados:**
- [ ] Excel abre sem erros
- [ ] Aba "CONTROLE DE DESPESAS" carrega corretamente
- [ ] Aba "BALANCO" carrega corretamente
- [ ] Dados nulos/inconsistentes são tratados

**KPIs Principais:**
- [ ] Total de Recursos = R$ 27.281.568,51 (±0,01)
- [ ] Total Empenhado = R$ 23.382.410,38 (±0,01)
- [ ] Saldo Disponível calculado corretamente
- [ ] Processos Ativos = 302 (ou número correto)
- [ ] Taxa de Execução calculada corretamente

**Saldo por Fonte:**
- [ ] Gráfico mostra 5 fontes (500, 501, 753, 759, 622)
- [ ] Barras agrupadas (Recursos, Dotado, Empenhado, Saldo)
- [ ] Hover mostra valores formatados em R$
- [ ] Tabela exibe dados corretos
- [ ] % Execução por fonte está correto

**Orçado vs Executado:**
- [ ] Gráfico compara orçado e executado por elemento
- [ ] Barras horizontais lado a lado
- [ ] Ordenação decrescente por valor executado
- [ ] Alerta aparece quando categoria > 95%

**Filtros:**
- [ ] Filtro de fontes funciona (multiselect)
- [ ] Filtro de status funciona (multiselect)
- [ ] Todos os gráficos atualizam ao aplicar filtros
- [ ] Resposta em < 1 segundo

**Tabela Detalhada:**
- [ ] Exibe todos os processos (ou filtrados)
- [ ] Busca por processo funciona
- [ ] Busca por objeto funciona
- [ ] Ordenação ao clicar no cabeçalho funciona
- [ ] Download CSV funciona
- [ ] CSV abre corretamente no Excel (encoding UTF-8-BOM)

**Performance:**
- [ ] Carregamento inicial < 5 segundos
- [ ] Aplicação de filtros < 1 segundo
- [ ] Gráficos renderizam < 1 segundo

**Documentação:**
- [ ] README.md tem instruções de instalação
- [ ] README.md tem instruções de execução
- [ ] Código tem docstrings nas funções principais
- [ ] CLAUDE.md criado

---

### 6.2 Checklist de Validação de Dados

**Validar manualmente os seguintes valores comparando Dashboard vs Excel:**

1. [ ] Total de Recursos (BALANCO)
2. [ ] Total Empenhado (BALANCO)
3. [ ] Saldo da Fonte 500
4. [ ] Saldo da Fonte 753
5. [ ] % Execução da Fonte 500
6. [ ] Total orçado para "Material de Consumo"
7. [ ] Total executado para "Material de Consumo"
8. [ ] Número de processos com status "Empenhado"
9. [ ] Valor do processo XXX (escolher 1 aleatório)
10. [ ] Número total de linhas na tabela

**Critério:** 10/10 valores devem bater exatamente (ou diferença < R$ 0,10 por arredondamento)

---

## 7. Roadmap Pós-MVP

### Versão 1.1 (Semana 2)
- Adicionar filtro por "Elemento de Despesa"
- Implementar formatação condicional na tabela (cores)
- Melhorias de UX (tooltips adicionais, legendas)
- Otimizações de performance (cache aprimorado)

### Versão 2.0 (Semana 3)
- Implementar gráficos de status de processos
- Implementar execução do PCA 2025
- Adicionar granularidades ao comparativo (Fonte, PCA)
- Implementar gráfico de pizza (distribuição)

### Versão 3.0 (Semana 4+)
- Evolução temporal (se dados disponíveis)
- Comparativos com anos anteriores
- Projeções de execução
- Alertas automáticos por email

### Versão 4.0+ (Futuro)
- Deploy em servidor local/nuvem
- Autenticação de usuários
- Integração com Google Sheets API
- App mobile

---

## 8. Riscos Específicos do MVP

| Risco | Probabilidade | Impacto | Mitigação MVP |
|-------|---------------|---------|---------------|
| Dados do Excel mudarem de estrutura | Média | Alto | Criar validação que alerta se colunas mudarem |
| Performance insuficiente com 302 linhas | Baixa | Médio | Implementar cache agressivo (@st.cache_data) |
| Valores não batem com Excel | Baixa | Crítico | Validação rigorosa (10 valores) antes de entregar |
| Usuários não conseguirem instalar Python | Média | Alto | README.md com instruções passo a passo + screenshots |
| Resistência ao uso do dashboard | Média | Alto | Envolver usuários nos testes (Fase 7) |

---

## 9. Definição de "Pronto" (Definition of Done)

Uma funcionalidade está **pronta** quando:

1. ✅ Código implementado e funcional
2. ✅ Testada manualmente (casos felizes e edge cases)
3. ✅ Validada com dados reais do Excel
4. ✅ Docstrings adicionadas nas funções
5. ✅ Performance atende requisitos (< 1s resposta)
6. ✅ Funciona com filtros aplicados
7. ✅ Revisada por desenvolvedor (self-review)
8. ✅ Demonstrada a pelo menos 1 usuário real
9. ✅ Feedback incorporado (se houver)
10. ✅ Documentada no README (se for feature visível ao usuário)

---

## 10. Métricas de Sucesso do MVP

### 10.1 Métricas Quantitativas

| Métrica | Meta MVP | Como Medir |
|---------|----------|------------|
| Tempo de carregamento | < 5 segundos | Cronômetro (F12 → Network) |
| Tempo de resposta de filtros | < 1 segundo | Cronômetro manual |
| Acurácia de cálculos | 100% (10/10 valores corretos) | Validação cruzada Excel |
| Linhas de código | ~775 linhas | `wc -l src/*.py app.py` |
| Tempo de desenvolvimento | < 23 horas | Log de horas trabalhadas |

### 10.2 Métricas Qualitativas

| Métrica | Meta MVP | Como Medir |
|---------|----------|------------|
| Facilidade de uso | Usuários conseguem usar sem treinamento | Teste de usabilidade (observação) |
| Clareza das visualizações | Insights identificados em < 30s | Teste com tarefas ("Qual fonte tem maior saldo?") |
| Satisfação do usuário | "Isso vai me economizar muito tempo!" | Entrevista pós-demo |
| Aprendizado (para analista) | "Entendi como funciona Streamlit e Plotly" | Auto-avaliação |

---

## 11. Próximos Passos

### Ações Imediatas

1. ✅ Revisar e aprovar este documento de MVP
2. ⏳ Criar `docs/04_SPECS_TECNICAS.md` (especificações técnicas detalhadas)
3. ⏳ Iniciar **Fase 2 - Setup e Estrutura**
   - Criar `requirements.txt`
   - Criar `.gitignore`
   - Criar estrutura de pastas
   - Criar `README.md` e `CLAUDE.md`

### Checkpoint de Aprovação

Antes de iniciar o desenvolvimento (Fase 3), validar:
- [ ] MVP está claro e alinhado com expectativas
- [ ] Funcionalidades FORA do MVP estão acordadas
- [ ] Timeline é realista (2-3 dias)
- [ ] Recursos necessários disponíveis (Python instalado, acesso ao Excel)

---

**Documento elaborado por:** Claude Code
**Revisão:** v1.0 - 11/02/2026
**Status:** 🟡 Aguardando aprovação

---

## Apêndice: Comparação MVP vs Full

| Funcionalidade | MVP v1.0 | Full (v2.0+) |
|----------------|----------|--------------|
| KPIs principais | ✅ 5 KPIs | ✅ 5 KPIs + tendências |
| Saldo por fonte | ✅ Gráfico + tabela | ✅ + Drill-down interativo |
| Orçado vs executado | ✅ Por elemento apenas | ✅ Por elemento, fonte e PCA |
| Filtros | ✅ 2 filtros (Fonte, Status) | ✅ 3+ filtros (+ Elemento, + Período) |
| Tabela de despesas | ✅ Busca + ordenação | ✅ + Formatação condicional |
| Status de processos | ❌ Não | ✅ Gráfico barras + pizza |
| Execução PCA | ❌ Não | ✅ Bullet chart |
| Evolução temporal | ❌ Não | ✅ Gráfico de linha |
| Comparativo anos | ❌ Não | ✅ Análise multi-ano |
| Exportação | ✅ CSV | ✅ CSV + PDF + Excel |
| Deploy | ❌ Apenas local | ✅ Servidor/nuvem |
| Autenticação | ❌ Não | ✅ Login seguro |
| API integração | ❌ Não | ✅ Google Sheets API |
| **Linhas de código** | ~775 | ~1500+ |
| **Tempo de dev** | 16-23h | 40-60h |
