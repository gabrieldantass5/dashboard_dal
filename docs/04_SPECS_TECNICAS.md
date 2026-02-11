# Especificações Técnicas Detalhadas
## Dashboard de Controle Orçamentário DAL/CBMAL

**Versão:** 1.0
**Data:** 11/02/2026
**Objetivo:** Detalhar estruturas de dados, transformações e design de implementação

---

## 1. Arquitetura de Dados

### 1.1 Fluxo de Dados Geral

```
┌─────────────────┐
│  EXCEL (.xlsx)  │
│  12 abas        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  data_loader.py │ ← Carregamento e limpeza
│  load_excel()   │
│  clean_*()      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DataFrames     │ ← Dados limpos em memória
│  Pandas         │   (cached com @st.cache_data)
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ data_processor.py│ ← Processamento e cálculos
│ calcular_*()     │
│ processar_*()    │
└────────┬─────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
┌──────────────┐ ┌─────────────┐ ┌──────────┐
│ KPIs         │ │ Agregações  │ │ Métricas │
│ (dict)       │ │ (DataFrame) │ │ (Series) │
└──────┬───────┘ └──────┬──────┘ └─────┬────┘
       │                │               │
       └────────────────┴───────────────┘
                        │
                        ▼
        ┌───────────────────────────┐
        │  visualizations.py        │ ← Criação de gráficos
        │  grafico_*()              │
        └───────────────┬───────────┘
                        │
                        ▼
        ┌───────────────────────────┐
        │  app.py (Streamlit)       │ ← Interface do usuário
        │  Renderização + Filtros   │
        └───────────────────────────┘
```

---

## 2. Estrutura de Dados do Excel

### 2.1 Aba: CONTROLE DE DESPESAS (MVP - CRÍTICA)

**Dimensões:** 303 linhas × 9 colunas

**Estrutura original (raw):**
```
Linha 0: Vazia (header de mesclagem)
Linha 1: Cabeçalhos verdadeiros
Linha 2+: Dados
```

**Mapeamento de colunas:**

| Coluna Original | Nome Limpo | Tipo | Descrição | Exemplo |
|----------------|-----------|------|-----------|---------|
| `Unnamed: 0` | `Processo` | str | Número do processo | "E:01203.0000000498/2025" |
| `Unnamed: 1` | `Objeto` | str | Descrição do objeto | "Água mineral" |
| `CONTROLE DE DESPESAS 2025` | `Valor` | float | Valor total do processo | 32709.00 |
| `Unnamed: 3` | `Fonte` | int | Fonte de recursos | 500, 501, 753, 759, 622 |
| `Unnamed: 4` | `Elemento` | str | Elemento de despesa | "CONSUMO", "PERMANENTE", etc. |
| `Unnamed: 5` | `Nota_Reserva` | bool | Tem nota de reserva? | True/False |
| `Unnamed: 6` | `Nota_Empenho` | bool | Tem nota de empenho? | True/False |
| `Unnamed: 7` | `Acao_PCA` | str | Ação do PCA 2025 | "Expediente, limpeza..." |
| `Unnamed: 8` | `Observacao` | str | Observações | (maioria vazia) |

**Transformações necessárias:**

1. **Pular linha 0** (vazia/mesclada)
2. **Usar linha 1 como header** parcial, mas renomear colunas manualmente
3. **Criar coluna `Status`** derivada de:
   - `Nota_Empenho == True` → "Empenhado"
   - `Nota_Reserva == True` e `Nota_Empenho == False` → "Reservado"
   - Ambos `False` → "Em análise"
   - Se `Valor == 0` ou processo marcado como "CANCELADO" na observação → "Cancelado"

4. **Remover linhas vazias:**
   - Onde `Processo` é NaN ou vazio
   - Total esperado: ~279 linhas de dados (303 - 24 nulas)

5. **Converter tipos:**
   ```python
   df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
   df['Fonte'] = pd.to_numeric(df['Fonte'], errors='coerce').astype('Int64')
   df['Nota_Reserva'] = df['Nota_Reserva'].fillna(False).astype(bool)
   df['Nota_Empenho'] = df['Nota_Empenho'].fillna(False).astype(bool)
   ```

6. **Calcular % Execução:**
   - Requer cruzamento com aba BALANCO (Dotado por fonte)
   - `% Exec = (Valor / Dotado_da_Fonte) × 100`

**DataFrame resultante (clean_despesas):**

```python
Colunas finais:
- Processo: str
- Objeto: str
- Valor: float
- Fonte: int (500, 501, 753, 759, 622)
- Elemento: str ("CONSUMO", "PERMANENTE", "SERVIÇO PJ", "SERVIÇO PF")
- Status: str ("Empenhado", "Reservado", "Em análise", "Cancelado")
- Acao_PCA: str
- Observacao: str

Shape esperado: (~279, 8)
```

