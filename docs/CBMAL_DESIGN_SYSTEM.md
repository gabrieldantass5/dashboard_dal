# CBMAL Design System v2.0
## Paleta de Cores Oficial - Dashboard DAL

**Baseado em:** skill `dashboard-designer-cbmal` v2.0
**Data de Aplicação:** 11/02/2026
**Fonte:** Dados empíricos extraídos pela APO/EMG

---

## 🎨 Paleta Principal

### Cores Primárias CBMAL

| Uso | Nome | HEX | RGB | Quando Usar |
|-----|------|-----|-----|-------------|
| **Destaque Primário** | Vermelho CBMAL | `#DC1B13` | `220, 27, 19` | Identidade visual, elementos de marca, CTAs principais |
| **KPI Secundário** | Azul Destaque | `#4C7695` | `76, 118, 149` | KPIs secundários, dados informativos, fundo de elementos |
| **Normalidade/OK** | Verde Militar | `#4B5320` | `75, 83, 32` | Indicadores positivos, processos normais, status OK |
| **Alertas Críticos** | Vermelho Crítico | `#B22222` | `178, 34, 34` | Alertas > 95%, situações críticas, avisos urgentes |
| **Base/Fundo** | Cinza Base | `#F2F2F2` | `242, 242, 242` | Fundos, agrupamentos, contraste sutil |

### Cores Secundárias (Alertas)

| Uso | Nome | HEX | Observação |
|-----|------|-----|------------|
| **Alertas Moderados** | Amarelo/Laranja | `#FFA500` | Execução entre 80-95%, atenção moderada |
| **Textos Secundários** | Cinza Médio | `#7f7f7f` | Textos de suporte, informações menos relevantes |
| **Diversidade** | Roxo | `#9467bd` | Quando precisa diferenciar > 5 categorias |

---

## 📊 Aplicação por Componente

### KPIs Principais
- **Títulos**: Cinza Médio `#7f7f7f`
- **Valores**: Verde Militar `#4B5320` (se OK) ou Vermelho Crítico `#B22222` (se alerta)
- **Delta/Variação**: Verde Militar (positivo) ou Vermelho Crítico (negativo)

### Gráficos de Barras (Saldo por Fonte)
- **Recursos**: Azul Destaque `#4C7695`
- **Dotado**: Vermelho CBMAL `#DC1B13`
- **Empenhado**: Verde Militar `#4B5320`
- **Saldo**: Roxo `#9467bd` (neutro)

### Gráfico Orçado vs Executado
- **Orçado**: Azul Destaque `#4C7695`
- **Executado (< 95%)**: Verde Militar `#4B5320`
- **Executado (95-100%)**: Amarelo `#FFA500`
- **Executado (> 100%)**: Vermelho Crítico `#B22222`

### Status de Processos
- **Empenhado**: Verde Militar `#4B5320` (processo OK)
- **Reservado**: Amarelo `#FFA500` (aguardando)
- **Em análise**: Azul Destaque `#4C7695` (em andamento)
- **Cancelado**: Cinza Médio `#7f7f7f` (inativo)

### Fontes de Recursos
- **500 (Tesouro)**: Azul Destaque `#4C7695` (principal)
- **501 (DREM)**: Vermelho CBMAL `#DC1B13` (destaque)
- **753 (Convênios)**: Verde Militar `#4B5320` (normalidade)
- **759 (Fundos)**: Vermelho Crítico `#B22222` (atenção)
- **622 (SUS)**: Roxo `#9467bd` (diferenciação)

---

## ✅ Checklist C.L.E.A.N.

### C - Contexto
- [ ] O dashboard responde a pergunta em < 5 segundos?
- [ ] KPIs críticos estão visíveis sem scroll?

### L - Limpeza
- [ ] Removidos ruídos visuais?
- [ ] Excesso de bordas eliminado?
- [ ] Cores limitadas a paleta oficial?

### E - Ênfase
- [ ] Dado crítico é o maior elemento visual?
- [ ] KPI principal ocupa pelo menos 20% do topo?
- [ ] Vermelho CBMAL `#DC1B13` usado apenas para elementos essenciais?

### A - Acessibilidade
- [ ] Contraste WCAG 4.5:1 verificado?
- [ ] Tooltips informativos presentes?
- [ ] Texto legível em fundos coloridos?

### N - Navegação
- [ ] Fluxo em "Z" respeitado?
- [ ] Hierarquia visual clara?
- [ ] "Próximo Passo" ou "Ação Requerida" visível?

---

## 🎯 Tipografia Recomendada

### Títulos
- **Font**: Exo 2 Black ou Roboto Bold
- **Tamanho**: 18-24px
- **Cor**: Cinza Médio `#7f7f7f` ou Vermelho CBMAL `#DC1B13` (destaque)

### Dados/KPIs
- **Font**: Arial, Inter ou Roboto
- **Tamanho**: 28-36px (valores principais)
- **Cor**: Verde Militar `#4B5320` (OK) ou Vermelho Crítico `#B22222` (alerta)

### Textos de Suporte
- **Font**: Arial, Inter ou Roboto
- **Tamanho**: 12-14px
- **Cor**: Cinza Médio `#7f7f7f`

---

## 🚫 Anti-Padrões (Evitar)

### Cores
- ❌ **NÃO** usar `#DC1B13` em excesso (reservar para marca e CTAs)
- ❌ **NÃO** usar mais de 5 cores em um único gráfico
- ❌ **NÃO** usar vermelho para dados neutros ou positivos

### Layout
- ❌ **NÃO** colocar mais de 3 itens de destaque no topo
- ❌ **NÃO** usar gráficos de pizza com > 6 fatias
- ❌ **NÃO** usar 3D em gráficos

### Texto
- ❌ **NÃO** usar emojis como ícones (usar SVG)
- ❌ **NÃO** misturar mais de 2 famílias de fontes
- ❌ **NÃO** usar texto < 12px

---

## 📚 Referências

- **Framework**: PaperBanana (Visualizer-Critic loop)
- **Skill**: `dashboard-designer-cbmal` v2.0
- **Padrão**: CBMAL Design Guidelines 2025-2029
- **Desenvolvido por**: APO/EMG

---

**Última Atualização**: 11/02/2026
**Versão**: 1.0
**Aplicado em**: Dashboard de Controle Orçamentário DAL/CBMAL
