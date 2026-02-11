"""
Módulo de Carregamento de Dados
Dashboard de Controle Orçamentário DAL/CBMAL

Responsável por:
- Carregar arquivo Excel de orçamento
- Limpar e estruturar dados das abas principais
- Aplicar transformações e validações
"""

import pandas as pd
import streamlit as st
import logging
from typing import Dict

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        logger.info(f"📂 Carregando Excel: {filepath}")

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
                logger.info(f"✓ Aba '{aba}' carregada: {df.shape}")
            except Exception as e:
                logger.warning(f"⚠️  Erro ao carregar aba '{aba}': {e}")

        # Validar que abas críticas foram carregadas
        for aba in abas_mvp:
            if aba not in dados or dados[aba].empty:
                raise ValueError(f"Aba crítica '{aba}' não encontrada ou vazia")

        logger.info(f"✅ Excel carregado com sucesso: {len(dados)} abas")
        return dados

    except FileNotFoundError:
        logger.error(f"❌ Arquivo não encontrado: {filepath}")
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar Excel: {e}")
        raise ValueError(f"Erro ao carregar Excel: {e}")


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
    logger.info("🧹 Limpando aba CONTROLE DE DESPESAS...")

    # Fazer cópia para não modificar original
    df = df_raw.copy()

    # Remover linha 0 (geralmente vazia/header de mesclagem)
    df = df.iloc[1:].reset_index(drop=True)

    # Renomear colunas manualmente
    # Baseado na análise: linha 1 tem os nomes verdadeiros
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

    logger.info(f"   Linhas após remover vazias: {len(df)}")

    # Converter tipos de dados
    df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce').fillna(0)
    df['Fonte'] = pd.to_numeric(df['Fonte'], errors='coerce')

    # Converter para Int64 (permite NaN em inteiros)
    df['Fonte'] = df['Fonte'].astype('Int64')

    # Converter booleanos para Nota_Reserva
    df['Nota_Reserva'] = df['Nota_Reserva'].fillna(False)
    df['Nota_Reserva'] = df['Nota_Reserva'].replace({
        'SIM': True, 'NÃO': False, 'NAO': False, 'Sim': True, 'Não': False,
        True: True, False: False, 1: True, 0: False, '1': True, '0': False
    }).astype(bool)

    # Converter booleanos para Nota_Empenho
    df['Nota_Empenho'] = df['Nota_Empenho'].fillna(False)
    df['Nota_Empenho'] = df['Nota_Empenho'].replace({
        'SIM': True, 'NÃO': False, 'NAO': False, 'Sim': True, 'Não': False,
        True: True, False: False, 1: True, 0: False, '1': True, '0': False
    }).astype(bool)

    # Criar coluna Status
    def determinar_status(row):
        """Determina status do processo baseado em flags e valores."""
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
    df['Elemento'] = df['Elemento'].astype(str).str.upper().str.strip()

    # Padronizar elementos
    elemento_map = {
        'CONSUMO': 'CONSUMO',
        'MATERIAL DE CONSUMO': 'CONSUMO',
        'MAT. CONSUMO': 'CONSUMO',
        'PERMANENTE': 'PERMANENTE',
        'MATERIAL PERMANENTE': 'PERMANENTE',
        'MAT. PERMANENTE': 'PERMANENTE',
        'SERVIÇO PJ': 'SERVIÇO PJ',
        'SERVICO PJ': 'SERVIÇO PJ',
        'SERV. PJ': 'SERVIÇO PJ',
        'SERVIÇO PF': 'SERVIÇO PF',
        'SERVICO PF': 'SERVIÇO PF',
        'SERV. PF': 'SERVIÇO PF'
    }
    df['Elemento'] = df['Elemento'].replace(elemento_map)

    # Remover colunas auxiliares (manter apenas Status)
    df = df.drop(columns=['Nota_Reserva', 'Nota_Empenho'])

    # Ordenar por Processo
    df = df.sort_values('Processo').reset_index(drop=True)

    # Log de estatísticas
    logger.info(f"   ✓ Processos limpos: {len(df)}")
    logger.info(f"   ✓ Processos por status:")
    for status, count in df['Status'].value_counts().items():
        logger.info(f"      - {status}: {count}")
    logger.info(f"   ✓ Total de recursos: R$ {df['Valor'].sum():,.2f}")

    return df


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
    logger.info("🧹 Limpando aba BALANCO...")

    df = df_raw.copy()

    # Encontrar linhas-chave (busca flexível)
    idx_recursos = None
    idx_dotado = None
    idx_empenhado = None

    # Buscar em todo o DataFrame
    for idx, row in df.iterrows():
        row_str = ' '.join([str(val).upper() for val in row if pd.notna(val)])

        if 'RECURSOS' in row_str and idx_recursos is None:
            idx_recursos = idx
            logger.info(f"   Linha RECURSOS encontrada: índice {idx}")

        if 'DOTADO' in row_str and idx_dotado is None:
            idx_dotado = idx
            logger.info(f"   Linha DOTADO encontrada: índice {idx}")

        if 'EMPENHADO' in row_str and idx_empenhado is None:
            idx_empenhado = idx
            logger.info(f"   Linha EMPENHADO encontrada: índice {idx}")

    if any(x is None for x in [idx_recursos, idx_dotado, idx_empenhado]):
        logger.error("   ❌ Não foi possível localizar linhas de RECURSOS, DOTADO ou EMPENHADO")
        raise ValueError("Não foi possível localizar linhas de RECURSOS, DOTADO ou EMPENHADO na aba BALANCO")

    # Identificar colunas das fontes
    # Procurar linha com fontes (linha que contém "500", "753", etc.)
    idx_header = None
    col_map = {}

    for idx, row in df.iterrows():
        row_values = [str(val) for val in row]
        if '500' in row_values and '753' in row_values:
            idx_header = idx
            logger.info(f"   Linha de cabeçalhos de fontes encontrada: índice {idx}")

            # Criar mapeamento dinâmico
            for col_idx, val in enumerate(row):
                val_str = str(val).strip()
                if val_str in ['500', '501', '753', '759', '622']:
                    col_map[int(val_str)] = col_idx
                    logger.info(f"      Fonte {val_str} → coluna {col_idx}")
            break

    # Se não encontrou header, tentar mapeamento manual baseado em padrões comuns
    if not col_map:
        logger.warning("   ⚠️  Header de fontes não encontrado, tentando mapeamento manual...")
        # Tentar encontrar valores nas linhas de dados
        # Procurar na linha RECURSOS por valores que parecem ser das fontes
        recursos_row = df.iloc[idx_recursos]

        # Tentar mapear por posição (mais robusto)
        # Geralmente: col 2=500, 3=753, 4=759, 5=622, 6=501
        col_map = {500: 2, 753: 3, 759: 4, 622: 5, 501: 6}
        logger.info("   Usando mapeamento manual padrão")

    # Extrair valores
    fontes = [500, 753, 759, 622, 501]
    dados_balanco = []

    for fonte in fontes:
        if fonte in col_map:
            col_idx = col_map[fonte]

            # Extrair valores com conversão robusta
            recursos = pd.to_numeric(df.iloc[idx_recursos, col_idx], errors='coerce')
            dotado = pd.to_numeric(df.iloc[idx_dotado, col_idx], errors='coerce')
            empenhado = pd.to_numeric(df.iloc[idx_empenhado, col_idx], errors='coerce')

            dados_balanco.append({
                'Fonte': fonte,
                'Recursos': recursos if pd.notna(recursos) else 0,
                'Dotado': dotado if pd.notna(dotado) else 0,
                'Empenhado': empenhado if pd.notna(empenhado) else 0
            })

            logger.info(f"   Fonte {fonte}: R$ {recursos:,.2f} recursos | R$ {empenhado:,.2f} empenhado")
        else:
            logger.warning(f"   ⚠️  Fonte {fonte} não encontrada no mapeamento")

    if not dados_balanco:
        raise ValueError("Nenhum dado de fonte foi extraído da aba BALANCO")

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

    # Log de estatísticas
    logger.info(f"   ✓ Total de Recursos: R$ {total['Recursos']:,.2f}")
    logger.info(f"   ✓ Total Empenhado: R$ {total['Empenhado']:,.2f}")
    logger.info(f"   ✓ Saldo Disponível: R$ {total['Saldo']:,.2f}")
    logger.info(f"   ✓ % Execução Geral: {total['Perc_Execucao']:.2f}%")

    return df_balanco


