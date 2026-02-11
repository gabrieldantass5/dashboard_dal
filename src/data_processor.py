"""
Módulo de Processamento de Dados
Dashboard de Controle Orçamentário DAL/CBMAL

Responsável por:
- Calcular métricas e KPIs
- Agregar dados por diferentes dimensões
- Gerar comparativos e análises
"""

import pandas as pd
import logging
from typing import Dict

# Configurar logging
logger = logging.getLogger(__name__)


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
        - perc_execucao: Alias para taxa_execucao

    Examples:
        >>> metricas = gerar_metricas_kpi(df_balanco, df_despesas)
        >>> print(f"Total: {metricas['total_recursos']}")
    """
    logger.info("📊 Gerando métricas KPI...")

    # Pegar linha de totais (última linha ou onde Fonte == 'TOTAL')
    total_row = df_balanco[df_balanco['Fonte'] == 'TOTAL']

    if total_row.empty:
        logger.warning("   ⚠️  Linha de TOTAL não encontrada, usando soma manual")
        total_row = df_balanco[df_balanco['Fonte'] != 'TOTAL'].sum()
        total_recursos = total_row['Recursos']
        total_empenhado = total_row['Empenhado']
        total_saldo = total_row['Saldo']
        taxa_exec = (total_empenhado / total_row['Dotado']) * 100 if total_row['Dotado'] > 0 else 0
    else:
        total_row = total_row.iloc[0]
        total_recursos = total_row['Recursos']
        total_empenhado = total_row['Empenhado']
        total_saldo = total_row['Saldo']
        taxa_exec = total_row['Perc_Execucao']

    # Processos ativos (excluindo cancelados)
    processos_ativos = len(df_despesas[df_despesas['Status'] != 'Cancelado'])

    # Total de processos (incluindo todos)
    total_todos_processos = len(df_despesas)

    metricas = {
        'total_recursos': total_recursos,
        'total_empenhado': total_empenhado,
        'saldo_disponivel': total_saldo,
        'total_processos': processos_ativos,
        'total_processos_geral': total_todos_processos,
        'taxa_execucao': taxa_exec,
        'perc_execucao': taxa_exec  # Alias
    }

    # Log das métricas
    logger.info(f"   ✓ Total Recursos: R$ {total_recursos:,.2f}")
    logger.info(f"   ✓ Total Empenhado: R$ {total_empenhado:,.2f}")
    logger.info(f"   ✓ Saldo Disponível: R$ {total_saldo:,.2f}")
    logger.info(f"   ✓ Processos Ativos: {processos_ativos}")
    logger.info(f"   ✓ Taxa de Execução: {taxa_exec:.2f}%")

    return metricas


def calcular_saldos_por_fonte(df_balanco: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna saldos por fonte (wrapper/validação).

    Args:
        df_balanco: DataFrame já processado de clean_balanco()

    Returns:
        DataFrame com saldos por fonte

    Raises:
        ValueError: Se estrutura do DataFrame for inválida
    """
    # Validar estrutura
    required_cols = ['Fonte', 'Recursos', 'Dotado', 'Empenhado', 'Saldo', 'Perc_Execucao']

    if not all(col in df_balanco.columns for col in required_cols):
        missing_cols = [col for col in required_cols if col not in df_balanco.columns]
        raise ValueError(f"DataFrame balanco deve ter colunas: {required_cols}. Faltando: {missing_cols}")

    return df_balanco.copy()


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

    Para MVP: apenas granularidade "Elemento" é implementada com dados reais
    """
    logger.info(f"📊 Calculando orçado vs executado por {granularidade}...")

    if granularidade not in ['Elemento', 'Fonte', 'Acao_PCA']:
        raise ValueError(f"Granularidade inválida: {granularidade}. Use 'Elemento', 'Fonte' ou 'Acao_PCA'")

    # Filtrar apenas processos ativos (não cancelados)
    df_ativos = df_despesas[df_despesas['Status'] != 'Cancelado'].copy()

    if granularidade == 'Elemento':
        # Agregar por elemento
        agregado = df_ativos.groupby('Elemento').agg({
            'Valor': 'sum'
        }).reset_index()
        agregado.columns = ['Categoria', 'Executado']

        # Para MVP: Orçado = Dotado total / número de elementos (simplificação)
        # Versão futura: mapear orçado específico de cada elemento da aba AUX BALANCO
        dotado_total = df_balanco[df_balanco['Fonte'] != 'TOTAL']['Dotado'].sum()

        # Distribuição proporcional (simplificação MVP)
        # Na v2.0, buscar da aba AUX BALANCO que tem dotado por elemento
        agregado['Orcado'] = dotado_total / len(agregado) if len(agregado) > 0 else 0

        logger.info(f"   Granularidade Elemento: {len(agregado)} categorias")

    elif granularidade == 'Fonte':
        # Agregar por fonte
        agregado = df_ativos.groupby('Fonte').agg({
            'Valor': 'sum'
        }).reset_index()
        agregado.columns = ['Categoria', 'Executado']

        # Merge com balanco para pegar Dotado correto
        balanco_fontes = df_balanco[df_balanco['Fonte'] != 'TOTAL'].copy()
        balanco_map = balanco_fontes.set_index('Fonte')['Dotado'].to_dict()

        agregado['Orcado'] = agregado['Categoria'].map(balanco_map).fillna(0)

        logger.info(f"   Granularidade Fonte: {len(agregado)} categorias")

    else:  # Acao_PCA
        # Agregar por ação do PCA
        agregado = df_ativos.groupby('Acao_PCA').agg({
            'Valor': 'sum'
        }).reset_index()
        agregado.columns = ['Categoria', 'Executado']

        # Para MVP: Orçado = 0 (requer dados do PCA 2025 - Post-MVP)
        agregado['Orcado'] = 0

        logger.warning("   ⚠️  Granularidade Acao_PCA: orçado não disponível (Post-MVP)")
        logger.info(f"   Granularidade Acao_PCA: {len(agregado)} categorias")

    # Calcular métricas
    agregado['Saldo'] = agregado['Orcado'] - agregado['Executado']
    agregado['Perc_Execucao'] = (agregado['Executado'] / agregado['Orcado']) * 100
    agregado['Perc_Execucao'] = agregado['Perc_Execucao'].replace([float('inf'), -float('inf')], 0).fillna(0)

    # Ordenar por executado (decrescente)
    agregado = agregado.sort_values('Executado', ascending=False).reset_index(drop=True)

    # Log de estatísticas
    categorias_acima_95 = len(agregado[agregado['Perc_Execucao'] > 95])
    if categorias_acima_95 > 0:
        logger.warning(f"   ⚠️  {categorias_acima_95} categoria(s) com execução > 95%")

    return agregado


def processar_status_processos(df_despesas: pd.DataFrame) -> pd.DataFrame:
    """
    Processa contagem de processos por status.

    Args:
        df_despesas: DataFrame de despesas

    Returns:
        DataFrame com colunas:
        - Status, Quantidade, Valor_Total, Percentual

    Nota: Implementação para Post-MVP (v2.0)
    """
    logger.info("📊 Processando status de processos...")

    # Agregar por status
    agregado = df_despesas.groupby('Status').agg({
        'Processo': 'count',
        'Valor': 'sum'
    }).reset_index()

    agregado.columns = ['Status', 'Quantidade', 'Valor_Total']

    # Calcular percentual
    total_processos = agregado['Quantidade'].sum()
    agregado['Percentual'] = (agregado['Quantidade'] / total_processos) * 100 if total_processos > 0 else 0

    # Ordenar por quantidade (decrescente)
    agregado = agregado.sort_values('Quantidade', ascending=False).reset_index(drop=True)

    logger.info(f"   ✓ Processado: {len(agregado)} status diferentes")

    return agregado


def calcular_execucao_pca(df_pca: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula % de execução por classe/grupo do PCA.

    Args:
        df_pca: DataFrame da aba PCA 2025 (já limpo por clean_pca)

    Returns:
        DataFrame com colunas:
        - Acao (nome da ação), Previsto (valor estimado), 
          Executado (empenhado), Perc_Execucao

    Processamento:
        1. Agrupa por Classe_Grupo se necessário
        2. Calcula percentual de execução
        3. Ordena por percentual (decrescente)
    """
    logger.info("📊 Calculando execução PCA...")

    if df_pca.empty:
        logger.warning("   ⚠️  DataFrame PCA vazio")
        return pd.DataFrame()

    # Criar DataFrame de saída
    df_exec = df_pca.copy()

    # Renomear colunas para padrão esperado pelo gráfico
    df_exec = df_exec.rename(columns={
        'Classe_Grupo': 'Acao',
        'Valor_Estimado': 'Previsto',
        'Empenhado': 'Executado'
    })

    # Selecionar apenas colunas relevantes
    colunas_saida = ['Acao', 'Previsto', 'Executado', 'Perc_Execucao']
    df_exec = df_exec[colunas_saida].copy()

    # Remover linhas com ação vazia ou "nan"
    df_exec = df_exec[
        (df_exec['Acao'].notna()) & 
        (df_exec['Acao'] != 'nan') &
        (df_exec['Acao'] != '')
    ].copy()

    # Ordenar por percentual de execução (decrescente)
    df_exec = df_exec.sort_values('Perc_Execucao', ascending=False).reset_index(drop=True)

    # Limitar a top 15 para melhor visualização
    if len(df_exec) > 15:
        logger.info(f"   Limitando visualização a top 15 de {len(df_exec)} ações")
        df_exec = df_exec.head(15)

    # Estatísticas
    exec_media = df_exec['Perc_Execucao'].mean()
    acoes_concluidas = len(df_exec[df_exec['Perc_Execucao'] >= 100])
    acoes_criticas = len(df_exec[df_exec['Perc_Execucao'] < 50])

    logger.info(f"   ✓ Ações processadas: {len(df_exec)}")
    logger.info(f"   ✓ Execução média: {exec_media:.1f}%")
    logger.info(f"   ✓ Ações concluídas (≥100%): {acoes_concluidas}")
    logger.info(f"   ✓ Ações críticas (\u003c50%): {acoes_criticas}")

    return df_exec


