# ✅ Checklist de Validação - Dashboard DAL v2.0 CBMAL

**Versão:** 2.0 CBMAL Edition
**Data:** 11/02/2026
**URL:** http://localhost:8501

---

## 🎯 Objetivo do Teste

Validar se as melhorias aplicadas (paleta CBMAL, checklist C.L.E.A.N., hierarquia KPIs, alertas) estão funcionando corretamente e atendem às expectativas.

---

## 📋 Checklist de Validação

### ✅ SEÇÃO 1: Identidade Visual CBMAL

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 1.1 | Vermelho CBMAL (#DC1B13) aplicado | Verificar cor dos botões, elementos de destaque | ⬜ |  |
| 1.2 | Azul Destaque (#4C7695) nos KPIs | Observar cores dos gráficos e métricas | ⬜ |  |
| 1.3 | Verde Militar (#4B5320) em indicadores OK | Ver barras "Empenhado" nos gráficos | ⬜ |  |
| 1.4 | Tema Streamlit customizado | Verificar fundo cinza claro (#F2F2F2) | ⬜ |  |
| 1.5 | Logo placeholder (🚒) visível | Topo esquerdo do cabeçalho | ⬜ |  |

---

### ✅ SEÇÃO 2: Hierarquia Visual dos KPIs

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 2.1 | **Saldo Disponível** é o KPI principal | Deve ser o MAIOR em tamanho (H1) | ⬜ |  |
| 2.2 | Progress bar de execução visível | Barra azul abaixo do Saldo Disponível | ⬜ |  |
| 2.3 | KPIs em 2 linhas (principal + secundária) | Linha 1: 3 KPIs / Linha 2: 2 KPIs | ⬜ |  |
| 2.4 | Subtítulo "Dados consolidados do orçamento 2025" | Abaixo do título principal | ⬜ |  |
| 2.5 | Taxa de Execução com alerta dinâmico | Se > 95%, deve mostrar "⚠️ Atenção" | ⬜ |  |

**Valores esperados:**
- Saldo Disponível: **R$ 3.899.158,13**
- Total Recursos: **R$ 27.281.568,51**
- Total Empenhado: **R$ 23.382.410,38**
- Processos Ativos: **259**
- Taxa de Execução: **89,4%** (deve mostrar "✅ Normal")

---

### ✅ SEÇÃO 3: Sistema de Alertas Automáticos

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 3.1 | Alerta crítico para Fonte 500 aparece | Card vermelho: "🚨 ALERTA CRÍTICO" | ⬜ |  |
| 3.2 | Fonte 500 mostra execução 99,93% | Dentro do card de alerta | ⬜ |  |
| 3.3 | Ação sugerida: "Bloqueie novos processos" | Texto visível no alerta | ⬜ |  |
| 3.4 | Alerta informativo para Fonte 501 | Card azul: "ℹ️ ATENÇÃO" (0% utilizada) | ⬜ |  |
| 3.5 | Fonte 759 também deve ter alerta | Execução 91,70% (> 90% pode ter alerta) | ⬜ |  |

**Comportamento esperado:**
- 🚨 **2 fontes críticas** (500 e 759 com > 90%)
- ℹ️ **1 fonte não utilizada** (501 com 0%)

---

### ✅ SEÇÃO 4: Títulos Mais Informativos

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 4.1 | "Visão Geral - Indicadores Estratégicos" | Título da seção de KPIs | ⬜ |  |
| 4.2 | "Análise Detalhada: Saldo por Fonte" | Título da seção de gráficos | ⬜ |  |
| 4.3 | Subtítulos explicativos presentes | Texto em itálico abaixo dos títulos | ⬜ |  |
| 4.4 | "Execução Orçamentária: Planejado vs Realizado" | Título do comparativo | ⬜ |  |
| 4.5 | "Base de Dados Completa: Processos e Despesas" | Título da tabela | ⬜ |  |

---

### ✅ SEÇÃO 5: Checklist C.L.E.A.N.

#### C - Contexto (< 5 segundos)

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 5.1 | Identifica problema em < 5s | Cronometrar: abrir dashboard → identificar fontes críticas | ⬜ |  |
| 5.2 | KPIs visíveis sem scroll | Todos os 5 KPIs aparecem sem rolar página | ⬜ |  |
| 5.3 | Alertas no topo, imediatamente após KPIs | Alertas vermelhos logo após progress bar | ⬜ |  |

#### L - Limpeza

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 5.4 | Cores limitadas à paleta CBMAL | Não deve haver cores "aleatórias" | ⬜ |  |
| 5.5 | Fundo neutro (cinza claro) | Sem excesso de elementos visuais | ⬜ |  |
| 5.6 | Sem bordas excessivas | Layout limpo e espaçado | ⬜ |  |

#### E - Ênfase

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 5.7 | Saldo Disponível ocupa ~25% do topo | É o maior elemento visual | ⬜ |  |
| 5.8 | Vermelho CBMAL usado apenas em destaques | Botões, alertas críticos, fonte 501 | ⬜ |  |
| 5.9 | Hierarquia clara (H1 > H2 > H3) | Tamanhos de fonte progressivos | ⬜ |  |

#### A - Acessibilidade

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 5.10 | Texto legível em todos os fundos | Contraste adequado | ⬜ |  |
| 5.11 | Tooltips informativos nos KPIs | Hover sobre métricas mostra explicação | ⬜ |  |
| 5.12 | Legendas nos gráficos | Todos os gráficos têm legenda clara | ⬜ |  |

#### N - Navegação

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 5.13 | Fluxo em "Z" respeitado | Olho segue: topo-esquerda → direita → abaixo-esquerda | ⬜ |  |
| 5.14 | Ações sugeridas visíveis | Alertas mostram o que fazer ("Bloqueie processos") | ⬜ |  |
| 5.15 | Seções bem delimitadas | Divisores entre cada seção | ⬜ |  |

---

### ✅ SEÇÃO 6: Gráficos e Visualizações

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 6.1 | Gráfico "Saldo por Fonte" carrega | Barras agrupadas visíveis | ⬜ |  |
| 6.2 | Cores CBMAL aplicadas no gráfico | Azul, vermelho, verde militar | ⬜ |  |
| 6.3 | Hover mostra valores formatados | Passar mouse sobre barras | ⬜ |  |
| 6.4 | Tabela de saldos formatada | Valores em R$ com 2 casas decimais | ⬜ |  |
| 6.5 | Gráfico "Orçado vs Executado" funcional | Barras horizontais lado a lado | ⬜ |  |
| 6.6 | Cores condicionais no executado | Verde (< 95%), amarelo (95-100%), vermelho (> 100%) | ⬜ |  |
| 6.7 | Alerta aparece se categoria > 95% | Card amarelo expandível | ⬜ |  |

**Valores a validar no gráfico:**
- Fonte 500: Saldo ~R$ 11.810,69 (99,93% executado)
- Fonte 753: Saldo ~R$ 1.458.144,97 (72,28% executado)
- Fonte 759: Saldo ~R$ 331.085,74 (91,70% executado)

---

### ✅ SEÇÃO 7: Funcionalidades Interativas

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 7.1 | Filtro de fontes funciona | Selecionar apenas Fonte 500 → gráficos atualizam | ⬜ |  |
| 7.2 | Filtro de status funciona | Desmarcar "Cancelado" → tabela atualiza | ⬜ |  |
| 7.3 | Botão "Limpar Filtros" funciona | Redefine todos os filtros | ⬜ |  |
| 7.4 | Busca na tabela funciona | Digitar processo → filtra em tempo real | ⬜ |  |
| 7.5 | Download CSV funciona | Baixa arquivo com dados filtrados | ⬜ |  |
| 7.6 | CSV abre corretamente no Excel | Encoding UTF-8-BOM | ⬜ |  |

---

### ✅ SEÇÃO 8: Performance e Estabilidade

| # | Item a Validar | Como Testar | Status | Observações |
|---|---------------|-------------|--------|-------------|
| 8.1 | Carregamento inicial < 5s | Cronometrar do refresh até tudo carregar | ⬜ |  |
| 8.2 | Aplicação de filtros < 1s | Filtrar → cronometrar atualização | ⬜ |  |
| 8.3 | Gráficos renderizam < 1s | Sem lentidão ou travamentos | ⬜ |  |
| 8.4 | Sem erros no console do navegador | F12 → Console → verificar erros | ⬜ |  |
| 8.5 | Valores validados com Excel | KPIs batem com planilha original | ⬜ |  |

---

## 📊 Cenários de Teste Específicos

### Cenário 1: Identificação Rápida de Problema

**Tarefa:** Abra o dashboard e identifique qual fonte está crítica.

**Tempo esperado:** < 5 segundos

**Passos:**
1. Abrir http://localhost:8501
2. Observar alertas vermelhos
3. Identificar Fonte 500 como crítica

**Resultado esperado:**
- ✅ Alerta vermelho visível imediatamente
- ✅ Fonte 500 claramente identificada
- ✅ Ação sugerida visível

---

### Cenário 2: Análise Detalhada de Fonte

**Tarefa:** Verificar saldo da Fonte 753 (Convênios)

**Passos:**
1. Filtrar apenas Fonte 753 na sidebar
2. Observar KPIs atualizados
3. Ver gráfico de saldo

**Resultado esperado:**
- ✅ KPIs mostram apenas dados da Fonte 753
- ✅ Saldo: ~R$ 1.458.144,97
- ✅ Execução: 72,28%
- ✅ Gráfico atualizado

---

### Cenário 3: Exportação de Dados

**Tarefa:** Exportar processos empenhados

**Passos:**
1. Filtrar Status: apenas "Empenhado"
2. Clicar em "⬇️ Baixar CSV"
3. Abrir CSV no Excel

**Resultado esperado:**
- ✅ CSV baixado com sucesso
- ✅ 214 linhas (processos empenhados)
- ✅ Abre corretamente no Excel (sem caracteres estranhos)

---

## 🎯 Critérios de Aprovação

### Aprovação Mínima (70%)

- [ ] **18/25** itens da Seção 1-5 validados
- [ ] **5/7** itens da Seção 6 validados
- [ ] **4/6** itens da Seção 7 validados
- [ ] **3/5** itens da Seção 8 validados

### Aprovação Ideal (90%+)

- [ ] **23/25** itens da Seção 1-5 validados
- [ ] **6/7** itens da Seção 6 validados
- [ ] **5/6** itens da Seção 7 validados
- [ ] **4/5** itens da Seção 8 validados

---

## 📝 Registro de Problemas Encontrados

Use esta seção para anotar qualquer problema encontrado durante o teste:

| # | Problema | Gravidade | Seção | Observação |
|---|----------|-----------|-------|------------|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |

**Gravidade:**
- 🔴 **Crítico:** Impede uso do dashboard
- 🟡 **Médio:** Funciona mas prejudica experiência
- 🟢 **Baixo:** Melhoria cosmética

---

## ✅ Resultado Final

**Data do teste:** ___/___/______

**Testado por:** _________________

**Aprovação:**
- ⬜ ✅ Aprovado (≥ 90%)
- ⬜ ⚠️ Aprovado com ressalvas (70-89%)
- ⬜ ❌ Reprovado (< 70%)

**Comentários gerais:**

---

**Próximos passos após aprovação:**
1. Substituir emoji 🚒 por logo oficial CBMAL
2. Planejar módulo SAC
3. Adicionar gráficos de status de processos (v2.1)
4. Implementar dark mode (v2.2)
