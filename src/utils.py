"""
Módulo de Utilidades
Dashboard de Controle Orçamentário DAL/CBMAL

Funções auxiliares e constantes compartilhadas
"""

import pandas as pd
from typing import Dict, List


def formatar_moeda(valor: float) -> str:
    """
    Formata valor em moeda brasileira.

    Args:
        valor: Valor numérico

    Returns:
        String formatada (ex: "R$ 1.234.567,89")

    Examples:
        >>> formatar_moeda(1234567.89)
        'R$ 1.234.567,89'
        >>> formatar_moeda(0)
        'R$ 0,00'
    """
    if pd.isna(valor):
        return "R$ 0,00"

    # Formatar com separadores
    formatado = f"{valor:,.2f}"

    # Trocar separadores (padrão US para BR)
    formatado = formatado.replace(',', 'X').replace('.', ',').replace('X', '.')

    return f"R$ {formatado}"


def formatar_percentual(valor: float, casas_decimais: int = 1) -> str:
    """
    Formata valor em percentual.

    Args:
        valor: Valor numérico (ex: 85.7)
        casas_decimais: Número de casas decimais (padrão: 1)

    Returns:
        String formatada (ex: "85,7%")

    Examples:
        >>> formatar_percentual(85.7)
        '85,7%'
        >>> formatar_percentual(100.0, 2)
        '100,00%'
    """
    if pd.isna(valor):
        return "0,0%"

    formatado = f"{valor:.{casas_decimais}f}%"
    formatado = formatado.replace('.', ',')

    return formatado


def aplicar_filtros(df: pd.DataFrame, filtros: Dict[str, List]) -> pd.DataFrame:
    """
    Aplica múltiplos filtros ao DataFrame.

    Args:
        df: DataFrame original
        filtros: Dicionário {coluna: [valores permitidos]}

    Returns:
        DataFrame filtrado

    Examples:
        >>> filtros = {
        ...     'Fonte': [500, 753],
        ...     'Status': ['Empenhado', 'Reservado']
        ... }
        >>> df_filtrado = aplicar_filtros(df, filtros)
    """
    df_filtrado = df.copy()

    for coluna, valores in filtros.items():
        if coluna in df_filtrado.columns and valores:
            # Filtrar apenas se há valores selecionados
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]

    return df_filtrado


def validar_valores_esperados(df_balanco: pd.DataFrame) -> Dict[str, bool]:
    """
    Valida se os valores calculados batem com valores esperados do Excel.

    Args:
        df_balanco: DataFrame com saldos por fonte

    Returns:
        Dicionário com resultados da validação

    Valores esperados (aproximados):
        - Total Recursos: R$ 27.281.568,51
        - Total Empenhado: R$ 23.382.410,38
    """
    # Pegar linha de totais
    total_row = df_balanco[df_balanco['Fonte'] == 'TOTAL']

    if total_row.empty:
        return {
            'total_recursos': False,
            'total_empenhado': False,
            'mensagem': 'Linha de TOTAL não encontrada'
        }

    total_recursos = total_row.iloc[0]['Recursos']
    total_empenhado = total_row.iloc[0]['Empenhado']

    # Tolerância de R$ 100 para arredondamentos
    tolerancia = 100

    recursos_ok = abs(total_recursos - 27281568.51) < tolerancia
    empenhado_ok = abs(total_empenhado - 23382410.38) < tolerancia

    return {
        'total_recursos': recursos_ok,
        'total_empenhado': empenhado_ok,
        'valor_recursos': total_recursos,
        'valor_empenhado': total_empenhado,
        'mensagem': 'Validação concluída'
    }


# =============================================================================
# CONSTANTES
# =============================================================================

# Cores padrão do dashboard (Paleta Premium v3.0 — Suavizada)
# Tons mais suaves e confortáveis para dark mode
CORES_PADRAO = {
    # ── Cores institucionais (suavizadas para dark mode) ──
    'vermelho_cbmal': '#D32F2F',    # Vermelho suave (era #C10A0A)
    'amarelo_cbmal': '#FFB300',     # Âmbar dourado (era #FFFF00 — muito forte)
    'azul_destaque': '#5C9DED',     # Azul céu suave (era #4A94FF)
    'azul_escuro': '#3D7DD9',       # Azul médio (era #0017FF — muito intenso)
    'vermelho_vivo': '#EF5350',     # Vermelho coral (era #FF1A24)
    'amarelo_ouro': '#FB8C00',      # Laranja dourado (era #FF8000)
    'verde_militar': '#43A047',     # Verde equilibrado (era #4B5320 — muito escuro)
    'cinza_brasao': '#9BA4B5',      # Cinza azulado (era #B5B5B5)

    # Mapeamento para compatibilidade com código existente
    'azul': '#5C9DED',              # Azul céu suave
    'verde': '#43A047',             # Verde limpo e legível
    'amarelo': '#FFB300',           # Âmbar dourado (legível em dark)
    'vermelho': '#D32F2F',          # Vermelho suave
    'vermelho_critico': '#EF5350', # Vermelho coral (alertas críticos)
    'cinza': '#9BA4B5',             # Cinza azulado
    'laranja': '#FB8C00',           # Laranja dourado
    'roxo': '#AB47BC',              # Roxo vibrante mas suave (era #9467bd)
    'rosa': '#EC407A',              # Rosa moderno (era #e377c2)
    'marrom': '#8D6E63',            # Marrom quente (era #8c564b)
    'verde_claro': '#66BB6A'        # Verde claro amigável (era #bcbd22)
}


# Cores por fonte de recursos (Paleta Premium v3.0)
CORES_FONTES = {
    500: '#5C9DED',  # Azul céu suave (Tesouro)
    501: '#EF5350',  # Vermelho coral (DREM)
    753: '#43A047',  # Verde equilibrado (Convênios)
    759: '#FFB300',  # Âmbar dourado (Fundos)
    622: '#AB47BC'   # Roxo suave (SUS)
}

# Nomes legíveis das fontes
NOMES_FONTES = {
    500: '500 - Tesouro',
    501: '501 - Tesouro DREM',
    753: '753 - Convênios/Taxas',
    759: '759 - Fundos',
    622: '622 - SUS'
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

# Cores por status (Paleta Premium v3.0)
CORES_STATUS = {
    'Empenhado': '#43A047',     # Verde equilibrado (OK)
    'Reservado': '#FFB300',     # Âmbar dourado (Aguardando)
    'Em análise': '#5C9DED',    # Azul suave (Em andamento)
    'Cancelado': '#78909C'      # Cinza-azulado (Inativo)
}

# Configuração de página Streamlit
PAGE_CONFIG = {
    'page_title': 'Dashboard Orçamentário DAL/CBMAL',
    'page_icon': '📊',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Textos padrão
TEXTOS = {
    'titulo_principal': '📊 Dashboard de Controle Orçamentário',
    'subtitulo': '**Diretoria de Apoio Logístico - CBMAL** | Orçamento 2025',
    'rodape': 'Dashboard desenvolvido em Python com Streamlit + Plotly + Pandas | Dados atualizados manualmente',
    'erro_arquivo': '❌ Arquivo ORÇAMENTO 2025 (1).xlsx não encontrado na pasta data/',
    'erro_carregamento': '❌ Erro ao carregar dados. Verifique o arquivo Excel.',
    'sucesso_carregamento': '✅ Dados carregados com sucesso!',
    'aguarde': '⏳ Carregando dados...'
}
