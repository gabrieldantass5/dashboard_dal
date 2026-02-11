"""
Módulo de Visualizações
Dashboard de Controle Orçamentário DAL/CBMAL

Responsável por:
- Criar gráficos interativos com Plotly
- Formatar tabelas para exibição
- Aplicar estilos visuais consistentes
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.utils import CORES_PADRAO, CORES_FONTES, NOMES_FONTES, formatar_moeda
import logging

# Configurar logging
logger = logging.getLogger(__name__)


# ── Tema Premium Reutilizável ────────────────────────────────────────
# Aplicado a TODOS os gráficos para manter consistência visual
FONT_FAMILY = "Inter, Segoe UI, Roboto, sans-serif"

def apply_premium_theme(fig: go.Figure, title: str = "", height: int = 480) -> go.Figure:
    """
    Aplica o tema premium unificado a qualquer figura Plotly.
    Garante fontes legíveis, margens adequadas e cores suaves.
    """
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family=FONT_FAMILY, size=18, color="#EAEEF3"),
            x=0.01,
            xanchor="left",
            pad=dict(b=12)
        ),
        font=dict(family=FONT_FAMILY, size=14, color="#C8CDD8"),
        height=height,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(22,28,40,0.35)",
        margin=dict(l=20, r=24, t=56, b=20),
        hoverlabel=dict(
            bgcolor="rgba(30,36,50,0.92)",
            bordercolor="rgba(255,255,255,0.12)",
            font=dict(family=FONT_FAMILY, size=13, color="#EAEEF3"),
        ),
        legend=dict(
            font=dict(size=13, color="#C8CDD8"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="right",
            x=1,
        ),
    )
    fig.update_xaxes(
        title_font=dict(size=13, color="#9BA4B5"),
        tickfont=dict(size=12, color="#9BA4B5"),
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    )
    fig.update_yaxes(
        title_font=dict(size=13, color="#9BA4B5"),
        tickfont=dict(size=13, color="#C8CDD8"),
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    )
    return fig



def grafico_saldo_por_fonte(df_saldos: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras agrupadas com saldos por fonte.

    Args:
        df_saldos: DataFrame com colunas [Fonte, Recursos, Dotado, Empenhado, Saldo]

    Returns:
        Figura Plotly com gráfico de barras agrupadas

    Visualização:
        - Eixo X: Fontes de recursos (500, 501, 753, 759, 622)
        - Eixo Y: Valores em R$
        - 4 barras por fonte: Recursos, Dotado, Empenhado, Saldo
        - Cores diferenciadas
        - Tooltips com valores formatados
    """
    logger.info("📊 Criando gráfico de saldo por fonte...")

    # Remover linha de total para visualização
    df = df_saldos[df_saldos['Fonte'] != 'TOTAL'].copy()

    # Converter fonte para string para melhor exibição
    df['Fonte_Label'] = df['Fonte'].map(NOMES_FONTES)

    # Criar figura
    fig = go.Figure()

    # Adicionar barras para cada métrica (com opacidade suave)
    fig.add_trace(go.Bar(
        name='Recursos',
        x=df['Fonte_Label'],
        y=df['Recursos'],
        marker=dict(color=CORES_PADRAO['azul'], opacity=0.88, line=dict(width=0)),
        text=[formatar_moeda(v) for v in df['Recursos']],
        textposition='none',
        hovertemplate='<b>%{x}</b><br>Recursos: %{text}<extra></extra>',
    ))

    fig.add_trace(go.Bar(
        name='Dotado',
        x=df['Fonte_Label'],
        y=df['Dotado'],
        marker=dict(color=CORES_PADRAO['laranja'], opacity=0.88, line=dict(width=0)),
        text=[formatar_moeda(v) for v in df['Dotado']],
        textposition='none',
        hovertemplate='<b>%{x}</b><br>Dotado: %{text}<extra></extra>',
    ))

    fig.add_trace(go.Bar(
        name='Empenhado',
        x=df['Fonte_Label'],
        y=df['Empenhado'],
        marker=dict(color=CORES_PADRAO['verde'], opacity=0.88, line=dict(width=0)),
        text=[formatar_moeda(v) for v in df['Empenhado']],
        textposition='none',
        hovertemplate='<b>%{x}</b><br>Empenhado: %{text}<extra></extra>',
    ))

    fig.add_trace(go.Bar(
        name='Saldo',
        x=df['Fonte_Label'],
        y=df['Saldo'],
        marker=dict(color=CORES_PADRAO['roxo'], opacity=0.88, line=dict(width=0)),
        text=[formatar_moeda(v) for v in df['Saldo']],
        textposition='none',
        hovertemplate='<b>%{x}</b><br>Saldo: %{text}<extra></extra>',
    ))

    # Aplicar tema premium
    apply_premium_theme(fig, title='Saldo Disponível por Fonte de Recursos', height=500)
    fig.update_layout(barmode='group', hovermode='x unified')
    fig.update_yaxes(separatethousands=True, tickformat=',')

    logger.info("   ✓ Gráfico de saldo por fonte criado")

    return fig