---

### 2.2 Aba: BALANCO (MVP - CRÍTICA)

**Dimensões:** 67 linhas × 15 colunas

**Estrutura original (raw):**
- Planilha de layout complexo (não tabular)
- Dados organizados em "regiões" específicas
- Linhas importantes:
  - Linha com "SALDOS" + colunas 500, 753, 759, 622, 501
  - Linha com "RECURSOS"
  - Linha com "DOTADO"
  - Linha com "EMPENHADO"

**Estrutura identificada:**

```
Linha 2 (índice 2): SALDOS | 500 | 753 | 759 | 622 | 501 | SOMATÓRIO
Linha X: RECURSOS          | val | val | val | val | val | total
Linha Y: DOTADO            | val | val | val | val | val | total
Linha Z: EMPENHADO         | val | val | val | val | val | total
```

**Exemplo de dados (baseado na análise):**

| Métrica | 500 | 753 | 759 | 622 | 501 | Total |
|---------|-----|-----|-----|-----|-----|-------|
| RECURSOS | 15.911.610 | 5.260.154 | 1.717.749 | 2.880.926 | valor | 27.281.568 |
| DOTADO   | 15.900.724 | 4.819.755 | valor | valor | valor | total |
| EMPENHADO | 15.899.799 | 3.802.009 | valor | valor | valor | 23.382.410 |

**Transformações necessárias:**

1. **Localizar linhas-chave:**
   ```python
   # Encontrar linha que contém "SALDOS" ou "RECURSOS"
   idx_recursos = df[df['Unnamed: 1'] == 'RECURSOS'].index[0]
   idx_dotado = df[df['Unnamed: 1'] == 'DOTADO'].index[0]
   idx_empenhado = df[df['Unnamed: 1'] == 'EMPENHADO'].index[0]
   ```

2. **Extrair valores por fonte:**
   ```python
   # Linha de cabeçalhos das fontes (linha 2)
   fontes = [500, 753, 759, 622, 501]

   # Mapear colunas
   # "MODERNIZAÇÃO DO ÓRGÃO" (índice 2) = coluna 500
   # "Unnamed: 3" (índice 3) = coluna 753
   # "Unnamed: 4" (índice 4) = coluna 759
   # "Unnamed: 5" (índice 5) = coluna 622
   # "Unnamed: 6" (índice 6) = coluna 501
   ```

3. **Criar DataFrame estruturado:**
   ```python
   df_balanco = pd.DataFrame({
       'Fonte': [500, 501, 753, 759, 622],
       'Recursos': [recursos[col] for col in cols_fontes],
       'Dotado': [dotado[col] for col in cols_fontes],
       'Empenhado': [empenhado[col] for col in cols_fontes]
   })
   ```

4. **Calcular colunas derivadas:**
   ```python
   df_balanco['Saldo'] = df_balanco['Recursos'] - df_balanco['Empenhado']
   df_balanco['Perc_Execucao'] = (df_balanco['Empenhado'] / df_balanco['Dotado']) * 100
   ```

5. **Adicionar linha de totais:**
   ```python
   total_row = {
       'Fonte': 'TOTAL',
       'Recursos': df_balanco['Recursos'].sum(),
       'Dotado': df_balanco['Dotado'].sum(),
       'Empenhado': df_balanco['Empenhado'].sum(),
       'Saldo': df_balanco['Saldo'].sum(),
       'Perc_Execucao': (df_balanco['Empenhado'].sum() / df_balanco['Dotado'].sum()) * 100
   }
   df_balanco = pd.concat([df_balanco, pd.DataFrame([total_row])], ignore_index=True)
   ```

**DataFrame resultante (clean_balanco):**

```python
Colunas:
- Fonte: int ou str (500, 501, 753, 759, 622, 'TOTAL')
- Recursos: float
- Dotado: float
- Empenhado: float
- Saldo: float (calculado)
- Perc_Execucao: float (calculado)

Shape esperado: (6, 6)  # 5 fontes + 1 linha de total
```

**Valores esperados (validação):**
- Total Recursos: R$ 27.281.568,51
- Total Empenhado: R$ 23.382.410,38
- Saldo Total: R$ 3.899.158,13

---

### 2.3 Aba: PCA 2025 (Post-MVP)

**Dimensões:** 43 linhas × 8 colunas

**Mapeamento de colunas:**

| Coluna Original | Nome Limpo | Tipo | Descrição |
|----------------|-----------|------|-----------|
| `Unnamed: 0` | `Tipo` | str | "Material" ou "Serviço" |
| `Unnamed: 1` | `Item` | int | Número do item |
| `PCA 2025` | `Classe_Grupo` | str | Nome da classe/grupo |
| `Unnamed: 3` | `Valor_Estimado` | float | Valor total estimado |
| `DESEMPENHO PCA 2025` | `Dotado` | float | Valor dotado |
| `Unnamed: 5` | `Empenhado` | float | Valor empenhado |
| `Unnamed: 6` | `Saldo_Dotacao` | float | Saldo para dotação |
| `Unnamed: 7` | `Perc_Execucao` | float | % de execução |

