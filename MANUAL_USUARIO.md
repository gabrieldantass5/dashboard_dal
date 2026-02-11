# 📘 Manual de Utilização
## Dashboard de Controle Orçamentário DAL/CBMAL

**Versão:** 1.0 MVP
**Data:** 11/02/2026
**Público-alvo:** Diretor DAL, Gestores Financeiros e Analistas

---

## 📑 Índice

1. [Introdução](#1-introdução)
2. [Acessando o Dashboard](#2-acessando-o-dashboard)
3. [Visão Geral da Interface](#3-visão-geral-da-interface)
4. [Usando os KPIs Principais](#4-usando-os-kpis-principais)
5. [Analisando Saldos por Fonte](#5-analisando-saldos-por-fonte)
6. [Comparativo Orçado vs Executado](#6-comparativo-orçado-vs-executado)
7. [Trabalhando com Filtros](#7-trabalhando-com-filtros)
8. [Buscando Processos Específicos](#8-buscando-processos-específicos)
9. [Exportando Dados](#9-exportando-dados)
10. [Dicas e Boas Práticas](#10-dicas-e-boas-práticas)
11. [Perguntas Frequentes](#11-perguntas-frequentes)

---

## 1. Introdução

### O Que é o Dashboard?

O **Dashboard de Controle Orçamentário DAL/CBMAL** é uma ferramenta interativa desenvolvida em Python que substitui a planilha Excel complexa, permitindo visualizar e analisar dados orçamentários de forma rápida e intuitiva.

### Benefícios

| Antes (Excel) | Depois (Dashboard) |
|---------------|-------------------|
| 30-45 minutos para gerar relatório | < 5 minutos |
| Análise manual em 12 abas | Visualização única integrada |
| Cálculos manuais propensos a erro | Cálculos automáticos 100% precisos |
| Gráficos estáticos | Gráficos interativos em tempo real |
| Dificuldade de filtrar dados | Filtros dinâmicos instantâneos |

### Dados Disponíveis

O dashboard processa automaticamente:
- **279 processos** (259 ativos + 20 cancelados)
- **5 fontes de recursos** (500, 501, 753, 759, 622)
- **Total de R$ 27.281.568,51** em recursos
- **R$ 23.382.410,38** já empenhados
- **89,41%** de taxa de execução

---

## 2. Acessando o Dashboard

### Passo a Passo

#### 2.1. Abrir o Terminal/Prompt de Comando

**Windows:**
- Pressione `Win + R`
- Digite `cmd` e pressione Enter
- Navegue até a pasta do projeto:
  ```bash
  cd "C:\Users\D_A_N\OneDrive\Desktop\Dashboard DAL"
  ```

**Alternativa:** Abra a pasta do projeto no Explorer e digite `cmd` na barra de endereços.

#### 2.2. Ativar Ambiente Virtual

```bash
venv\Scripts\activate
```

Você verá `(venv)` aparecer no início da linha do terminal.

#### 2.3. Executar o Dashboard

```bash
streamlit run app.py
```

Ou para modo silencioso:

```bash
streamlit run app.py --server.headless=true
```

#### 2.4. Aguardar Carregamento

Você verá no terminal:

```
Collecting usage statistics...

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.0.6:8501

INFO:__main__:CARREGAMENTO CONCLUÍDO COM SUCESSO
```

#### 2.5. Acessar no Navegador

- O navegador abrirá automaticamente, OU
- Acesse manualmente: **http://localhost:8501**

### Tempos de Carregamento

| Etapa | Tempo |
|-------|-------|
| Inicialização do Streamlit | 2-3s |
| Carregamento do Excel | 1-2s |
| Processamento de dados | 1s |
| Renderização de gráficos | 1s |
| **TOTAL (primeira vez)** | **5-8s** |
| **Acessos subsequentes** | **< 1s (cache)** |

---

## 3. Visão Geral da Interface

### Layout do Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│ 📊 Dashboard de Controle Orçamentário                           │
│ Diretoria de Apoio Logístico - CBMAL | Orçamento 2025          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌──────────┬──────────┬──────────┬──────────┬──────────┐       │
│ │ 27.28M   │ 23.38M   │ 3.90M    │ 259      │ 89.41%   │       │
│ │ Recursos │ Empenhado│ Saldo    │ Processos│ Execução │       │
│ └──────────┴──────────┴──────────┴──────────┴──────────┘       │
│                                                                 │
│ ────────────────────────────────────────────────────────────── │
│                                                                 │
│ 💰 SALDO POR FONTE                                              │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ [GRÁFICO DE BARRAS AGRUPADAS - INTERATIVO]              │    │
│ │                                                          │    │
│ │ Fontes: 500 | 753 | 759 | 622 | 501                     │    │
│ │ Dados: Recursos | Dotado | Empenhado | Saldo            │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ ────────────────────────────────────────────────────────────── │
│                                                                 │
│ 📊 COMPARATIVO: ORÇADO vs EXECUTADO                             │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ [GRÁFICO DE BARRAS HORIZONTAIS]                          │    │
│ │                                                          │    │
│ │ ⚠️ 2 categoria(s) com execução acima de 95%             │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│ ────────────────────────────────────────────────────────────── │
│                                                                 │
│ 🔎 DETALHAMENTO DE DESPESAS                                     │
│ Buscar: [____________]  ⬇️ Baixar CSV                           │
│ ┌─────────────────────────────────────────────────────────┐    │
│ │ [TABELA COM 259 PROCESSOS]                               │    │
│ │ Processo | Objeto | Valor | Fonte | Elemento | Status   │    │
│ └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

SIDEBAR (Barra Lateral):
┌────────────────┐
│ 🔍 FILTROS     │
├────────────────┤
│ Fontes:        │
│ ☑ 500          │
│ ☑ 501          │
│ ☑ 753          │
│ ☑ 759          │
│ ☑ 622          │
│                │
│ Status:        │
│ ☑ Empenhado    │
│ ☑ Reservado    │
│ ☑ Em análise   │
│ ☐ Cancelado    │
│                │
│ 🔄 Limpar      │
└────────────────┘
```

### Elementos Principais

1. **Cabeçalho**: Título e identificação
2. **KPIs**: 5 métricas principais em destaque
3. **Gráfico de Saldos**: Visualização por fonte de recursos
4. **Gráfico Comparativo**: Orçado vs Executado
5. **Tabela de Processos**: Detalhamento completo
6. **Sidebar**: Filtros e controles
7. **Rodapé**: Informações e ajuda

---

## 4. Usando os KPIs Principais

### O Que São KPIs?

**KPI** = Key Performance Indicator (Indicador-Chave de Desempenho)

São métricas resumidas que mostram rapidamente o status orçamentário.

### Os 5 KPIs do Dashboard

#### 4.1. 💰 Total de Recursos

**O que mostra:** Soma de todos os recursos disponíveis de todas as fontes.

**Valor atual:** R$ 27.281.568,51

**Como interpretar:**
- Este é o "teto" orçamentário total
- Soma das 5 fontes: 500 + 501 + 753 + 759 + 622
- Não pode ser ultrapassado

**Tooltip:** Passe o mouse sobre o KPI para ver: "Soma de todas as fontes de recursos disponíveis"

---

#### 4.2. 💳 Total Empenhado

**O que mostra:** Soma de todos os valores já empenhados (comprometidos).

**Valor atual:** R$ 23.382.410,38

**Delta:** 89,41% (percentual do total de recursos)

**Como interpretar:**
- Verde: Boa execução (acima de 85%)
- Amarelo: Execução moderada (60-85%)
- Vermelho: Execução baixa (< 60%)

**Atenção:** Este valor inclui empenhos de **214 processos**.

---

#### 4.3. 💵 Saldo Disponível

**O que mostra:** Quanto ainda resta para empenhar.

**Cálculo:** Recursos - Empenhado

**Valor atual:** R$ 3.899.158,13

**Como interpretar:**
- Este é o valor que ainda pode ser empenhado
- Se chegar perto de zero, recursos estão esgotados
- Se negativo, há problema (sobre-execução)

---

#### 4.4. 📋 Processos Ativos

**O que mostra:** Número de processos em andamento.

**Valor atual:** 259 processos

**Cálculo:** Total (279) - Cancelados (20)

**Status dos processos:**
- **Empenhado:** 214 processos (✅ concluídos)
- **Reservado:** 45 processos (⏳ em andamento)
- **Cancelado:** 20 processos (❌ excluídos do cálculo)

---

#### 4.5. 📊 Taxa de Execução

**O que mostra:** Percentual médio de execução orçamentária.

**Cálculo:** (Total Empenhado / Total Dotado) × 100

**Valor atual:** 89,41%

**Como interpretar:**
- **< 70%:** Execução baixa (atenção necessária)
- **70-85%:** Execução moderada (dentro do esperado)
- **85-95%:** Boa execução (meta atingida)
- **> 95%:** Execução alta (risco de esgotar recursos)

---

## 5. Analisando Saldos por Fonte

### Entendendo o Gráfico

O gráfico de barras agrupadas mostra 4 métricas para cada uma das 5 fontes de recursos:

1. **Recursos** (azul): Total disponível para a fonte
2. **Dotado** (laranja): Valor alocado/planejado
3. **Empenhado** (verde): Valor já comprometido
4. **Saldo** (roxo): Valor restante (Recursos - Empenhado)

### As 5 Fontes de Recursos

#### Fonte 500 - Tesouro

**Recursos:** R$ 15.911.610,00
**Empenhado:** R$ 15.899.799,31
**Saldo:** R$ 11.810,69
**% Execução:** 99,93%

⚠️ **ATENÇÃO:** Fonte praticamente esgotada! Apenas 0,07% de saldo.

---

#### Fonte 753 - Convênios/Taxas

**Recursos:** R$ 5.260.154,46
**Empenhado:** R$ 3.802.009,49
**Saldo:** R$ 1.458.144,97
**% Execução:** 72,28%

✅ **OK:** Execução moderada, ainda há saldo significativo.

---

#### Fonte 759 - Fundos

**Recursos:** R$ 3.989.462,32
**Empenhado:** R$ 3.658.376,58
**Saldo:** R$ 331.085,74
**% Execução:** 91,70%

⚠️ **ATENÇÃO:** Execução alta, saldo limitado.

---

#### Fonte 622 - SUS

**Recursos:** R$ 32.505,73
**Empenhado:** R$ 22.225,00
**Saldo:** R$ 10.280,73
**% Execução:** 68,37%

✅ **OK:** Pequeno valor, mas execução controlada.

---

#### Fonte 501 - Tesouro DREM

**Recursos:** R$ 2.087.836,00
**Empenhado:** R$ 0,00
**Saldo:** R$ 2.087.836,00
**% Execução:** 0,00%

❗ **IMPORTANTE:** Recurso ainda não utilizado. Investigar motivo.

---

### Como Usar o Gráfico

#### Interagir com Hover (Passar Mouse)

1. **Passe o mouse** sobre qualquer barra
2. Aparecerá um **tooltip** mostrando:
   - Nome da fonte
   - Métrica (Recursos/Dotado/Empenhado/Saldo)
   - Valor formatado em R$

**Exemplo:**
```
500 - Tesouro
Saldo: R$ 11.810,69
```

#### Zoom e Pan

- **Zoom:** Role o scroll do mouse sobre o gráfico
- **Pan (arrastar):** Clique e arraste o gráfico
- **Resetar:** Clique duas vezes no gráfico

#### Comparar Fontes

- Compare visualmente as alturas das barras
- Identifique rapidamente quais fontes têm maior saldo
- Veja quais estão com execução alta (saldo pequeno)

---

### Tabela de Detalhamento

À direita do gráfico, há uma tabela com os valores exatos:

| Fonte | Recursos | Dotado | Empenhado | Saldo | % Execução |
|-------|----------|--------|-----------|-------|------------|
| 500 | R$ 15.911.610,00 | ... | R$ 15.899.799,31 | R$ 11.810,69 | 99,93% |
| 753 | R$ 5.260.154,46 | ... | R$ 3.802.009,49 | R$ 1.458.144,97 | 72,28% |
| 759 | R$ 3.989.462,32 | ... | R$ 3.658.376,58 | R$ 331.085,74 | 91,70% |
| 622 | R$ 32.505,73 | ... | R$ 22.225,00 | R$ 10.280,73 | 68,37% |
| 501 | R$ 2.087.836,00 | ... | R$ 0,00 | R$ 2.087.836,00 | 0,00% |
| **TOTAL** | **R$ 27.281.568,51** | ... | **R$ 23.382.410,38** | **R$ 3.899.158,13** | **89,41%** |

**Use esta tabela para:**
- Copiar valores exatos para relatórios
- Verificar cálculos
- Exportar para Excel (via screenshot ou transcrição)

---

## 6. Comparativo Orçado vs Executado

### O Que Este Gráfico Mostra

Compara o valor **planejado (orçado)** com o valor **realizado (executado)** por categoria.

No MVP, a granularidade é por **Elemento de Despesa**:
- Material de Consumo
- Material Permanente
- Serviço PJ (Pessoa Jurídica)
- Serviço PF (Pessoa Física)

### Interpretando o Gráfico

#### Barras Azuis = Orçado

O que foi planejado/alocado para cada categoria.

#### Barras Verdes/Amarelas/Vermelhas = Executado

O que realmente foi gasto/empenhado.

**Cores:**
- 🟢 **Verde:** Execução normal (< 95%)
- 🟡 **Amarelo:** Execução alta (95-100%)
- 🔴 **Vermelho:** Sobre-execução (> 100%)

### Alertas Automáticos

Se houver categorias com execução > 95%, aparecerá um alerta:

```
⚠️ 2 categoria(s) com execução acima de 95%
```

**Clique em "Ver categorias em risco"** para expandir e ver detalhes:

| Categoria | Orçado | Executado | Saldo | % Execução |
|-----------|--------|-----------|-------|------------|
| Material Permanente | R$ 5.000.000 | R$ 4.850.000 | R$ 150.000 | 97,0% |
| Serviço PJ | R$ 8.000.000 | R$ 7.700.000 | R$ 300.000 | 96,3% |

**Ação recomendada:**
- Bloquear novos processos nessas categorias
- Avaliar necessidade de remanejamento
- Comunicar gestores responsáveis

---

## 7. Trabalhando com Filtros

### Localização

Os filtros estão na **barra lateral esquerda** (sidebar).

### Filtro: Fontes de Recursos

**O que faz:** Mostra apenas processos das fontes selecionadas.

**Como usar:**
1. Clique na caixa "Fontes de Recursos"
2. **Marque** as fontes que deseja ver
3. **Desmarque** as que deseja ocultar
4. O dashboard atualiza automaticamente

**Exemplo de uso:**

**Cenário:** "Quero ver apenas processos da fonte 500 (Tesouro)"

**Passos:**
1. Abrir filtro de fontes
2. Desmarcar todas (500, 501, 753, 759, 622)
3. Marcar apenas 500
4. ✅ Dashboard mostra apenas fonte 500

**Resultado:**
- KPIs recalculados apenas para fonte 500
- Gráficos mostram apenas fonte 500
- Tabela filtra apenas processos com Fonte = 500

---

### Filtro: Status dos Processos

**O que faz:** Mostra apenas processos com os status selecionados.

**Status disponíveis:**
- ✅ **Empenhado** (214 processos): Processo concluído, valor empenhado
- ⏳ **Reservado** (45 processos): Processo em andamento, valor reservado
- 📋 **Em análise** (0 processos): Processo em fase inicial
- ❌ **Cancelado** (20 processos): Processo cancelado (não conta no saldo)

**Padrão:** Por padrão, "Cancelado" vem desmarcado (excluído).

**Como usar:**

**Cenário 1:** "Quero ver apenas processos empenhados"

1. Desmarcar todos os status
2. Marcar apenas "Empenhado"
3. ✅ Tabela mostra 214 processos

**Cenário 2:** "Quero incluir processos cancelados na análise"

1. Marcar também "Cancelado"
2. ✅ Tabela mostra 279 processos (259 + 20)

---

### Filtros Combinados

Você pode combinar múltiplos filtros!

**Exemplo:**

**Objetivo:** "Ver processos empenhados da fonte 500"

**Passos:**
1. Filtro Fontes: Selecionar apenas 500
2. Filtro Status: Selecionar apenas "Empenhado"
3. ✅ Resultado: Apenas processos empenhados da fonte 500

---

### Limpar Filtros

**Botão:** 🔄 Limpar Filtros

**O que faz:** Volta todos os filtros para o padrão (todas as fontes, sem cancelados).

---

### Efeitos dos Filtros

Quando você aplica filtros, **TODO o dashboard é atualizado**:

1. **KPIs:** Recalculados para dados filtrados
2. **Gráfico de Saldos:** Mostra apenas fontes selecionadas
3. **Gráfico Comparativo:** Recalcula com dados filtrados
4. **Tabela:** Mostra apenas linhas que passam nos filtros
5. **Contadores:** Atualizam (ex: "Processos exibidos: 150")

---

## 8. Buscando Processos Específicos

### Barra de Busca

**Localização:** Acima da tabela de despesas

**Campo:** 🔍 Buscar por processo ou objeto

### Como Usar

#### Buscar por Número de Processo

**Exemplo:** Procurar processo "E:01203.0000000498/2025"

**Passos:**
1. Clicar no campo de busca
2. Digitar: `498` (parte do número)
3. ✅ Tabela filtra em tempo real
4. Resultado: Apenas processos com "498" no número

**Dica:** Não precisa digitar o número completo!

---

#### Buscar por Objeto

**Exemplo:** Procurar todos os processos de "Água"

**Passos:**
1. Clicar no campo de busca
2. Digitar: `água`
3. ✅ Tabela filtra instantaneamente
4. Resultado: Apenas processos com "água" no objeto

**Nota:** A busca não diferencia maiúsculas/minúsculas.

---

#### Busca Combinada

A busca procura em **duas colunas simultaneamente**:
- Número do Processo
- Objeto

**Exemplo:** Digitar "consumo" encontra:
- Processos com "consumo" no objeto
- Processos com número contendo "consumo" (raro)

---

### Ordenação da Tabela

**Como ordenar:**
1. Clique no **cabeçalho da coluna**
2. Primeira vez: Ordem crescente ▲
3. Segunda vez: Ordem decrescente ▼

**Colunas ordenáveis:**
- Processo (alfabética)
- Valor (numérica)
- Fonte (numérica)
- Elemento (alfabética)
- Status (alfabética)

**Exemplo de uso:**

**Objetivo:** "Ver processos com maior valor primeiro"

**Passos:**
1. Clicar em "Valor" (cabeçalho)
2. Clicar novamente (ordem decrescente)
3. ✅ Processos com maior valor aparecem no topo

---

## 9. Exportando Dados

### Botão de Download

**Localização:** Canto superior direito da seção de tabela

**Botão:** ⬇️ Baixar CSV

### O Que É Exportado

- **Formato:** CSV (Comma-Separated Values)
- **Encoding:** UTF-8-BOM (compatível com Excel)
- **Dados:** Apenas as linhas **visíveis** após filtros e busca

**Importante:** Se você aplicou filtros, apenas os dados filtrados serão exportados!

---

### Como Exportar

#### Passo a Passo

1. **Aplicar filtros desejados** (opcional)
   - Selecionar fontes
   - Selecionar status
   - Usar busca

2. **Verificar contadores**
   - "Processos exibidos: X"
   - Certifique-se que é o número esperado

3. **Clicar em "⬇️ Baixar CSV"**

4. **Salvar arquivo**
   - Nome padrão: `despesas_filtradas.csv`
   - Escolher local para salvar
   - Clicar em "Salvar"

---

### Abrindo no Excel

1. **Abrir Excel**
2. **Arquivo → Abrir**
3. **Selecionar o CSV baixado**
4. ✅ Abre corretamente com acentos

**Nota:** O encoding UTF-8-BOM garante que acentos apareçam corretamente.

---

### Exemplos de Uso

#### Exemplo 1: Exportar apenas fonte 500

**Objetivo:** Gerar relatório apenas da fonte 500 (Tesouro)

**Passos:**
1. Filtro Fontes: Selecionar apenas 500
2. Verificar: "Processos exibidos: ~150" (aproximado)
3. Clicar em "⬇️ Baixar CSV"
4. ✅ Arquivo contém apenas fonte 500

---

#### Exemplo 2: Exportar processos empenhados de valor alto

**Objetivo:** Lista de processos empenhados com valor > R$ 100.000

**Passos:**
1. Filtro Status: Selecionar apenas "Empenhado"
2. Clicar em "Valor" para ordenar (decrescente)
3. Verificar visualmente os valores > 100k
4. Baixar CSV
5. No Excel: Filtrar coluna "Valor" > 100000

---

## 10. Dicas e Boas Práticas

### 💡 Dicas de Performance

1. **Primeira execução:** Aguarde 5-8 segundos para carregar completamente
2. **Cache automático:** Após primeira vez, é quase instantâneo
3. **Não abra o Excel simultaneamente:** Pode causar conflito de arquivo
4. **Use filtros:** Dashboard responde mais rápido com menos dados

---

### 💡 Dicas de Análise

1. **Comece pelos KPIs:** Visão geral em 5 segundos
2. **Identifique alertas:** Procure por categorias > 95%
3. **Compare fontes:** Use o gráfico de saldos
4. **Foque no crítico:** Fonte 500 está 99,93% executada!
5. **Investigue anomalias:** Fonte 501 com 0% de execução

---

### 💡 Dicas de Uso Diário

#### Para Diretores

**Rotina sugerida: 5 minutos/dia**

1. Abrir dashboard (1 min)
2. Verificar KPIs (30s)
3. Identificar alertas (1 min)
4. Verificar saldo das fontes críticas (2 min)
5. Tomar decisões baseadas em dados (30s)

---

#### Para Gestores Financeiros

**Rotina sugerida: 15 minutos/dia**

1. Verificar KPIs e alertas (2 min)
2. Analisar saldos por fonte (3 min)
3. Revisar processos empenhados do dia (5 min)
4. Atualizar planilha Excel com novos dados (3 min)
5. Recarregar dashboard com Excel atualizado (2 min)

---

#### Para Analistas de Dados

**Rotina sugerida: Conforme demanda**

1. Manter planilha Excel atualizada
2. Gerar relatórios sob demanda com filtros
3. Exportar dados para análises externas
4. Validar valores com Excel original
5. Investigar discrepâncias

---

### 💡 Quando Atualizar Dados

**Frequência recomendada:** Semanal ou conforme novos empenhos

**Como atualizar:**

1. **Atualizar a planilha Excel** (`data/ORÇAMENTO 2025 (1).xlsx`)
2. **Salvar e fechar** o Excel
3. **Recarregar o dashboard:**
   - Pressionar `C` na interface do dashboard (limpar cache)
   - Ou pressionar `Ctrl+C` no terminal e executar novamente
4. **Verificar logs:** "CARREGAMENTO CONCLUÍDO COM SUCESSO"
5. **Validar:** Verificar se valores mudaram conforme esperado

---

## 11. Perguntas Frequentes

### ❓ Como sei que os dados estão corretos?

**Resposta:**

1. Ao carregar, o dashboard exibe no terminal:
   ```
   ✅ VALIDAÇÃO: Valores batem com Excel
   ```

2. Valores esperados (validados):
   - Total Recursos: R$ 27.281.568,51
   - Total Empenhado: R$ 23.382.410,38

3. Se os valores forem diferentes, verifique se:
   - Está usando a planilha correta
   - Planilha foi modificada recentemente
   - Cache está desatualizado (pressione `C`)

---

### ❓ Os filtros afetam os KPIs?

**Resposta:** **SIM!**

Os KPIs são **recalculados** quando você aplica filtros.

**Exemplo:**
- **Sem filtros:** Total Empenhado = R$ 23.382.410,38
- **Apenas fonte 500:** Total Empenhado = R$ 15.899.799,31

Isso permite analisar cada fonte isoladamente.

---

### ❓ Posso usar em outro computador?

**Resposta:** Sim, mas precisa:

1. **Instalar Python 3.9+**
2. **Copiar todo o projeto** (pasta completa)
3. **Incluir a planilha Excel** em `data/`
4. **Criar ambiente virtual e instalar dependências**
5. **Executar normalmente**

---

### ❓ Posso compartilhar o dashboard?

**Resposta:**

**Localmente:** Outros computadores na mesma rede podem acessar usando o "Network URL":
```
Network URL: http://192.168.0.6:8501
```

**Atenção:**
- ⚠️ Dados são **sensíveis** (orçamento do CBMAL)
- ⚠️ Não compartilhar publicamente
- ⚠️ Apenas rede interna confiável

**Para acesso remoto seguro:** Aguardar versão 5.0 com autenticação.

---

### ❓ Como faço para parar o dashboard?

**Resposta:**

1. **No terminal:** Pressionar `Ctrl + C`
2. **Ou:** Fechar a janela do terminal
3. A página no navegador mostrará "Connection lost"

Para executar novamente: `streamlit run app.py`

---

### ❓ Posso modificar a planilha Excel enquanto o dashboard está aberto?

**Resposta:** **NÃO recomendado!**

**Motivo:**
- Pode causar erro de acesso ao arquivo
- Pode gerar dados inconsistentes
- Cache pode não atualizar

**Procedimento correto:**
1. **Parar** o dashboard (Ctrl+C)
2. **Modificar** a planilha Excel
3. **Salvar e fechar** o Excel
4. **Executar** o dashboard novamente

---

### ❓ Por que a Fonte 501 tem 0% de execução?

**Resposta:**

Segundo os dados carregados:
- Recursos disponíveis: R$ 2.087.836,00
- Empenhado: R$ 0,00
- % Execução: 0,00%

**Possíveis motivos:**
1. Recurso recém-disponibilizado
2. Aguardando planejamento
3. Reservado para contingência
4. Erro nos dados (verificar Excel)

**Ação recomendada:** Verificar com gestor responsável.

---

### ❓ O que significa "2 categoria(s) com execução > 95%"?

**Resposta:**

Indica que 2 elementos de despesa estão com execução muito alta:
- Risco de esgotar recursos
- Pode ser necessário bloquear novos processos
- Avaliar possibilidade de remanejamento

**Clique no alerta** para ver quais categorias e tomar ação.

---

### ❓ Posso adicionar mais filtros?

**Resposta:**

**No MVP (v1.0):** Apenas 2 filtros (Fontes e Status)

**Versões futuras (v2.0+):**
- Filtro por Elemento de Despesa
- Filtro por Ação do PCA
- Filtro por período/data
- Filtro por faixa de valor

---

### ❓ Como sei qual versão estou usando?

**Resposta:**

Veja no rodapé do dashboard ou no README.md:
- **Versão atual:** 1.0 MVP
- **Data:** 11/02/2026

---

## 📞 Suporte

### Problemas Técnicos

1. **Consultar:** `README.md` (seção "Solução de Problemas")
2. **Consultar:** `TESTES.md` (checklist de validação)
3. **Logs:** Verificar terminal para mensagens de erro
4. **Contato:** Equipe de TI do CBMAL

### Dúvidas sobre Dados

1. **Validar com Excel:** Comparar valores manualmente
2. **Verificar planilha:** Confirmar que está atualizada
3. **Contato:** Analista de Dados responsável
4. **Contato:** Gestor Financeiro DAL

---

## 📚 Documentação Adicional

- **README.md**: Guia rápido de instalação e uso
- **TESTES.md**: Checklist de validação e testes
- **docs/02_PRD.md**: Requisitos detalhados do produto
- **docs/03_MVP.md**: Definição do MVP
- **docs/04_SPECS_TECNICAS.md**: Especificações técnicas

---

**📘 Fim do Manual de Utilização**

**Versão:** 1.0 MVP
**Última atualização:** 11/02/2026
**Desenvolvido por:** Claude Code + Equipe DAL/CBMAL

**🎊 Bom uso do Dashboard!**