def grafico_orcado_vs_executado(df_comparativo: pd.DataFrame, granularidade: str = 'Elemento') -> go.Figure:
    """
    Cria gráfico de barras horizontais comparando orçado vs executado.

    Args:
        df_comparativo: DataFrame com colunas [Categoria, Orcado, Executado, Perc_Execucao]
        granularidade: Nome da granularidade para título ("Elemento", "Fonte", etc.)

    Returns:
        Figura Plotly com barras horizontais comparativas

    Visualização:
        - Eixo Y: Categorias (elementos, fontes ou ações)
        - Eixo X: Valores em R$
        - 2 barras lado a lado: Orçado (azul) | Executado (verde)
        - Destaque para sobre-execução (> 100%)
    """
    logger.info(f"📊 Criando gráfico orçado vs executado ({granularidade})...")

    df = df_comparativo.copy()

    # Limitar a top 10 para melhor visualização
    if len(df) > 10:
        df = df.head(10)
        logger.info(f"   Limitando visualização a top 10 de {len(df_comparativo)} categorias")

    # Criar figura
    fig = go.Figure()

    # Barra de Orçado
    fig.add_trace(go.Bar(
        name='Orçado',
        y=df['Categoria'],
        x=df['Orcado'],
        orientation='h',
        marker_color=CORES_PADRAO['azul'],
        text=[formatar_moeda(v) for v in df['Orcado']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Orçado: %{text}<extra></extra>',
        customdata=[[formatar_moeda(v)] for v in df['Orcado']]
    ))

    # Barra de Executado
    # Cor condicional: verde se < 95%, amarelo se 95-100%, vermelho se > 100%
    cores_executado = []
    for perc in df['Perc_Execucao']:
        if perc > 100:
            cores_executado.append(CORES_PADRAO['vermelho'])
        elif perc > 95:
            cores_executado.append(CORES_PADRAO['amarelo'])
        else:
            cores_executado.append(CORES_PADRAO['verde'])

    fig.add_trace(go.Bar(
        name='Executado',
        y=df['Categoria'],
        x=df['Executado'],
        orientation='h',
        marker_color=cores_executado,
        text=[formatar_moeda(v) for v in df['Executado']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Executado: %{text}<extra></extra>',
        customdata=[[formatar_moeda(v)] for v in df['Executado']]
    ))

    # Aplicar tema premium com altura dinâmica
    apply_premium_theme(
        fig,
        title=f'Comparativo: Orçado vs Executado por {granularidade}',
        height=max(460, len(df) * 65)
    )
    fig.update_layout(barmode='group')
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(separatethousands=True, tickformat=',')

    logger.info("   ✓ Gráfico orçado vs executado criado")

    return fig


def grafico_pizza_distribuicao(df: pd.DataFrame, coluna_valores: str, coluna_labels: str) -> go.Figure:
    """
    Cria gráfico de pizza para distribuição.

    Args:
        df: DataFrame com dados
        coluna_valores: Nome da coluna com valores numéricos
        coluna_labels: Nome da coluna com labels (categorias)

    Returns:
        Figura Plotly com gráfico de pizza

    Nota: Implementação para Post-MVP (v2.0)
    """
    logger.info("📊 Criando gráfico de pizza (Post-MVP)...")

    # Implementação básica
    df_clean = df[[coluna_labels, coluna_valores]].copy()
    df_clean = df_clean.dropna()

    fig = px.pie(
        df_clean,
        values=coluna_valores,
        names=coluna_labels,
        template='plotly_dark',
        height=420
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(family=FONT_FAMILY, size=13, color='#EAEEF3'),
        marker=dict(line=dict(color='rgba(14,17,23,0.6)', width=2)),
    )

    # Aplicar tema premium (sem eixos)
    fig.update_layout(
        title=dict(
            text='Distribuição de Recursos',
            font=dict(family=FONT_FAMILY, size=18, color='#EAEEF3'),
            x=0.01, xanchor='left'
        ),
        font=dict(family=FONT_FAMILY, size=14, color='#C8CDD8'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=56, b=20),
        hoverlabel=dict(
            bgcolor='rgba(30,36,50,0.92)',
            font=dict(family=FONT_FAMILY, size=13, color='#EAEEF3'),
        ),
    )

    logger.info("   ✓ Gráfico de pizza criado")

    return fig


def grafico_status_processos(df_status: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras horizontais com status dos processos.

    Args:
        df_status: DataFrame com colunas [Status, Quantidade, Valor_Total, Percentual]

    Returns:
        Figura Plotly com barras horizontais

    Visualização:
        - Eixo Y: Status dos processos
        - Eixo X: Quantidade de processos
        - Cores por status (verde, amarelo, azul, cinza)
        - Tooltips com quantidade e percentual
    """
    logger.info("📊 Criando gráfico de status de processos...")

    if df_status.empty:
        logger.warning("   ⚠️  DataFrame de status vazio")
        return go.Figure()

    # Mapear cores por status
    cores_status = []
    for status in df_status['Status']:
        cores_status.append(CORES_PADRAO.get(status.lower(), CORES_PADRAO.get('verde', '#4B5320')))

    # Criar figura
    fig = go.Figure()

    # Adicionar barras
    fig.add_trace(go.Bar(
        y=df_status['Status'],
        x=df_status['Quantidade'],
        orientation='h',
        marker_color=cores_status,
        text=[f"{int(q)} ({p:.1f}%)" for q, p in zip(df_status['Quantidade'], df_status['Percentual'])],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Quantidade: %{x}<br>Valor Total: R$ %{customdata:,.2f}<extra></extra>',
        customdata=df_status['Valor_Total']
    ))

    # Aplicar tema premium
    apply_premium_theme(fig, title='Status de Processos por Quantidade', height=420)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(autorange="reversed")

    logger.info("   ✓ Gráfico de status de processos criado")

    return fig


def tabela_interativa_despesas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formata DataFrame para exibição como tabela interativa.

    Args:
        df: DataFrame de despesas

    Returns:
        DataFrame formatado (mesmo objeto, para uso com st.dataframe())

    Formatação:
        - Valores numéricos em moeda brasileira
        - Percentuais com 1 casa decimal
        - Ordenação mantida
    """
    logger.info("📊 Formatando tabela de despesas...")

    # Criar cópia para não modificar original
    df_display = df.copy()

    # Selecionar colunas para exibição (MVP)
    colunas_exibir = ['Processo', 'Objeto', 'Valor', 'Fonte', 'Elemento', 'Status']

    # Filtrar apenas colunas existentes
    colunas_exibir = [col for col in colunas_exibir if col in df_display.columns]

    df_display = df_display[colunas_exibir]

    # Renomear colunas para português (se necessário)
    # df_display = df_display.rename(columns={'Valor': 'Valor (R$)'})

    logger.info(f"   ✓ Tabela formatada: {len(df_display)} linhas, {len(colunas_exibir)} colunas")

    return df_display


def aplicar_estilo_tabela(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """
    Aplica formatação condicional à tabela.

    Args:
        df: DataFrame de despesas

    Returns:
        Styler object para uso com st.dataframe()

    Formatação Condicional:
        - Valores: R$ com 2 casas decimais
        - Status "Cancelado": cinza
        - Valores > 1M: negrito (Post-MVP)

    Nota: Implementação completa para Post-MVP (v2.0)
    """
    logger.info("📊 Aplicando estilo à tabela (Post-MVP)...")

    # Implementação básica para MVP
    styler = df.style.format({
        'Valor': lambda x: formatar_moeda(x) if pd.notna(x) else 'R$ 0,00'
    })

    logger.warning("   ⚠️  Formatação condicional completa disponível na v2.0")

    return styler


def grafico_execucao_pca(df_pca: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico bullet chart para execução do PCA 2025.

    Args:
        df_pca: DataFrame com colunas [Acao, Previsto, Executado, Perc_Execucao]

    Returns:
        Figura Plotly com bullet chart ou barras horizontais

    Visualização:
        - Eixo Y: Ações do PCA
        - Eixo X: Percentual de execução (0-100%)
        - Barras coloridas por faixa de execução
        - Meta em 100%
    """
    logger.info("📊 Criando gráfico de execução PCA...")

    if df_pca.empty:
        logger.warning("   ⚠️  DataFrame PCA vazio - retornando gráfico placeholder")
        # Criar gráfico placeholder
        fig = go.Figure()
        fig.add_annotation(
            text="📋 Dados do PCA 2025 em desenvolvimento<br><br>Funcionalidade disponível em breve",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#FAFAFA'),
            align='center'
        )
        fig.update_layout(
            title='Execução do PCA 2025',
            height=400,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(28,28,28,0.3)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

    # Criar cores condicionais baseadas na % de execução
    cores = []
    for perc in df_pca['Perc_Execucao']:
        if perc >= 100:
            cores.append(CORES_PADRAO['verde'])  # Verde: meta atingida
        elif perc >= 75:
            cores.append(CORES_PADRAO['azul'])   # Azul: em andamento
        elif perc >= 50:
            cores.append(CORES_PADRAO['amarelo']) # Amarelo: atenção
        else:
            cores.append(CORES_PADRAO['vermelho']) # Vermelho: crítico

    # Criar figura
    fig = go.Figure()

    # Adicionar barras de execução
    fig.add_trace(go.Bar(
        y=df_pca['Acao'],
        x=df_pca['Perc_Execucao'],
        orientation='h',
        marker_color=cores,
        text=[f"{p:.1f}%" for p in df_pca['Perc_Execucao']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Executado: %{x:.1f}%<br>Previsto: R$ %{customdata[0]:,.2f}<br>Realizado: R$ %{customdata[1]:,.2f}<extra></extra>',
        customdata=list(zip(df_pca['Previsto'], df_pca['Executado']))
    ))

    # Adicionar linha de meta (100%)
    fig.add_vline(
        x=100,
        line_dash="dash",
        line_color="#4C7695",
        annotation_text="Meta 100%",
        annotation_position="top"
    )

    # Aplicar tema premium com altura dinâmica
    apply_premium_theme(
        fig,
        title='Execução do PCA 2025 por Ação',
        height=max(460, len(df_pca) * 52)
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(range=[0, 120])
    fig.update_yaxes(autorange="reversed")

    logger.info("   ✓ Gráfico de execução PCA criado")

    return fig


def grafico_projecoes_esgotamento(df_projecoes: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de projeções de esgotamento por fonte.
    
    Args:
        df_projecoes: DataFrame com projeções (da função calcular_projecoes_esgotamento)
    
    Returns:
        Figura Plotly com gráfico de barras horizontais
    
    Visualização:
        - Eixo Y: Fontes de recursos
        - Eixo X: Dias restantes até esgotamento
        - Cores por nível de alerta
    """
    logger.info("📊 Criando gráfico de projeções de esgotamento...")
    
    if df_projecoes.empty:
        logger.warning("   ⚠️  DataFrame de projeções vazio")
        return go.Figure()
    
    # Mapear cores por nível de alerta
    cores_alerta = {
        'CRÍTICO': CORES_PADRAO['vermelho'],
        'ALTO': CORES_PADRAO['amarelo'],
        'MÉDIO': CORES_PADRAO['laranja'],
        'BAIXO': CORES_PADRAO['verde']
    }
    
    cores = [cores_alerta.get(nivel, CORES_PADRAO['cinza']) for nivel in df_projecoes['Nivel_Alerta']]
    
    # Mapear nomes de fontes
    from src.utils import NOMES_FONTES
    df_projecoes['Fonte_Nome'] = df_projecoes['Fonte'].map(NOMES_FONTES)
    
    # Criar figura
    fig = go.Figure()
    
    # Adicionar barras
    fig.add_trace(go.Bar(
        y=df_projecoes['Fonte_Nome'],
        x=df_projecoes['Dias_Restantes'],
        orientation='h',
        marker_color=cores,
        text=[f"{int(d)} dias" if d < 9999 else "Sem risco" for d in df_projecoes['Dias_Restantes']],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Dias restantes: %{x:.0f}<br>Saldo: R$ %{customdata[0]:,.2f}<br>Nível: %{customdata[1]}<extra></extra>',
        customdata=list(zip(df_projecoes['Saldo_Atual'], df_projecoes['Nivel_Alerta']))
    ))
    
    # Linhas de referência mais suaves
    fig.add_vline(x=30, line_dash="dot", line_color="rgba(239,83,80,0.6)",
                  annotation_text="30 dias", annotation_position="top",
                  annotation_font=dict(size=12, color='#EF5350'))
    fig.add_vline(x=90, line_dash="dot", line_color="rgba(255,179,0,0.6)",
                  annotation_text="90 dias", annotation_position="top",
                  annotation_font=dict(size=12, color='#FFB300'))
    
    # Aplicar tema premium
    apply_premium_theme(fig, title='Projeção de Esgotamento de Recursos por Fonte', height=440)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(autorange="reversed")
    
    logger.info("   ✓ Gráfico de projeções criado")
    
    return fig


def grafico_evolucao_temporal(df_temporal: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de linha com evolução temporal da execução.
    
    Args:
        df_temporal: DataFrame com colunas [Mes, Empenhado_Acumulado, Meta]
    
    Returns:
        Figura Plotly com gráfico de linha
    
    Nota: F8 - Implementação com dados simulados
    """
    logger.info("📊 Criando gráfico de evolução temporal (F8)...")
    
    if df_temporal.empty:
        # Criar placeholder
        fig = go.Figure()
        fig.add_annotation(
            text="📅 Evolução Temporal<br><br>Funcionalidade disponível quando houver<br>dados históricos mensais",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#FAFAFA'),
            align='center'
        )
        fig.update_layout(
            title='Evolução Temporal da Execução Orçamentária',
            height=400,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(28,28,28,0.3)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    # Criar figura com dados reais
    fig = go.Figure()
    
    # Linha de execução real
    fig.add_trace(go.Scatter(
        x=df_temporal['Mes'],
        y=df_temporal['Empenhado_Acumulado'],
        mode='lines+markers',
        name='Executado',
        line=dict(color=CORES_PADRAO['verde'], width=3),
        marker=dict(size=8)
    ))
    
    # Linha de meta
    if 'Meta' in df_temporal.columns:
        fig.add_trace(go.Scatter(
            x=df_temporal['Mes'],
            y=df_temporal['Meta'],
            mode='lines',
            name='Meta',
            line=dict(color=CORES_PADRAO['azul'], width=2, dash='dash')
        ))
    
    # Aplicar tema premium
    apply_premium_theme(fig, title='Evolução Mensal da Execução Orçamentária', height=440)
    fig.update_layout(hovermode='x unified')
    fig.update_yaxes(separatethousands=True, tickformat=',')
    
    logger.info("   ✓ Gráfico de evolução temporal criado")
    
    return fig


def grafico_comparativo_anos(df_comparativo: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico comparativo entre anos.
    
    Args:
        df_comparativo: DataFrame com colunas [Categoria, Ano_2025, Ano_2024, Ano_2023]
    
    Returns:
        Figura Plotly com gráfico de barras agrupadas
    
    Nota: F9 - Implementação com dados mockados
    """
    logger.info("📊 Criando gráfico comparativo de anos (F9)...")
    
    if df_comparativo.empty:
        # Criar placeholder
        fig = go.Figure()
        fig.add_annotation(
            text="📊 Comparativo com Anos Anteriores<br><br>Funcionalidade disponível quando houver<br>dados de orçamentos de 2024 e 2023",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#FAFAFA'),
            align='center'
        )
        fig.update_layout(
            title='Comparativo: Execução 2025 vs Anos Anteriores',
            height=400,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(28,28,28,0.3)',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    # Criar figura com dados
    fig = go.Figure()
    
    # Barras para cada ano
    anos = [col for col in df_comparativo.columns if col.startswith('Ano_')]
    cores_anos = [CORES_PADRAO['verde'], CORES_PADRAO['azul'], CORES_PADRAO['laranja']]
    
    for idx, ano in enumerate(anos):
        ano_label = ano.replace('Ano_', '')
        fig.add_trace(go.Bar(
            name=ano_label,
            x=df_comparativo['Categoria'],
            y=df_comparativo[ano],
            marker_color=cores_anos[idx % len(cores_anos)]
        ))
    
    # Aplicar tema premium
    apply_premium_theme(fig, title='Comparativo: Execução Orçamentária por Ano', height=460)
    fig.update_layout(barmode='group')
    fig.update_yaxes(separatethousands=True, tickformat=',')
    
    logger.info("   ✓ Gráfico comparativo de anos criado")
    
    return fig