**Transformações:**
- Pular linha 0 (header)
- Linha 1 tem os cabeçalhos
- Calcular `Perc_Execucao = (Empenhado / Valor_Estimado) × 100` se não estiver preenchido

---

## 3. Especificações de Funções

### 3.1 Módulo: `src/data_loader.py`

#### Função: `load_excel_data(filepath: str) -> dict`

**Objetivo:** Carregar todas as abas relevantes do Excel em um dicionário de DataFrames.

**Parâmetros:**
- `filepath` (str): Caminho para o arquivo Excel

**Retorno:**
- `dict[str, pd.DataFrame]`: Dicionário com nome da aba como chave e DataFrame como valor

**Implementação:**

```python
import pandas as pd
import streamlit as st
from typing import Dict

@st.cache_data
def load_excel_data(filepath: str) -> Dict[str, pd.DataFrame]:
    """
    Carrega todas as abas do arquivo Excel de orçamento.

    Args:
        filepath: Caminho para o arquivo ORÇAMENTO 2025.xlsx

    Returns:
        Dicionário com DataFrames de cada aba

    Raises:
        FileNotFoundError: Se arquivo não existir
        ValueError: Se estrutura do Excel for inválida
    """
    try:
        # Carregar todas as abas
        excel_file = pd.ExcelFile(filepath)
        dados = {}

        # Abas críticas para MVP
        abas_mvp = ['CONTROLE DE DESPESAS', 'BALANCO']

        # Abas para versões futuras
        abas_futuras = ['PCA 2025', 'Despesas 2025', 'RECURSOS TESOURO 2025']

        for aba in excel_file.sheet_names:
            try:
                # Carregar sem header para processamento manual
                df = pd.read_excel(excel_file, sheet_name=aba, header=None)
                dados[aba] = df
                print(f"✓ Aba '{aba}' carregada: {df.shape}")
            except Exception as e:
                print(f"⚠️ Erro ao carregar aba '{aba}': {e}")

        # Validar que abas críticas foram carregadas
        for aba in abas_mvp:
            if aba not in dados or dados[aba].empty:
                raise ValueError(f"Aba crítica '{aba}' não encontrada ou vazia")

        return dados

    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    except Exception as e:
        raise ValueError(f"Erro ao carregar Excel: {e}")
```

---

#### Função: `clean_despesas(df_raw: pd.DataFrame) -> pd.DataFrame`

**Objetivo:** Limpar e estruturar aba CONTROLE DE DESPESAS.

**Parâmetros:**
- `df_raw` (pd.DataFrame): DataFrame bruto da aba CONTROLE DE DESPESAS

**Retorno:**
- `pd.DataFrame`: DataFrame limpo e estruturado

**Implementação:**

