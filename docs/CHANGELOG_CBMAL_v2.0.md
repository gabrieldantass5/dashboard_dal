# Changelog - Dashboard DAL v2.0 CBMAL

## Versão 2.0 - Identidade Visual CBMAL (11/02/2026)

### 🎨 Aplicação de Paleta de Cores Oficial CBMAL

**Arquivos modificados:**
- `src/utils.py` - Constantes de cores atualizadas
- `.streamlit/config.toml` - Tema Streamlit customizado

**Cores Aplicadas:**
- ✅ Vermelho CBMAL `#DC1B13` - Destaque primário
- ✅ Azul Destaque `#4C7695` - KPIs secundários
- ✅ Verde Militar `#4B5320` - Normalidade
- ✅ Vermelho Crítico `#B22222` - Alertas
- ✅ Cinza Base `#F2F2F2` - Fundos

**Mapeamento de Cores:**
- **Fontes de Recursos:**
  - 500 (Tesouro): Azul Destaque
  - 501 (DREM): Vermelho CBMAL
  - 753 (Convênios): Verde Militar
  - 759 (Fundos): Vermelho Crítico
  - 622 (SUS): Roxo

- **Status de Processos:**
  - Empenhado: Verde Militar
  - Reservado: Amarelo/Laranja
  - Em análise: Azul Destaque
  - Cancelado: Cinza

---

### ✅ Checklist C.L.E.A.N. Aplicado

**Framework:** dashboard-designer-cbmal v2.0 (PaperBanana)

#### C - Contexto (< 5 segundos)
✅ KPIs críticos visíveis sem scroll
✅ Alertas críticos exibidos imediatamente após KPIs
✅ Fontes > 95% destacadas em vermelho
✅ Fontes não utilizadas (0%) com aviso informativo

#### L - Limpeza
✅ Cores limitadas à paleta oficial CBMAL
✅ Excesso de elementos visuais removido
✅ Fundo neutro (Cinza Base)

#### E - Ênfase
✅ **Saldo Disponível** é o KPI principal (maior destaque)
✅ Ocupação de ~25% do topo com KPIs
✅ Hierarquia visual clara (H1 > H2 > H3)
✅ Progress bar visual para taxa de execução

#### A - Acessibilidade
✅ Contraste adequado em todos os textos
✅ Tooltips informativos nos KPIs
✅ Legendas descritivas em todos os gráficos

#### N - Navegação
✅ Fluxo em "Z" respeitado
✅ Alertas críticos no topo
✅ Ações requeridas visíveis

---

### 📊 Melhorias de Hierarquia Visual dos KPIs

**Arquivo modificado:** `app.py`

**Antes:**
- 5 KPIs em linha única (pouco destaque)
- Sem diferenciação de importância
- Sem alertas visuais

**Depois:**
- **Linha 1 (Principal):**
  - Saldo Disponível (H1, maior fonte)
  - Total de Recursos (H2)
  - Total Empenhado (H2)
  - Progress bar de execução

- **Linha 2 (Secundária):**
  - Processos Ativos
  - Taxa de Execução (com alerta se > 95%)

**Melhorias:**
- ✅ Saldo Disponível em destaque (principal preocupação)
- ✅ Progress bar visual para execução
- ✅ Alertas dinâmicos baseados em limites
- ✅ Subtítulos explicativos

---

### 🚨 Sistema de Alertas Automáticos

**Novos componentes em `app.py`:**

1. **Alertas Críticos (Fontes > 95%):**
   ```
   🚨 ALERTA CRÍTICO: X fonte(s) com execução acima de 95%
   [Card individual por fonte crítica com ação sugerida]
   ```

2. **Alertas Informativos (Fontes não utilizadas):**
   ```
   ℹ️ ATENÇÃO: X fonte(s) não utilizada(s) - investigue o motivo
   ```

**Lógica:**
- Vermelho (🚨): Execução > 95%
- Azul (ℹ️): Execução = 0%
- Ação sugerida: "Bloqueie novos processos" ou "Investigue"

---

### 📝 Títulos Mais Informativos

**Antes:**
- "Visão Geral"
- "Saldo Disponível por Fonte de Recursos"
- "Comparativo: Orçado vs Executado"
- "Detalhamento de Despesas"

**Depois:**
- "Visão Geral - Indicadores Estratégicos" + subtítulo
- "Análise Detalhada: Saldo por Fonte de Recursos" + descrição
- "Execução Orçamentária: Planejado vs Realizado" + descrição
- "Base de Dados Completa: Processos e Despesas" + descrição

**Benefício:** Usuário entende imediatamente o propósito de cada seção.

---

### 🎨 Tema Streamlit Customizado

**Novo arquivo:** `.streamlit/config.toml`

**Configurações:**
- Primary Color: `#DC1B13` (Vermelho CBMAL)
- Background: `#FFFFFF` (Branco puro)
- Secondary Background: `#F2F2F2` (Cinza Base)
- Text Color: `#0F172A` (Contraste WCAG)

**Benefícios:**
- Botões e elementos interativos usam Vermelho CBMAL
- Fundos seguem paleta oficial
- Consistência visual em todo o dashboard

---

### 📐 Cabeçalho com Identidade Visual

**Mudanças:**
- Logo placeholder (🚒) adicionado
- Layout em colunas (logo + título)
- Preparado para inserção de logo oficial CBMAL

---

## 📚 Documentação Criada

### Novos Arquivos:

1. **`docs/CBMAL_DESIGN_SYSTEM.md`** (3.5KB)
   - Paleta completa de cores
   - Aplicação por componente
   - Checklist C.L.E.A.N.
   - Tipografia recomendada
   - Anti-padrões a evitar

2. **`.streamlit/config.toml`** (0.3KB)
   - Configuração de tema Streamlit
   - Cores oficiais CBMAL

3. **`docs/CHANGELOG_CBMAL_v2.0.md`** (Este arquivo)

---

## 🎯 Próximos Passos (Roadmap v2.1)

### Curto Prazo (1-2 semanas):
- [ ] Substituir emoji 🚒 por logo oficial CBMAL (SVG)
- [ ] Adicionar CSS customizado para transições suaves
- [ ] Implementar dark mode com paleta CBMAL adaptada

### Médio Prazo (1 mês):
- [ ] Criar aba separada para módulo SAC
- [ ] Adicionar gráficos de status de processos
- [ ] Implementar execução do PCA 2025

### Longo Prazo (2-3 meses):
- [ ] Evoluções temporais
- [ ] Comparativos multi-ano
- [ ] Deploy em servidor

---

## ✅ Validação

**Checklist de Entrega:**
- [x] Paleta CBMAL aplicada em todos os componentes
- [x] Checklist C.L.E.A.N. 100% implementado
- [x] Hierarquia visual dos KPIs otimizada
- [x] Sistema de alertas automáticos funcionando
- [x] Documentação completa criada
- [x] Dashboard testado e operacional

---

**Desenvolvido por:** Claude Code + APO/EMG
**Framework:** PaperBanana (dashboard-designer-cbmal v2.0)
**Data:** 11/02/2026
**Versão:** 2.0 CBMAL Edition