def clean_pca(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e estrutura dados da aba PCA 2025.

    Args:
        df_raw: DataFrame bruto da aba PCA 2025

    Returns:
        DataFrame limpo com colunas:
        - Tipo, Item, Classe_Grupo, Valor_Estimado, Dotado, Empenhado, 
          Saldo_Dotacao, Perc_Execucao

    Processamento:
        1. Remove linhas vazias e cabeçalhos
        2. Renomeia colunas
        3. Converte tipos de dados
        4. Calcula percentual de execução se necessário
    """
    logger.info("🧹 Limpando aba PCA 2025...")

    # Fazer cópia
    df = df_raw.copy()

    # Linha 2 (índice 2) tem os cabeçalhos
    # Remover linhas 0, 1 (vazias/mescladas)
    df = df.iloc[2:].reset_index(drop=True)

    # Usar primeira linha como header
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    # Renomear colunas para nomes limpos
    df.columns = [
        'Tipo',
        'Item',
        'Classe_Grupo',
        'Valor_Estimado',
        'Dotado',
        'Empenhado',
        'Saldo_Dotacao',
        'Perc_Execucao'
    ]

    # Remover linhas completamente vazias
    df = df.dropna(how='all').copy()

    # Remover linhas onde Tipo é vazio
    df = df[df['Tipo'].notna()].copy()

    # Converter tipos numéricos
    colunas_numericas = ['Item', 'Valor_Estimado', 'Dotado', 'Empenhado', 
                         'Saldo_Dotacao', 'Perc_Execucao']
    
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Calcular percentual de execução se não estiver preenchido ou for 0
    # Perc_Execucao = (Empenhado / Valor_Estimado) * 100
    mask_recalcular = (df['Perc_Execucao'] == 0) | (df['Perc_Execucao'].isna())
    df.loc[mask_recalcular, 'Perc_Execucao'] = (
        (df.loc[mask_recalcular, 'Empenhado'] / df.loc[mask_recalcular, 'Valor_Estimado']) * 100
    ).fillna(0)

    # Limpar strings
    df['Tipo'] = df['Tipo'].astype(str).str.strip()
    df['Classe_Grupo'] = df['Classe_Grupo'].astype(str).str.strip()

    # Ordenar por Item
    df = df.sort_values('Item').reset_index(drop=True)

    logger.info(f"   ✓ PCA limpo: {len(df)} itens")
    logger.info(f"   ✓ Tipos: {df['Tipo'].unique().tolist()}")
    
    # Estatísticas
    exec_media = df['Perc_Execucao'].mean()
    itens_concluidos = len(df[df['Perc_Execucao'] >= 100])
    logger.info(f"   ✓ Execução média: {exec_media:.1f}%")
    logger.info(f"   ✓ Itens concluídos (≥100%): {itens_concluidos}")

    return df


def clean_despesas_recorrentes(df_raw: pd.DataFrame) -> pd.DataFrame:

    """
    Limpa e estrutura dados da aba Despesas 2025.

    Args:
        df_raw: DataFrame bruto da aba Despesas 2025

    Returns:
        DataFrame limpo com despesas recorrentes

    Nota: Implementação para Post-MVP (v2.0)
    """
    logger.info("🧹 Limpando aba Despesas 2025 (Post-MVP)...")

    # Placeholder - implementar na v2.0
    logger.warning("   ⚠️  Função clean_despesas_recorrentes() ainda não implementada (Post-MVP)")

    return pd.DataFrame()