```python
def clean_despesas(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e estrutura dados da aba CONTROLE DE DESPESAS.

    Args:
        df_raw: DataFrame bruto da aba

    Returns:
        DataFrame limpo com colunas:
        - Processo, Objeto, Valor, Fonte, Elemento, Status, Acao_PCA, Observacao

    Processamento:
        1. Remove linha 0 (vazia)
        2. Usa linha 1 como referência (mas renomeia manualmente)
        3. Remove linhas vazias
        4. Converte tipos de dados
        5. Cria coluna Status derivada
    """
    # Fazer cópia para não modificar original
    df = df_raw.copy()

    # Remover linha 0 (geralmente vazia/header de mesclagem)
    df = df.iloc[1:].reset_index(drop=True)

    # Renomear colunas manualmente (linha 1 tem headers parciais)
    # Baseado na análise: linha 1 tem os nomes verdadeiros
    # Mas vamos usar índices para maior confiabilidade
    df.columns = [
        'Processo',      # Unnamed: 0
        'Objeto',        # Unnamed: 1
        'Valor',         # CONTROLE DE DESPESAS 2025
        'Fonte',         # Unnamed: 3
        'Elemento',      # Unnamed: 4
        'Nota_Reserva',  # Unnamed: 5
        'Nota_Empenho',  # Unnamed: 6
        'Acao_PCA',      # Unnamed: 7
        'Observacao'     # Unnamed: 8
    ]

    # Remover primeira linha (que agora contém os headers antigos)
    df = df.iloc[1:].reset_index(drop=True)

    # Remover linhas onde Processo é vazio
    df = df[df['Processo'].notna() & (df['Processo'] != '')].copy()

    # Converter tipos de dados
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
    df['Fonte'] = pd.to_numeric(df['Fonte'], errors='coerce').astype('Int64')

    # Converter booleanos
    df['Nota_Reserva'] = df['Nota_Reserva'].fillna(False)
    df['Nota_Reserva'] = df['Nota_Reserva'].replace({
        'SIM': True, 'NÃO': False, 'NAO': False,
        True: True, False: False, 1: True, 0: False
    })

    df['Nota_Empenho'] = df['Nota_Empenho'].fillna(False)
    df['Nota_Empenho'] = df['Nota_Empenho'].replace({
        'SIM': True, 'NÃO': False, 'NAO': False,
        True: True, False: False, 1: True, 0: False
    })

    # Criar coluna Status
    def determinar_status(row):
        if pd.isna(row['Valor']) or row['Valor'] == 0:
            return 'Cancelado'
        if pd.notna(row['Observacao']) and 'CANCELADO' in str(row['Observacao']).upper():
            return 'Cancelado'
        if row['Nota_Empenho']:
            return 'Empenhado'
        if row['Nota_Reserva']:
            return 'Reservado'
        return 'Em análise'

    df['Status'] = df.apply(determinar_status, axis=1)

    # Limpar coluna Elemento (uppercase, trim)
    df['Elemento'] = df['Elemento'].str.upper().str.strip()

    # Padronizar elementos
    elemento_map = {
        'CONSUMO': 'CONSUMO',
        'MATERIAL DE CONSUMO': 'CONSUMO',
        'PERMANENTE': 'PERMANENTE',
        'MATERIAL PERMANENTE': 'PERMANENTE',
        'SERVIÇO PJ': 'SERVIÇO PJ',
        'SERVICO PJ': 'SERVIÇO PJ',
        'SERVIÇO PF': 'SERVIÇO PF',
        'SERVICO PF': 'SERVIÇO PF'
    }
    df['Elemento'] = df['Elemento'].replace(elemento_map)

    # Remover colunas auxiliares
    df = df.drop(columns=['Nota_Reserva', 'Nota_Empenho'])

    # Ordenar por Processo
    df = df.sort_values('Processo').reset_index(drop=True)

    return df
```

---

#### Função: `clean_balanco(df_raw: pd.DataFrame) -> pd.DataFrame`

**Objetivo:** Extrair e estruturar dados de saldo por fonte da aba BALANCO.

**Parâmetros:**
- `df_raw` (pd.DataFrame): DataFrame bruto da aba BALANCO

**Retorno:**
- `pd.DataFrame`: DataFrame estruturado com saldos por fonte

**Implementação:**

```python
def clean_balanco(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Extrai dados de saldo por fonte da aba BALANCO.

    Args:
        df_raw: DataFrame bruto da aba BALANCO

    Returns:
        DataFrame com colunas:
        - Fonte, Recursos, Dotado, Empenhado, Saldo, Perc_Execucao

    Processamento:
        1. Localiza linhas com "RECURSOS", "DOTADO", "EMPENHADO"
        2. Extrai valores das 5 fontes (500, 501, 753, 759, 622)
        3. Calcula Saldo e % Execução
        4. Adiciona linha de totais
    """
    df = df_raw.copy()

    # Encontrar linhas-chave (busca flexível)
    idx_recursos = None
    idx_dotado = None
    idx_empenhado = None

    for idx, row in df.iterrows():
        row_str = ' '.join([str(val).upper() for val in row if pd.notna(val)])
        if 'RECURSOS' in row_str and idx_recursos is None:
            idx_recursos = idx
        if 'DOTADO' in row_str and idx_dotado is None:
            idx_dotado = idx
        if 'EMPENHADO' in row_str and idx_empenhado is None:
            idx_empenhado = idx

    if any(x is None for x in [idx_recursos, idx_dotado, idx_empenhado]):
        raise ValueError("Não foi possível localizar linhas de RECURSOS, DOTADO ou EMPENHADO")

    # Identificar colunas das fontes
    # Baseado na análise: linha 2 tem "SALDOS | 500 | 753 | 759 | 622 | 501"
    # Procurar linha com fontes
    idx_header = None
    for idx, row in df.iterrows():
        if '500' in [str(val) for val in row]:
            idx_header = idx
            break

    if idx_header is None:
        # Tentar mapeamento manual baseado na análise
        # "MODERNIZAÇÃO DO ÓRGÃO" (col 2) = 500
        # "Unnamed: 3" (col 3) = 753
        # "Unnamed: 4" (col 4) = 759
        # "Unnamed: 5" (col 5) = 622
        # "Unnamed: 6" (col 6) = 501
        col_map = {
            500: 2,
            753: 3,
            759: 4,
            622: 5,
            501: 6
        }
    else:
        # Criar mapeamento dinâmico
        header_row = df.iloc[idx_header]
        col_map = {}
        for col_idx, val in enumerate(header_row):
            if str(val) in ['500', '501', '753', '759', '622']:
                col_map[int(val)] = col_idx

    # Extrair valores
    fontes = [500, 753, 759, 622, 501]
    dados_balanco = []

    for fonte in fontes:
        if fonte in col_map:
            col_idx = col_map[fonte]
            recursos = pd.to_numeric(df.iloc[idx_recursos, col_idx], errors='coerce')
            dotado = pd.to_numeric(df.iloc[idx_dotado, col_idx], errors='coerce')
            empenhado = pd.to_numeric(df.iloc[idx_empenhado, col_idx], errors='coerce')

            dados_balanco.append({
                'Fonte': fonte,
                'Recursos': recursos if pd.notna(recursos) else 0,
                'Dotado': dotado if pd.notna(dotado) else 0,
                'Empenhado': empenhado if pd.notna(empenhado) else 0
            })

    # Criar DataFrame
    df_balanco = pd.DataFrame(dados_balanco)

    # Calcular colunas derivadas
    df_balanco['Saldo'] = df_balanco['Recursos'] - df_balanco['Empenhado']
    df_balanco['Perc_Execucao'] = (df_balanco['Empenhado'] / df_balanco['Dotado']) * 100
    df_balanco['Perc_Execucao'] = df_balanco['Perc_Execucao'].fillna(0)

    # Adicionar linha de totais
    total = {
        'Fonte': 'TOTAL',
        'Recursos': df_balanco['Recursos'].sum(),
        'Dotado': df_balanco['Dotado'].sum(),
        'Empenhado': df_balanco['Empenhado'].sum(),
        'Saldo': df_balanco['Saldo'].sum(),
        'Perc_Execucao': (df_balanco['Empenhado'].sum() / df_balanco['Dotado'].sum()) * 100 if df_balanco['Dotado'].sum() > 0 else 0
    }

    df_balanco = pd.concat([df_balanco, pd.DataFrame([total])], ignore_index=True)

    return df_balanco
```

