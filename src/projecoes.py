"""
Módulo de Projeções e Alertas (F10)
Funções para calcular projeções de esgotamento e gerar alertas
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


def calcular_projecoes_esgotamento(
    df_balanco: pd.DataFrame,
    df_despesas: pd.DataFrame,
    dias_no_ano: int = 365
) -> pd.DataFrame:
    """
    Calcula projeção de esgotamento de recursos por fonte.
    
    Args:
        df_balanco: DataFrame com saldos por fonte
        df_despesas: DataFrame com despesas
        dias_no_ano: Número de dias para projeção (padrão: 365)
    
    Returns:
        DataFrame com colunas:
        - Fonte, Saldo_Atual, Taxa_Diaria, Dias_Restantes, 
          Data_Esgotamento, Nivel_Alerta
    
    Metodologia:
        1. Calcula taxa diária de execução: Empenhado / dias decorridos
        2. Projeta dias restantes: Saldo / taxa_diaria
        3. Calcula data estimada de esgotamento
        4. Define nível de alerta baseado em dias restantes
    """
    logger.info("📊 Calculando projeções de esgotamento...")
    
    # Remover linha de total
    df = df_balanco[df_balanco['Fonte'] != 'TOTAL'].copy()
    
    # Assumir que estamos em fevereiro (mês 2), dia 11
    # Dias decorridos no ano: 31 (jan) + 11 (fev) = 42 dias
    dias_decorridos = 42
    dias_restantes_ano = dias_no_ano - dias_decorridos
    
    projecoes = []
    
    for _, row in df.iterrows():
        fonte = row['Fonte']
        saldo = row['Saldo']
        empenhado = row['Empenhado']
        recursos = row['Recursos']
        
        # Calcular taxa diária de execução
        if dias_decorridos > 0:
            taxa_diaria = empenhado / dias_decorridos
        else:
            taxa_diaria = 0
        
        # Calcular dias restantes até esgotamento
        if taxa_diaria > 0 and saldo > 0:
            dias_ate_esgotamento = saldo / taxa_diaria
        elif saldo <= 0:
            dias_ate_esgotamento = 0
        else:
            dias_ate_esgotamento = float('inf')
        
        # Calcular data estimada de esgotamento
        if dias_ate_esgotamento != float('inf') and dias_ate_esgotamento > 0:
            data_esgotamento = datetime.now() + timedelta(days=dias_ate_esgotamento)
        else:
            data_esgotamento = None
        
        # Definir nível de alerta
        if saldo <= 0:
            nivel_alerta = 'CRÍTICO'
        elif dias_ate_esgotamento < 30:
            nivel_alerta = 'CRÍTICO'
        elif dias_ate_esgotamento < 90:
            nivel_alerta = 'ALTO'
        elif dias_ate_esgotamento < 180:
            nivel_alerta = 'MÉDIO'
        else:
            nivel_alerta = 'BAIXO'
        
        # Calcular percentual de saldo restante
        perc_saldo = (saldo / recursos * 100) if recursos > 0 else 0
        
        projecoes.append({
            'Fonte': fonte,
            'Saldo_Atual': saldo,
            'Taxa_Diaria': taxa_diaria,
            'Dias_Restantes': min(dias_ate_esgotamento, 9999),  # Cap para display
            'Data_Esgotamento': data_esgotamento,
            'Nivel_Alerta': nivel_alerta,
            'Perc_Saldo': perc_saldo
        })
    
    df_projecoes = pd.DataFrame(projecoes)
    
    # Ordenar por dias restantes (crescente)
    df_projecoes = df_projecoes.sort_values('Dias_Restantes').reset_index(drop=True)
    
    # Estatísticas
    fontes_criticas = len(df_projecoes[df_projecoes['Nivel_Alerta'] == 'CRÍTICO'])
    fontes_alto_risco = len(df_projecoes[df_projecoes['Nivel_Alerta'] == 'ALTO'])
    
    logger.info(f"   ✓ Projeções calculadas para {len(df_projecoes)} fontes")
    logger.info(f"   ⚠️  Fontes em nível CRÍTICO: {fontes_criticas}")
    logger.info(f"   ⚠️  Fontes em nível ALTO: {fontes_alto_risco}")
    
    return df_projecoes


def gerar_alertas_automaticos(
    df_projecoes: pd.DataFrame,
    df_despesas: pd.DataFrame
) -> List[Dict]:
    """
    Gera lista de alertas automáticos baseados nas projeções.
    
    Args:
        df_projecoes: DataFrame com projeções de esgotamento
        df_despesas: DataFrame com despesas
    
    Returns:
        Lista de dicionários com alertas:
        - tipo: 'CRÍTICO', 'ALTO', 'MÉDIO', 'INFO'
        - titulo: Título do alerta
        - mensagem: Descrição detalhada
        - fonte: Fonte afetada (se aplicável)
        - acao_recomendada: Ação sugerida
    """
    logger.info("🚨 Gerando alertas automáticos...")
    
    alertas = []
    
    # Alerta 1: Fontes com saldo crítico (< 10%)
    fontes_criticas = df_projecoes[df_projecoes['Perc_Saldo'] < 10]
    for _, row in fontes_criticas.iterrows():
        alertas.append({
            'tipo': 'CRÍTICO',
            'titulo': f'Saldo Crítico - Fonte {row["Fonte"]}',
            'mensagem': f'Saldo restante: {row["Perc_Saldo"]:.1f}% (R$ {row["Saldo_Atual"]:,.2f})',
            'fonte': row['Fonte'],
            'acao_recomendada': 'Bloquear novos empenhos e revisar processos reservados'
        })
    
    # Alerta 2: Fontes que esgotarão em menos de 30 dias
    fontes_esgotamento_iminente = df_projecoes[
        (df_projecoes['Dias_Restantes'] < 30) & 
        (df_projecoes['Dias_Restantes'] > 0)
    ]
    for _, row in fontes_esgotamento_iminente.iterrows():
        data_str = row['Data_Esgotamento'].strftime('%d/%m/%Y') if row['Data_Esgotamento'] else 'N/A'
        alertas.append({
            'tipo': 'CRÍTICO',
            'titulo': f'Esgotamento Iminente - Fonte {row["Fonte"]}',
            'mensagem': f'Recursos esgotarão em ~{int(row["Dias_Restantes"])} dias (até {data_str})',
            'fonte': row['Fonte'],
            'acao_recomendada': 'Solicitar suplementação orçamentária urgente'
        })
    
    # Alerta 3: Fontes com alto risco (30-90 dias)
    fontes_alto_risco = df_projecoes[
        (df_projecoes['Dias_Restantes'] >= 30) & 
        (df_projecoes['Dias_Restantes'] < 90)
    ]
    for _, row in fontes_alto_risco.iterrows():
        data_str = row['Data_Esgotamento'].strftime('%d/%m/%Y') if row['Data_Esgotamento'] else 'N/A'
        alertas.append({
            'tipo': 'ALTO',
            'titulo': f'Alto Risco - Fonte {row["Fonte"]}',
            'mensagem': f'Recursos esgotarão em ~{int(row["Dias_Restantes"])} dias (até {data_str})',
            'fonte': row['Fonte'],
            'acao_recomendada': 'Planejar suplementação ou remanejamento'
        })
    
    # Alerta 4: Processos reservados com valor alto
    processos_reservados = df_despesas[df_despesas['Status'] == 'Reservado']
    valor_reservado_total = processos_reservados['Valor'].sum()
    
    if valor_reservado_total > 1000000:  # > 1M
        alertas.append({
            'tipo': 'MÉDIO',
            'titulo': 'Alto Valor em Processos Reservados',
            'mensagem': f'R$ {valor_reservado_total:,.2f} em {len(processos_reservados)} processos reservados',
            'fonte': None,
            'acao_recomendada': 'Revisar e empenhar processos prioritários'
        })
    
    # Alerta 5: Taxa de execução geral
    # (Já calculado em outras funções, mas podemos adicionar alerta específico)
    
    logger.info(f"   ✓ {len(alertas)} alertas gerados")
    
    # Ordenar por tipo (CRÍTICO > ALTO > MÉDIO > INFO)
    ordem_tipo = {'CRÍTICO': 0, 'ALTO': 1, 'MÉDIO': 2, 'INFO': 3}
    alertas.sort(key=lambda x: ordem_tipo.get(x['tipo'], 99))
    
    return alertas
