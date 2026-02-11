# CLAUDE.md - Guia para Claude Code
## Dashboard de Controle Orçamentário DAL/CBMAL

Este arquivo orienta o Claude Code sobre a estrutura e convenções do projeto.

---

## 📁 Estrutura do Projeto

```
Dashboard-DAL/
├── app.py                          # Aplicação principal Streamlit
├── src/
│   ├── data_loader.py             # Carregamento de dados do Excel
│   ├── data_processor.py          # Processamento e agregações
│   ├── visualizations.py          # Gráficos Plotly
│   └── utils.py                   # Funções auxiliares
├── data/
│   └── ORÇAMENTO 2025 (1).xlsx    # Planilha de dados (não versionada)
├── docs/
│   ├── 01_BRIEFING.md
│   ├── 02_PRD.md
│   ├── 03_MVP.md
│   └── 04_SPECS_TECNICAS.md
├── requirements.txt
├── README.md
├── CLAUDE.md                       # Este arquivo
└── .gitignore
```

---

## 🎯 Objetivo do Projeto

Dashboard interativo em Python/Streamlit para visualização e análise de dados orçamentários da DAL/CBMAL, substituindo planilha Excel complexa.

---

## 🚀 Comandos Comuns

### Executar Dashboard
```bash
streamlit run app.py
```

### Instalar Dependências
```bash
pip install -r requirements.txt
```

### Criar Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Atualizar Dependências
```bash
pip freeze > requirements.txt
```

### Limpar Cache do Streamlit
```bash
# Via CLI
streamlit cache clear

# Ou pressionar 'C' na interface web
```

---

## 📊 Arquitetura de Dados

### Fluxo Principal

```
Excel (ORÇAMENTO 2025.xlsx)
    ↓
data_loader.py (load_excel_data, clean_*)
    ↓
DataFrames limpos (pandas)
    ↓
data_processor.py (calcular_*, processar_*)
    ↓
Métricas e agregações
    ↓
visualizations.py (grafico_*)
    ↓
app.py (Streamlit)
    ↓
Dashboard interativo
```

### Abas do Excel Utilizadas

**MVP (Versão 1.0):**
- `CONTROLE DE DESPESAS`: Processos, valores, status
- `BALANCO`: Recursos, dotado, empenhado por fonte

**Post-MVP:**
- `PCA 2025`: Execução do planejamento anual
- `Despesas 2025`: Despesas recorrentes
- `RECURSOS TESOURO 2025`: Aportes mensais

### DataFrames Principais

**df_despesas** (de CONTROLE DE DESPESAS):
```python
Colunas:
- Processo: str
- Objeto: str
- Valor: float
- Fonte: int (500, 501, 753, 759, 622)
- Elemento: str ("CONSUMO", "PERMANENTE", "SERVIÇO PJ", "SERVIÇO PF")
- Status: str ("Empenhado", "Reservado", "Em análise", "Cancelado")
- Acao_PCA: str
- Observacao: str
```

**df_balanco** (de BALANCO):
```python
Colunas:
- Fonte: int ou 'TOTAL' (500, 501, 753, 759, 622)
- Recursos: float
- Dotado: float
- Empenhado: float
- Saldo: float (calculado)
- Perc_Execucao: float (calculado)
```

---

## 🔧 Módulos e Responsabilidades

### `src/data_loader.py`

**Responsabilidade**: Carregar e limpar dados do Excel

**Funções principais**:
- `load_excel_data(filepath)`: Carrega todas as abas do Excel
- `clean_despesas(df_raw)`: Limpa aba CONTROLE DE DESPESAS
- `clean_balanco(df_raw)`: Limpa aba BALANCO
- `clean_pca(df_raw)`: Limpa aba PCA 2025 (Post-MVP)

**Convenções**:
- Usar `@st.cache_data` para cache
- Logar erros com `logging`
- Validar estrutura esperada do Excel
- Tratar valores nulos apropriadamente

### `src/data_processor.py`

**Responsabilidade**: Processar dados e calcular métricas