---

### 3.2 Módulo: `src/data_processor.py`

#### Função: `gerar_metricas_kpi(df_balanco: pd.DataFrame, df_despesas: pd.DataFrame) -> dict`

**Objetivo:** Calcular os 5 KPIs principais do dashboard.

**Parâmetros:**
- `df_balanco` (pd.DataFrame): DataFrame de saldos por fonte
- `df_despesas` (pd.DataFrame): DataFrame de despesas

**Retorno:**
- `dict`: Dicionário com métricas

**Implementação:**

```python
from typing import Dict

def gerar_metricas_kpi(df_balanco: pd.DataFrame, df_despesas: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula KPIs principais do dashboard.

    Args:
        df_balanco: DataFrame com saldos por fonte
        df_despesas: DataFrame com despesas

    Returns:
        dict com:
        - total_recursos: Total de recursos disponíveis
        - total_empenhado: Total empenhado
        - saldo_disponivel: Saldo restante
        - total_processos: Número de processos ativos
        - taxa_execucao: % média de execução
    """
    # Pegar linha de totais (última linha)
    total_row = df_balanco[df_balanco['Fonte'] == 'TOTAL'].iloc[0]

    # Processos ativos (excluindo cancelados)
    processos_ativos = len(df_despesas[df_despesas['Status'] != 'Cancelado'])

    return {
        'total_recursos': total_row['Recursos'],
        'total_empenhado': total_row['Empenhado'],
        'saldo_disponivel': total_row['Saldo'],
        'total_processos': processos_ativos,
        'taxa_execucao': total_row['Perc_Execucao'],
        'perc_execucao': total_row['Perc_Execucao']  # Alias
    }
```

---

#### Função: `calcular_saldos_por_fonte(df_balanco: pd.DataFrame) -> pd.DataFrame`

**Objetivo:** Retornar DataFrame de saldos por fonte (já processado em clean_balanco).

**Implementação:**

```python
def calcular_saldos_por_fonte(df_balanco: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna saldos por fonte (wrapper/validação).

    Args:
        df_balanco: DataFrame já processado de clean_balanco()

    Returns:
        DataFrame com saldos por fonte
    """
    # Validar estrutura
    required_cols = ['Fonte', 'Recursos', 'Dotado', 'Empenhado', 'Saldo', 'Perc_Execucao']
    if not all(col in df_balanco.columns for col in required_cols):
        raise ValueError(f"DataFrame balanco deve ter colunas: {required_cols}")

    return df_balanco.copy()
```

---

#### Função: `calcular_orcado_vs_executado(df_despesas: pd.DataFrame, granularidade: str = 'Elemento') -> pd.DataFrame`

**Objetivo:** Comparar orçado vs executado por granularidade especificada.

**Parâmetros:**
- `df_despesas` (pd.DataFrame): DataFrame de despesas
- `granularidade` (str): "Elemento", "Fonte" ou "Acao_PCA"