def simular_evolucao_temporal(df_balanco: pd.DataFrame) -> pd.DataFrame:
    """
    Simula dados de evolução temporal mensal (F8).
    
    Args:
        df_balanco: DataFrame com saldos (para calcular meta)
    
    Returns:
        DataFrame com colunas: Mes, Empenhado_Acumulado, Meta
    
    Nota: Função temporária até haver dados históricos reais
    """
    logger.info("📊 Simulando evolução temporal (F8 - dados mockados)...")
    
    # Pegar total empenhado atual
    total_empenhado = df_balanco[df_balanco['Fonte'] == 'TOTAL']['Empenhado'].values[0]
    total_dotado = df_balanco[df_balanco['Fonte'] == 'TOTAL']['Dotado'].values[0]
    
    # Simular execução mensal (janeiro e fevereiro)
    meses = ['Jan', 'Fev']
    
    # Assumir que em janeiro foi empenhado 60% do total atual
    # E em fevereiro os 40% restantes
    empenhado_jan = total_empenhado * 0.60
    empenhado_fev = total_empenhado
    
    # Meta linear: 1/12 do dotado por mês
    meta_mensal = total_dotado / 12
    
    dados = []
    for idx, mes in enumerate(meses, 1):
        empenhado_acum = empenhado_jan if idx == 1 else empenhado_fev
        meta_acum = meta_mensal * idx
        
        dados.append({
            'Mes': mes,
            'Empenhado_Acumulado': empenhado_acum,
            'Meta': meta_acum
        })
    
    df_temporal = pd.DataFrame(dados)
    
    logger.info(f"   ✓ Dados temporais simulados: {len(df_temporal)} meses")
    
    return df_temporal