**Funções principais**:
- `gerar_metricas_kpi(df_balanco, df_despesas)`: Calcula 5 KPIs
- `calcular_saldos_por_fonte(df_balanco)`: Wrapper/validação
- `calcular_orcado_vs_executado(df_despesas, granularidade)`: Comparativo

**Convenções**:
- Retornar sempre novos DataFrames (não modificar originais)
- Validar parâmetros de entrada
- Documentar fórmulas de cálculo em docstrings

### `src/visualizations.py`

**Responsabilidade**: Criar gráficos Plotly

**Funções principais**:
- `grafico_saldo_por_fonte(df_saldos)`: Barras agrupadas
- `grafico_orcado_vs_executado(df_comparativo)`: Barras horizontais
- `tabela_interativa_despesas(df)`: Tabela Streamlit formatada

**Convenções**:
- Sempre retornar `go.Figure` (Plotly)
- Usar cores de `src/utils.py` (constantes)
- Incluir tooltips informativos
- Height padrão: 500px

### `src/utils.py`

**Responsabilidade**: Funções auxiliares e constantes

**Funções principais**:
- `formatar_moeda(valor)`: R$ 1.234,56
- `formatar_percentual(valor)`: 85,7%
- `aplicar_filtros(df, filtros)`: Filtragem múltipla

**Constantes**:
- `CORES_PADRAO`: Dict de cores do dashboard
- `CORES_FONTES`: Dict {fonte: cor}
- `NOMES_FONTES`: Dict {fonte: nome legível}
- `ELEMENTOS_DESPESA`: Lista de elementos
- `STATUS_PROCESSOS`: Lista de status

### `app.py`

**Responsabilidade**: Interface Streamlit

**Estrutura**:
1. Imports e configuração (`st.set_page_config`)
2. Cabeçalho
3. Sidebar com filtros
4. Carregamento de dados (cached)
5. Processamento
6. Seção 1: KPIs
7. Seção 2: Saldo por fonte
8. Seção 3: Orçado vs executado
9. Seção 4: Tabela detalhada
10. Rodapé

**Convenções**:
- Layout wide: `layout="wide"`
- Sidebar expandida: `initial_sidebar_state="expanded"`
- Cache em funções de carregamento
- Usar `st.columns()` para layout
- Usar `st.divider()` entre seções

---

## 🎨 Convenções de Código

### Estilo Python
- **PEP 8** compliant
- Usar type hints sempre que possível
- Docstrings estilo Google:
  ```python
  def funcao(param: str) -> int:
      """
      Descrição breve da função.

      Args:
          param: Descrição do parâmetro

      Returns:
          Descrição do retorno

      Raises:
          ValueError: Quando ocorre erro X
      """
  ```

### Nomenclatura
- **Funções**: snake_case (`calcular_saldo`, `gerar_kpis`)
- **Classes**: PascalCase (não usado no MVP)
- **Constantes**: UPPER_SNAKE_CASE (`CORES_PADRAO`, `FONTES_RECURSOS`)
- **Variáveis**: snake_case (`df_despesas`, `total_recursos`)

### Imports
```python
# Libs padrão primeiro
import logging
from typing import Dict, List

# Libs externas
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Imports locais
from src.data_loader import load_excel_data
from src.utils import formatar_moeda
```

---

## 🧪 Testes e Validação

### Valores de Validação (vs Excel)

Após mudanças em `data_loader.py` ou `data_processor.py`, validar:

1. Total Recursos = R$ 27.281.568,51
2. Total Empenhado = R$ 23.382.410,38
3. Saldo Total = R$ 3.899.158,13
4. Recursos Fonte 500 = R$ 15.911.610,00
5. Número de processos ≈ 279 (excluindo vazios)

### Como Testar

```bash
# Executar dashboard
streamlit run app.py

# Verificar logs no terminal
# Comparar KPIs com valores esperados
# Testar filtros (selecionar apenas fonte 500)
# Testar busca na tabela
# Testar exportação CSV
```

---

## 📝 Ao Modificar o Código

### Checklist de Desenvolvimento