**Retorno:**
- `pd.DataFrame`: Comparativo orçado vs executado

**Implementação:**

```python
def calcular_orcado_vs_executado(
    df_despesas: pd.DataFrame,
    df_balanco: pd.DataFrame,
    granularidade: str = 'Elemento'
) -> pd.DataFrame:
    """
    Calcula comparativo orçado vs executado por granularidade.

    Args:
        df_despesas: DataFrame de despesas
        df_balanco: DataFrame de saldos (para obter dotado)
        granularidade: Dimensão de agregação ("Elemento", "Fonte", "Acao_PCA")

    Returns:
        DataFrame com colunas:
        - Categoria, Orcado, Executado, Saldo, Perc_Execucao

    Para MVP: apenas granularidade "Elemento" é implementada
    """
    if granularidade not in ['Elemento', 'Fonte', 'Acao_PCA']:
        raise ValueError(f"Granularidade inválida: {granularidade}")

    # Filtrar apenas processos ativos (não cancelados)
    df_ativos = df_despesas[df_despesas['Status'] != 'Cancelado'].copy()

    if granularidade == 'Elemento':
        # Agregar por elemento
        agregado = df_ativos.groupby('Elemento').agg({
            'Valor': 'sum'
        }).reset_index()
        agregado.columns = ['Categoria', 'Executado']

        # Para MVP: Orçado = Dotado total / número de elementos (simplificação)
        # Versão futura: mapear orçado específico de cada elemento
        dotado_total = df_balanco[df_balanco['Fonte'] != 'TOTAL']['Dotado'].sum()
        n_elementos = len(agregado)

        agregado['Orcado'] = dotado_total / n_elementos  # Simplificação MVP

    elif granularidade == 'Fonte':
        # Agregar por fonte
        agregado = df_ativos.groupby('Fonte').agg({
            'Valor': 'sum'
        }).reset_index()
        agregado.columns = ['Categoria', 'Executado']

        # Merge com balanco para pegar Dotado correto
        balanco_map = df_balanco[df_balanco['Fonte'] != 'TOTAL'].set_index('Fonte')['Dotado'].to_dict()
        agregado['Orcado'] = agregado['Categoria'].map(balanco_map)

    else:  # Acao_PCA
        agregado = df_ativos.groupby('Acao_PCA').agg({
            'Valor': 'sum'
        }).reset_index()
        agregado.columns = ['Categoria', 'Executado']
        agregado['Orcado'] = 0  # Requer dados do PCA 2025 (Post-MVP)

    # Calcular métricas
    agregado['Saldo'] = agregado['Orcado'] - agregado['Executado']
    agregado['Perc_Execucao'] = (agregado['Executado'] / agregado['Orcado']) * 100
    agregado['Perc_Execucao'] = agregado['Perc_Execucao'].fillna(0)

    # Ordenar por executado (decrescente)
    agregado = agregado.sort_values('Executado', ascending=False).reset_index(drop=True)

    return agregado
```

---

### 3.3 Módulo: `src/utils.py`

#### Funções de Formatação

```python
def formatar_moeda(valor: float) -> str:
    """
    Formata valor em moeda brasileira.

    Args:
        valor: Valor numérico

    Returns:
        String formatada (ex: "R$ 1.234.567,89")
    """
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


def formatar_percentual(valor: float, casas_decimais: int = 1) -> str:
    """
    Formata valor em percentual.

    Args:
        valor: Valor numérico (ex: 85.7)
        casas_decimais: Número de casas decimais

    Returns:
        String formatada (ex: "85,7%")
    """
    return f"{valor:.{casas_decimais}f}%".replace('.', ',')


def aplicar_filtros(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    """
    Aplica múltiplos filtros ao DataFrame.

    Args:
        df: DataFrame original
        filtros: Dicionário {coluna: [valores permitidos]}

    Returns:
        DataFrame filtrado

    Exemplo:
        filtros = {
            'Fonte': [500, 753],
            'Status': ['Empenhado', 'Reservado']
        }
    """
    df_filtrado = df.copy()

    for coluna, valores in filtros.items():
        if coluna in df_filtrado.columns and valores:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]

    return df_filtrado
```

#### Constantes