def simular_comparativo_anos(df_balanco: pd.DataFrame) -> pd.DataFrame:
    """
    Simula dados comparativos com anos anteriores (F9).
    
    Args:
        df_balanco: DataFrame com saldos de 2025
    
    Returns:
        DataFrame com colunas: Categoria, Ano_2025, Ano_2024, Ano_2023
    
    Nota: Função temporária até haver dados de 2024 e 2023
    """
    logger.info("📊 Simulando comparativo de anos (F9 - dados mockados)...")
    
    # Pegar total empenhado de 2025
    total_2025 = df_balanco[df_balanco['Fonte'] == 'TOTAL']['Empenhado'].values[0]
    
    # Simular valores para 2024 e 2023 (variação de ±10-20%)
    import numpy as np
    np.random.seed(42)  # Para resultados consistentes
    
    categorias = ['Material de Consumo', 'Material Permanente', 'Serviços PJ', 'Serviços PF']
    
    dados = []
    for categoria in categorias:
        # Distribuir o total entre categorias (proporções simuladas)
        if categoria == 'Material de Consumo':
            prop = 0.40
        elif categoria == 'Material Permanente':
            prop = 0.25
        elif categoria == 'Serviços PJ':
            prop = 0.25
        else:  # Serviços PF
            prop = 0.10
        
        valor_2025 = total_2025 * prop
        valor_2024 = valor_2025 * np.random.uniform(0.85, 0.95)  # 5-15% menor
        valor_2023 = valor_2024 * np.random.uniform(0.90, 1.05)  # ±5%
        
        dados.append({
            'Categoria': categoria,
            'Ano_2025': valor_2025,
            'Ano_2024': valor_2024,
            'Ano_2023': valor_2023
        })
    
    df_comparativo = pd.DataFrame(dados)
    
    logger.info(f"   ✓ Dados comparativos simulados: {len(df_comparativo)} categorias")
    
    return df_comparativo