- [ ] Código segue PEP 8
- [ ] Type hints adicionados
- [ ] Docstrings completas
- [ ] Logging adicionado (se aplicável)
- [ ] Valores validados com Excel
- [ ] Performance testada (< 5s carregamento)
- [ ] README.md atualizado (se mudança de features)

### Quando Adicionar Nova Funcionalidade

1. Ler PRD (`docs/02_PRD.md`) e MVP (`docs/03_MVP.md`)
2. Verificar se é MVP ou Post-MVP
3. Adicionar código no módulo apropriado
4. Documentar função com docstring
5. Testar individualmente
6. Integrar com `app.py`
7. Validar dados
8. Atualizar README se visível ao usuário

### Quando Corrigir Bug

1. Reproduzir o bug
2. Identificar módulo afetado
3. Adicionar log de debug se necessário
4. Corrigir código
5. Validar com dados reais
6. Verificar se não quebrou outras features

---

## 🔍 Debugging

### Logs de Debug

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Uso
logger.info(f"Carregando Excel: {filepath}")
logger.warning(f"Coluna tem {n} valores nulos")
logger.error(f"Erro ao processar: {e}")
```

### Streamlit Debug Mode

```bash
# Executar com logs detalhados
streamlit run app.py --logger.level=debug
```

### Inspecionar DataFrames

```python
# No código
print(df.head())
print(df.info())
print(df.describe())

# No Streamlit (temporariamente)
st.write(df)
st.dataframe(df)
```

---

## 🚨 Erros Comuns

### FileNotFoundError: Excel não encontrado
**Causa**: Arquivo não está em `data/ORÇAMENTO 2025 (1).xlsx`
**Solução**: Verificar caminho e nome exato (incluindo espaços)

### KeyError em coluna
**Causa**: Estrutura do Excel mudou
**Solução**: Revisar `clean_despesas()` ou `clean_balanco()`

### Valores não batem
**Causa**: Lógica de cálculo incorreta ou dados mudaram
**Solução**: Comparar linha por linha com Excel, revisar fórmulas

### Cache desatualizado
**Causa**: Dados mudaram mas cache persiste
**Solução**: Limpar cache (pressionar 'C' no dashboard)

---

## 🔐 Segurança

### Dados Sensíveis

- **NUNCA** commitar arquivos `.xlsx` no Git
- **NUNCA** fazer deploy público sem autenticação
- Executar apenas localmente (localhost) no MVP
- Validar `.gitignore` antes de cada commit

### Arquivos Críticos Não Versionados

- `data/*.xlsx`
- `.streamlit/secrets.toml`
- Qualquer arquivo com dados financeiros reais

---

## 📦 Dependências Principais

| Lib | Versão | Uso |
|-----|--------|-----|
| streamlit | 1.31.0 | Framework de dashboard |
| pandas | 2.1.0 | Manipulação de dados |
| plotly | 5.18.0 | Visualizações interativas |
| openpyxl | 3.1.2 | Leitura de Excel |
| numpy | 1.26.0 | Operações numéricas |

---

## 🗺️ Roadmap Técnico

### MVP (v1.0) - Atual
- [x] Documentação completa
- [ ] Backend (data_loader, data_processor, utils)
- [ ] Frontend (visualizations, app)
- [ ] Testes e validação

### v2.0
- [ ] Gráfico de status de processos
- [ ] Execução PCA 2025
- [ ] Granularidades adicionais

### v3.0+
- [ ] Evolução temporal
- [ ] Comparativos multi-ano
- [ ] Deploy em servidor

---

## 💡 Dicas para Claude Code

### Ao Ler Código
- Sempre consultar specs técnicas (`docs/04_SPECS_TECNICAS.md`)
- Verificar convenções neste arquivo
- Entender fluxo de dados antes de modificar

### Ao Escrever Código
- Seguir estrutura de funções em specs técnicas
- Usar type hints e docstrings
- Validar com dados reais
- Logar operações importantes

### Ao Fazer Commit
- Verificar `.gitignore` (não commitar Excel)
- Mensagem clara: "feat:", "fix:", "docs:"
- Testar antes de commitar

---

**Última atualização**: 11/02/2026 | MVP v1.0