```python
# Cores padrão do dashboard
CORES_PADRAO = {
    'azul': '#1f77b4',
    'verde': '#2ca02c',
    'amarelo': '#ffbb33',
    'vermelho': '#d62728',
    'cinza': '#7f7f7f',
    'laranja': '#ff7f0e',
    'roxo': '#9467bd'
}

# Cores por fonte de recursos
CORES_FONTES = {
    500: '#1f77b4',  # Azul
    501: '#ff7f0e',  # Laranja
    753: '#2ca02c',  # Verde
    759: '#d62728',  # Vermelho
    622: '#9467bd'   # Roxo
}

# Nomes das fontes
NOMES_FONTES = {
    500: 'Tesouro (500)',
    501: 'Tesouro DREM (501)',
    753: 'Convênios/Taxas (753)',
    759: 'Fundos (759)',
    622: 'SUS (622)'
}

# Elementos de despesa
ELEMENTOS_DESPESA = [
    'CONSUMO',
    'PERMANENTE',
    'SERVIÇO PJ',
    'SERVIÇO PF'
]

# Status de processos
STATUS_PROCESSOS = [
    'Empenhado',
    'Reservado',
    'Em análise',
    'Cancelado'
]
```

---

### 3.4 Módulo: `src/visualizations.py`

#### Função: `grafico_saldo_por_fonte(df_saldos: pd.DataFrame) -> go.Figure`

**Objetivo:** Criar gráfico de barras agrupadas com saldos por fonte.

**Implementação:**

```python
import plotly.graph_objects as go
from src.utils import CORES_FONTES, NOMES_FONTES

def grafico_saldo_por_fonte(df_saldos: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras agrupadas com saldos por fonte.

    Args:
        df_saldos: DataFrame com saldos por fonte

    Returns:
        Figura Plotly
    """
    # Remover linha de total para visualização
    df = df_saldos[df_saldos['Fonte'] != 'TOTAL'].copy()

    # Criar figura
    fig = go.Figure()

    # Adicionar barras para cada métrica
    fig.add_trace(go.Bar(
        name='Recursos',
        x=df['Fonte'],
        y=df['Recursos'],
        marker_color='#1f77b4',
        text=df['Recursos'].apply(lambda x: f'R$ {x:,.0f}'),
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        name='Dotado',
        x=df['Fonte'],
        y=df['Dotado'],
        marker_color='#ff7f0e',
        text=df['Dotado'].apply(lambda x: f'R$ {x:,.0f}'),
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        name='Empenhado',
        x=df['Fonte'],
        y=df['Empenhado'],
        marker_color='#2ca02c',
        text=df['Empenhado'].apply(lambda x: f'R$ {x:,.0f}'),
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        name='Saldo',
        x=df['Fonte'],
        y=df['Saldo'],
        marker_color='#9467bd',
        text=df['Saldo'].apply(lambda x: f'R$ {x:,.0f}'),
        textposition='outside'
    ))

    # Layout
    fig.update_layout(
        title='Saldo Disponível por Fonte de Recursos',
        xaxis_title='Fonte de Recursos',
        yaxis_title='Valores (R$)',
        barmode='group',
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig
```

---

## 4. Validação e Testes

### 4.1 Checklist de Validação de Dados

**Valores a validar (comparar Dashboard vs Excel):**

| # | Métrica | Localização Excel | Valor Esperado | Tolerância |
|---|---------|-------------------|----------------|------------|
| 1 | Total Recursos | BALANCO, linha RECURSOS, coluna SOMATÓRIO | R$ 27.281.568,51 | ±R$ 1,00 |
| 2 | Total Empenhado | BALANCO, linha EMPENHADO, coluna SOMATÓRIO | R$ 23.382.410,38 | ±R$ 1,00 |
| 3 | Recursos Fonte 500 | BALANCO, linha RECURSOS, coluna 500 | R$ 15.911.610,00 | ±R$ 1,00 |
| 4 | Empenhado Fonte 500 | BALANCO, linha EMPENHADO, coluna 500 | R$ 15.899.799,31 | ±R$ 1,00 |
| 5 | Saldo Fonte 500 | Calculado: Recursos - Empenhado | R$ 11.810,69 | ±R$ 1,00 |
| 6 | % Execução Fonte 500 | (Empenhado / Dotado) × 100 | ~99,9% | ±0,1% |
| 7 | Número de processos | Contagem em CONTROLE DE DESPESAS | ~279 (excluindo vazios) | N/A |
| 8 | Processos Empenhados | Contagem onde Nota_Empenho = True | (verificar no Excel) | N/A |
| 9 | Valor específico processo | Ex: E:01203.0000000498/2025 | R$ 32.709,00 | ±R$ 0,01 |
| 10 | Total por elemento | Agregação em CONTROLE DE DESPESAS | (somar no Excel) | ±R$ 10,00 |

---

### 4.2 Casos de Teste Unitários

```python
# test_data_loader.py

import pytest
import pandas as pd
from src.data_loader import clean_despesas, clean_balanco

def test_clean_despesas():
    """Testa limpeza da aba CONTROLE DE DESPESAS"""
    # Mock data
    df_raw = pd.DataFrame({
        'Unnamed: 0': [None, 'NÚMERO DO PROCESSO', 'E:01203.0000000498/2025'],
        'Unnamed: 1': [None, 'OBJETO', 'Água mineral'],
        'CONTROLE DE DESPESAS 2025': [None, 'VALOR', 32709],
        'Unnamed: 3': [None, 'FONTE', 500],
        'Unnamed: 4': [None, 'ELEMENTO DE DESPESA', 'CONSUMO'],
        'Unnamed: 5': [None, 'NOTA DE RESERVA', False],
        'Unnamed: 6': [None, 'NOTA DE EMPENHO', True],
        'Unnamed: 7': [None, 'AÇÃO DO PCA2025', 'Expediente'],
        'Unnamed: 8': [None, 'OBSERVAÇÃO', None]
    })

    df_clean = clean_despesas(df_raw)

    # Verificações
    assert len(df_clean) == 1  # Apenas 1 linha de dados (excluindo headers)
    assert df_clean.iloc[0]['Processo'] == 'E:01203.0000000498/2025'
    assert df_clean.iloc[0]['Valor'] == 32709
    assert df_clean.iloc[0]['Status'] == 'Empenhado'
    assert 'Processo' in df_clean.columns
    assert 'Status' in df_clean.columns

def test_clean_balanco():
    """Testa extração da aba BALANCO"""
    # Mock data (simplificado)
    # ... implementar mock ...
    pass
```

---

## 5. Performance e Otimização

### 5.1 Estratégias de Cache

```python
# app.py

import streamlit as st

# Cache de carregamento de dados (persiste entre reruns)
@st.cache_data
def carregar_dados(caminho):
    dados = load_excel_data(caminho)
    return dados

# Cache de processamento (atualiza quando dados mudam)
@st.cache_data
def processar_dados(dados):
    df_despesas = clean_despesas(dados['CONTROLE DE DESPESAS'])
    df_saldos = calcular_saldos_por_fonte(clean_balanco(dados['BALANCO']))
    return df_despesas, df_saldos
```

### 5.2 Benchmarks de Performance

| Operação | Meta | Medição |
|----------|------|---------|
| Carregamento Excel | < 2s | `time.time()` antes/depois |
| Limpeza de dados | < 1s | Incluído no carregamento |
| Renderização gráfico | < 500ms | Profiling Streamlit |
| Aplicação de filtros | < 200ms | Teste com 5 fontes selecionadas |
| Exportação CSV | < 1s | Teste com 279 linhas |

---

## 6. Tratamento de Erros

### 6.1 Erros Esperados e Respostas

| Erro | Causa | Resposta |
|------|-------|----------|
| `FileNotFoundError` | Excel não encontrado | Mostrar mensagem: "Arquivo ORÇAMENTO 2025.xlsx não encontrado. Verifique o caminho." |
| `ValueError: Aba não encontrada` | Estrutura do Excel mudou | Mostrar mensagem: "Estrutura do Excel inválida. Verifique se a aba CONTROLE DE DESPESAS existe." |
| `KeyError` em colunas | Colunas renomeadas no Excel | Logar erro e mostrar: "Erro ao processar dados. Entre em contato com o suporte." |
| Dados vazios | Planilha sem dados | Mostrar: "Nenhum dado encontrado na planilha." |
| Valores negativos inesperados | Erro de digitação no Excel | Destacar visualmente no dashboard |

### 6.2 Logs de Debug

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Uso:
logger.info(f"Carregando Excel: {filepath}")
logger.warning(f"Coluna 'Fonte' tem {n_nulos} valores nulos")
logger.error(f"Erro ao processar aba {aba_name}: {e}")
```

---

## 7. Roadmap de Implementação

### Ordem de Desenvolvimento Recomendada

1. ✅ **Documentação** (concluída)
2. ⏳ **Setup** (próximo)
   - requirements.txt
   - .gitignore
   - Estrutura de pastas
3. ⏳ **Backend - data_loader.py**
   - load_excel_data()
   - clean_despesas()
   - clean_balanco()
   - Testes unitários
4. ⏳ **Backend - data_processor.py**
   - gerar_metricas_kpi()
   - calcular_saldos_por_fonte()
   - calcular_orcado_vs_executado()
5. ⏳ **Backend - utils.py**
   - Funções de formatação
   - Constantes
6. ⏳ **Frontend - visualizations.py**
   - grafico_saldo_por_fonte()
   - grafico_orcado_vs_executado()
   - tabela_interativa_despesas()
7. ⏳ **Frontend - app.py**
   - Configuração Streamlit
   - Sidebar
   - Seções do dashboard
   - Integração com backend
8. ⏳ **Testes e Validação**
   - Validação dos 10 valores-chave
   - Testes de performance
   - Ajustes de UX
9. ⏳ **Documentação Final**
   - README.md completo
   - Screenshots
   - Guia de uso

---

**Documento elaborado por:** Claude Code
**Revisão:** v1.0 - 11/02/2026
**Status:** ✅ Concluído
