"""
Dashboard de Controle Orçamentário DAL/CBMAL
Aplicação Principal Streamlit - VERSÃO 3.1 UX OTIMIZADA

Desenvolvido em Python com:
- Streamlit (interface)
- Plotly (visualizações)
- Pandas (processamento de dados)

Versão: 3.1 Premium Dark Edition - UX Otimizada
Data: 11/02/2026
Melhorias: Filtros locais por aba + Aba dedicada para Alertas + Sidebar limpa
"""

import streamlit as st
import pandas as pd
import logging
from pathlib import Path

# Imports locais
from src.data_loader import load_excel_data, clean_despesas, clean_balanco, clean_pca
from src.data_processor import (
    gerar_metricas_kpi,
    calcular_saldos_por_fonte,
    calcular_orcado_vs_executado,
    processar_status_processos,
    calcular_execucao_pca,
    simular_evolucao_temporal,
    simular_comparativo_anos
)
from src.visualizations import (
    grafico_saldo_por_fonte,
    grafico_orcado_vs_executado,
    tabela_interativa_despesas,
    grafico_status_processos,
    grafico_pizza_distribuicao,
    grafico_execucao_pca,
    grafico_projecoes_esgotamento,
    grafico_evolucao_temporal,
    grafico_comparativo_anos
)
from src.utils import (
    formatar_moeda,
    formatar_percentual,
    aplicar_filtros,
    PAGE_CONFIG,
    TEXTOS,
    validar_valores_esperados,
    NOMES_FONTES
)
from src.projecoes import calcular_projecoes_esgotamento, gerar_alertas_automaticos

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar CSS customizado
def load_css():
    """Carrega CSS customizado para melhorar dark mode."""
    css_file = Path(".streamlit/custom.css")
    if css_file.exists():
        with open(css_file, encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================

st.set_page_config(**PAGE_CONFIG)

# =============================================================================
# CABEÇALHO
# =============================================================================

# =============================================================================
# CABEÇALHO (Hero Section)
# =============================================================================

import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

brasao_path = Path("template/Brasão Manual Idenditade 2022 - Sem fundo.png")
if brasao_path.exists():
    img_base64 = get_base64_image(brasao_path)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="header-logo">'
else:
    img_html = '<div style="font-size: 3rem;">🚒</div>'

header_html = f"""
<div class="header-container">
    <div class="logo-container">
        {img_html}
    </div>
    <div class="title-container">
        <div class="main-title">
            <span class="highlight-bar">|</span> 
            {TEXTOS['titulo_principal']}
        </div>
        <div class="subtitle">
            Diretoria de Apoio Logístico - CBMAL <span class="separator">|</span> Orçamento 2025
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR - INFORMAÇÕES E CONTROLES
# =============================================================================

with st.sidebar:
    st.header("📊 Painel de Controle")

    st.markdown("### 📁 Fonte de Dados")

    arquivo_excel = Path("data/ORÇAMENTO 2025 (1).xlsx")

    if arquivo_excel.exists():
        st.success(f"✅ Conectado")
        st.caption(f"📄 {arquivo_excel.name}")
    else:
        st.warning("⚠️ Arquivo não encontrado")
        st.caption("🔍 Modo Demonstração Ativado")
        # st.stop() # Removido para permitir modo demo

    st.markdown("---")
    
    st.markdown("### ℹ️ Sobre o Dashboard")
    st.caption("**Versão:** 3.1 Premium UX")
    st.caption("**Atualizado:** 11/02/2026")
    st.caption("**Dados:** Orçamento 2025")
    
    st.markdown("---")
    
    # Botão para limpar cache
    if st.button("🔄 Limpar Cache", help="Limpa o cache do dashboard para resolver erros de carregamento"):
        st.cache_data.clear()
        st.success("✅ Cache limpo! Recarregando...")
        st.rerun()
    
    st.markdown("---")
    
    st.info("💡 **Dica:** Cada aba possui filtros específicos para análise focada")

# =============================================================================
# CARREGAMENTO DE DADOS
# =============================================================================

@st.cache_data(show_spinner=False)
def carregar_dados(caminho_excel):
    """Carrega e processa todos os dados do Excel."""
    try:
        dados_raw = load_excel_data(caminho_excel)
        
        # Verificar se é mock
        if dados_raw.get('__IS_MOCK__'):
            df_despesas = dados_raw['CONTROLE DE DESPESAS']
            df_balanco = dados_raw['BALANCO']
            df_pca = dados_raw['PCA 2025']
            logger.info("⚠️ Usando dados mockados (sem limpeza necessária)")
        else:
            df_despesas = clean_despesas(dados_raw['CONTROLE DE DESPESAS'])
            df_balanco = clean_balanco(dados_raw['BALANCO'])
            df_pca = clean_pca(dados_raw['PCA 2025']) if 'PCA 2025' in dados_raw else pd.DataFrame()
        
        logger.info(f"✅ Dados carregados: {len(df_despesas)} despesas, {len(df_balanco)} fontes")
        
        return {
            'despesas': df_despesas,
            'balanco': df_balanco,
            'pca': df_pca,
            'sucesso': True,
            'is_mock': dados_raw.get('__IS_MOCK__', False)
        }
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dados: {e}")
        return {
            'despesas': pd.DataFrame(),
            'balanco': pd.DataFrame(),
            'pca': pd.DataFrame(),
            'sucesso': False,
            'erro': str(e),
            'is_mock': False
        }


with st.spinner(TEXTOS['aguarde']):
    dados_carregados = carregar_dados(arquivo_excel)

if not dados_carregados['sucesso']:
    st.error(TEXTOS['erro_carregamento'])
    st.error(f"Detalhes: {dados_carregados.get('erro', 'Erro desconhecido')}")
    st.stop()

# Banner de Modo Demo
if dados_carregados.get('is_mock'):
    st.warning("⚠️ **ATENÇÃO: MODO DE DEMONSTRAÇÃO ATIVO** - Os dados apresentados abaixo são FICTÍCIOS e servem apenas para validação visual e de funcionalidades. Nenhuma informação real está sendo exibida.", icon="⚠️")

df_despesas = dados_carregados['despesas']
df_balanco = dados_carregados['balanco']
df_pca = dados_carregados.get('pca', pd.DataFrame())

validacao = validar_valores_esperados(df_balanco)

# =============================================================================
# NAVEGAÇÃO POR ABAS (7 ABAS)
# =============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Visão Geral",
    "🚨 Alertas",
    "💰 Análise Financeira", 
    "📋 Processos",
    "📑 PCA 2025",
    "📉 Projeções",
    "📈 Análises Avançadas"
])

# =============================================================================
# TAB 1: VISÃO GERAL (SEM FILTROS - SEMPRE MOSTRA TUDO)
# =============================================================================

with tab1:
    st.header("📈 Visão Geral — Indicadores Estratégicos")
    st.caption("Visão consolidada de todo o orçamento 2025")

    # Calcular métricas gerais (sem filtros)
    metricas = gerar_metricas_kpi(df_balanco, df_despesas)
    df_saldos_geral = calcular_saldos_por_fonte(df_balanco)

    # KPI Cards CSS Atualizado
    kpi_card_css = """
<style>
.kpi-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1.2rem;
    margin: 1.5rem 0;
}
.kpi-card {
    flex: 1;
    min-width: 250px;
    background: linear-gradient(135deg, rgba(30,36,50,0.85), rgba(15,18,25,0.98));
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.8rem 1.2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border-left: 6px solid #D32F2F;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    transition: all 0.3s ease;
}
.kpi-card:hover {
    transform: translateY(-5px);
    border-color: rgba(211,47,47,0.4);
}
.kpi-card.primary {
    background: linear-gradient(135deg, rgba(211,47,47,0.12), rgba(30,36,50,0.9));
    border-left: 8px solid #D32F2F;
}
.kpi-label {
    font-family: 'Inter',sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #9BA4B5;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.8rem;
}
.kpi-value {
    font-family: 'Inter',sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #EAEEF3;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.kpi-value.big { font-size: 2.6rem; }
.kpi-sub {
    font-family: 'Inter',sans-serif;
    font-size: 0.9rem;
    color: #8E9AAF;
    margin-top: 0.8rem;
    font-weight: 500;
}
.status-badge {
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    background: rgba(67, 160, 71, 0.2);
    color: #4CAF50;
    border: 1px solid rgba(67, 160, 71, 0.3);
}
.status-badge.alert {
    background: rgba(211, 47, 47, 0.2);
    color: #EF5350;
    border: 1px solid rgba(211, 47, 47, 0.3);
}
</style>
"""
    st.markdown(kpi_card_css, unsafe_allow_html=True)

    # Função auxiliar para quebrar R$ e numeral
    def format_kpi_value(moeda_str):
        partes = moeda_str.split('\xa0') if '\xa0' in moeda_str else moeda_str.split(' ')
        if len(partes) >= 2:
            return f'<span style="font-size: 0.55em; opacity: 0.7;">{partes[0]}</span><br>{partes[1]}'
        return moeda_str

    saldo_fmt = format_kpi_value(formatar_moeda(metricas['saldo_disponivel']))
    recursos_fmt = format_kpi_value(formatar_moeda(metricas['total_recursos']))
    empenhado_fmt = format_kpi_value(formatar_moeda(metricas['total_empenhado']))
    perc_fmt = formatar_percentual(metricas['perc_execucao'])
    
    taxa = metricas['taxa_execucao']
    status_taxa = "Normal" if taxa <= 95 else "Atenção"
    badge_class = "status-badge" if taxa <= 95 else "status-badge alert"

    st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card primary">
        <div class="kpi-label">💵 Saldo Disponível</div>
        <div class="kpi-value big">{saldo_fmt}</div>
        <div class="kpi-sub">Recursos para novos empenhos</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">💰 Recursos Totais</div>
        <div class="kpi-value">{recursos_fmt}</div>
        <div class="kpi-sub">Orçamento aprovado 2025</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">💳 Empenhado</div>
        <div class="kpi-value">{empenhado_fmt}</div>
        <div class="kpi-sub">Valor total executado</div>
    </div>
</div>

<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">📋 Processos Ativos</div>
        <div class="kpi-value">{metricas['total_processos']}</div>
        <div class="kpi-sub">Processos em andamento</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">📊 Taxa de Execução</div>
        <div class="kpi-value">{formatar_percentual(taxa)}</div>
        <div class="kpi-sub">Status: <span class="{badge_class}">{status_taxa}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)


    # Resumo rápido de alertas
    df_projecoes_geral = calcular_projecoes_esgotamento(df_balanco, df_despesas)
    alertas_geral = gerar_alertas_automaticos(df_projecoes_geral, df_despesas)
    
    criticos_count = len([a for a in alertas_geral if a['tipo'] == 'CRÍTICO'])
    altos_count = len([a for a in alertas_geral if a['tipo'] == 'ALTO'])
    
    if criticos_count > 0 or altos_count > 0:
        col_alert1, col_alert2 = st.columns(2)
        with col_alert1:
            if criticos_count > 0:
                st.error(f"🔴 **{criticos_count} Alerta(s) Crítico(s)** — Veja a aba 'Alertas'")
        with col_alert2:
            if altos_count > 0:
                st.warning(f"🟠 **{altos_count} Alerta(s) de Alto Risco** — Veja a aba 'Alertas'")

# =============================================================================
# TAB 2: ALERTAS (NOVA ABA DEDICADA)
# =============================================================================

with tab2:
    st.header("🚨 Central de Alertas Automáticos")
    st.caption("Monitoramento inteligente de riscos orçamentários")
    
    # Recalcular alertas
    df_projecoes_alertas = calcular_projecoes_esgotamento(df_balanco, df_despesas)
    alertas = gerar_alertas_automaticos(df_projecoes_alertas, df_despesas)
    
    if alertas:
        # Separar por tipo
        criticos = [a for a in alertas if a['tipo'] == 'CRÍTICO']
        altos = [a for a in alertas if a['tipo'] == 'ALTO']
        medios = [a for a in alertas if a['tipo'] == 'MÉDIO']
        
        # Dashboard de alertas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Críticos", len(criticos))
        with col2:
            st.metric("🟠 Altos", len(altos))
        with col3:
            st.metric("🟡 Médios", len(medios))
        
        st.divider()
        
        # Alertas críticos
        if criticos:
            st.error("### 🔴 Alertas Críticos — Ação Imediata Necessária")
            for alerta in criticos:
                with st.expander(f"⚠️ {alerta['titulo']}", expanded=True):
                    st.markdown(alerta['mensagem'])
                    st.markdown(f"**🎯 Ação Recomendada:** {alerta['acao_recomendada']}")
                    if alerta.get('fonte'):
                        st.caption(f"📍 Fonte: {NOMES_FONTES.get(alerta['fonte'], alerta['fonte'])}")
        
        # Alertas altos
        if altos:
            st.warning("### 🟠 Alertas de Alto Risco — Atenção Necessária")
            for alerta in altos:
                with st.expander(f"⚠️ {alerta['titulo']}"):
                    st.markdown(alerta['mensagem'])
                    st.markdown(f"**🎯 Ação Recomendada:** {alerta['acao_recomendada']}")
                    if alerta.get('fonte'):
                        st.caption(f"📍 Fonte: {NOMES_FONTES.get(alerta['fonte'], alerta['fonte'])}")
        
        # Alertas médios
        if medios:
            st.info("### 🟡 Alertas de Médio Risco — Monitoramento")
            for alerta in medios:
                with st.expander(f"ℹ️ {alerta['titulo']}"):
                    st.markdown(alerta['mensagem'])
                    st.markdown(f"**🎯 Ação Recomendada:** {alerta['acao_recomendada']}")
                    if alerta.get('fonte'):
                        st.caption(f"📍 Fonte: {NOMES_FONTES.get(alerta['fonte'], alerta['fonte'])}")
    else:
        st.success("✅ **Nenhum alerta ativo no momento!**")
        st.balloons()
        st.info("Todos os indicadores estão dentro dos parâmetros esperados.")

# =============================================================================
# TAB 3: ANÁLISE FINANCEIRA (COM FILTROS LOCAIS)
# =============================================================================

with tab3:
    st.header("💰 Análise Financeira Detalhada")
    
    # FILTROS LOCAIS
    with st.expander("🔍 Filtros de Análise", expanded=False):
        fontes_disponiveis = sorted(df_balanco[df_balanco['Fonte'] != 'TOTAL']['Fonte'].unique().tolist())
        fontes_selecionadas_fin = st.multiselect(
            "Selecione as Fontes de Recursos",
            options=fontes_disponiveis,
            default=fontes_disponiveis,
            key="filtro_fontes_financeiro"
        )
    
    # Aplicar filtros
    df_balanco_fin = df_balanco[
        (df_balanco['Fonte'].isin(fontes_selecionadas_fin)) | (df_balanco['Fonte'] == 'TOTAL')
    ].copy()
    
    df_despesas_fin = df_despesas[df_despesas['Fonte'].isin(fontes_selecionadas_fin)].copy()
    
    df_saldos_fin = calcular_saldos_por_fonte(df_balanco_fin)
    df_comparativo_fin = calcular_orcado_vs_executado(df_despesas_fin, df_balanco_fin, granularidade='Elemento')
    
    # Saldo por Fonte
    st.subheader("Saldo Disponível por Fonte de Recursos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_saldos = grafico_saldo_por_fonte(df_saldos_fin)
        st.plotly_chart(fig_saldos, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Resumo por Fonte")
        for _, row in df_saldos_fin[df_saldos_fin['Fonte'] != 'TOTAL'].iterrows():
            with st.expander(f"{NOMES_FONTES.get(row['Fonte'], str(row['Fonte']))}"):
                st.metric("Recursos", formatar_moeda(row['Recursos']))
                st.metric("Empenhado", formatar_moeda(row['Empenhado']))
                st.metric("Saldo", formatar_moeda(row['Saldo']))
                st.metric("% Execução", formatar_percentual(row['Perc_Execucao']))
    
    st.divider()
    
    # Orçado vs Executado
    st.subheader("Comparativo: Orçado vs Executado")
    
    fig_comparativo = grafico_orcado_vs_executado(df_comparativo_fin, granularidade='Elemento')
    st.plotly_chart(fig_comparativo, use_container_width=True)
    
    with st.expander("📋 Ver detalhes por elemento"):
        st.dataframe(
            df_comparativo_fin.style.format({
                'Orcado': lambda x: formatar_moeda(x),
                'Executado': lambda x: formatar_moeda(x),
                'Perc_Execucao': lambda x: formatar_percentual(x)
            }).hide(axis='index'),
            use_container_width=True
        )

# =============================================================================
# TAB 4: PROCESSOS (COM FILTROS LOCAIS)
# =============================================================================

with tab4:
    st.header("📋 Monitoramento de Processos")
    
    # FILTROS LOCAIS
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        status_disponiveis = df_despesas['Status'].unique().tolist()
        status_selecionados_proc = st.multiselect(
            "Status dos Processos",
            options=status_disponiveis,
            default=[s for s in status_disponiveis if s != 'Cancelado'],
            key="filtro_status_processos"
        )
    
    with col_filtro2:
        fontes_disponiveis_proc = sorted(df_despesas['Fonte'].dropna().unique().tolist())
        fontes_selecionadas_proc = st.multiselect(
            "Fontes de Recursos",
            options=fontes_disponiveis_proc,
            default=fontes_disponiveis_proc,
            key="filtro_fontes_processos"
        )
    
    # Aplicar filtros
    df_despesas_proc = df_despesas[
        (df_despesas['Status'].isin(status_selecionados_proc)) &
        (df_despesas['Fonte'].isin(fontes_selecionadas_proc))
    ].copy()
    
    df_status_proc = processar_status_processos(df_despesas_proc)
    
    # Status de Processos
    st.subheader("Status dos Processos Orçamentários")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig_status = grafico_status_processos(df_status_proc)
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Distribuição")
        fig_pizza = grafico_pizza_distribuicao(df_status_proc, 'Quantidade', 'Status')
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    st.divider()
    
    # Tabela Detalhada
    st.subheader("📄 Base de Dados Completa")
    
    col_busca, col_download = st.columns([3, 1])
    
    with col_busca:
        busca = st.text_input(
            "🔍 Buscar processo ou objeto",
            placeholder="Digite o número do processo ou palavra-chave...",
            key="busca_processos"
        )
    
    with col_download:
        csv = df_despesas_proc.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="⬇️ Baixar CSV",
            data=csv,
            file_name='despesas_filtradas.csv',
            mime='text/csv'
        )
    
    # Aplicar busca
    if busca:
        df_display = df_despesas_proc[
            df_despesas_proc['Processo'].str.contains(busca, case=False, na=False) |
            df_despesas_proc['Objeto'].str.contains(busca, case=False, na=False)
        ].copy()
    else:
        df_display = df_despesas_proc.copy()
    
    df_tabela = tabela_interativa_despesas(df_display)
    
    # Estatísticas
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.metric("Processos exibidos", len(df_tabela))
    with col_stats2:
        st.metric("Valor total", formatar_moeda(df_display['Valor'].sum()))
    with col_stats3:
        st.metric("Processos totais", len(df_despesas))
    
    # Tabela
    st.dataframe(
        df_tabela.style.format({
            'Valor': lambda x: formatar_moeda(x) if pd.notna(x) else 'R$ 0,00'
        }).hide(axis='index'),
        use_container_width=True,
        height=500
    )

# =============================================================================
# TAB 5: PCA 2025
# =============================================================================

with tab5:
    st.header("📑 Plano de Contratações Anual (PCA) 2025")
    
    if not df_pca.empty:
        df_pca_exec = calcular_execucao_pca(df_pca)
        
        fig_pca = grafico_execucao_pca(df_pca_exec)
        st.plotly_chart(fig_pca, use_container_width=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Ações", len(df_pca_exec))
        with col2:
            concluidas = len(df_pca_exec[df_pca_exec['Perc_Execucao'] >= 100])
            st.metric("Ações Concluídas", concluidas)
        with col3:
            em_andamento = len(df_pca_exec[(df_pca_exec['Perc_Execucao'] > 0) & (df_pca_exec['Perc_Execucao'] < 100)])
            st.metric("Em Andamento", em_andamento)
        with col4:
            nao_iniciadas = len(df_pca_exec[df_pca_exec['Perc_Execucao'] == 0])
            st.metric("Não Iniciadas", nao_iniciadas)
        
        with st.expander("📋 Ver detalhes do PCA"):
            st.dataframe(
                df_pca_exec.style.format({
                    'Previsto': lambda x: formatar_moeda(x),
                    'Executado': lambda x: formatar_moeda(x),
                    'Perc_Execucao': lambda x: formatar_percentual(x)
                }).hide(axis='index'),
                use_container_width=True
            )
    else:
        st.info("📋 Dados do PCA 2025 não disponíveis.")

# =============================================================================
# TAB 6: PROJEÇÕES
# =============================================================================

with tab6:
    st.header("📉 Projeções de Esgotamento de Recursos")
    
    # FILTROS LOCAIS
    with st.expander("🔍 Filtros de Projeção", expanded=False):
        fontes_disponiveis_proj = sorted(df_balanco[df_balanco['Fonte'] != 'TOTAL']['Fonte'].unique().tolist())
        fontes_selecionadas_proj = st.multiselect(
            "Selecione as Fontes para Projeção",
            options=fontes_disponiveis_proj,
            default=fontes_disponiveis_proj,
            key="filtro_fontes_projecoes"
        )
    
    # Aplicar filtros
    df_balanco_proj = df_balanco[
        (df_balanco['Fonte'].isin(fontes_selecionadas_proj)) | (df_balanco['Fonte'] == 'TOTAL')
    ].copy()
    
    df_despesas_proj = df_despesas[df_despesas['Fonte'].isin(fontes_selecionadas_proj)].copy()
    
    df_projecoes = calcular_projecoes_esgotamento(df_balanco_proj, df_despesas_proj)
    
    fig_projecoes = grafico_projecoes_esgotamento(df_projecoes)
    st.plotly_chart(fig_projecoes, use_container_width=True)
    
    with st.expander("📊 Ver tabela de projeções"):
        st.dataframe(
            df_projecoes.style.format({
                'Saldo_Atual': lambda x: formatar_moeda(x),
                'Gasto_Medio_Diario': lambda x: formatar_moeda(x)
            }).hide(axis='index'),
            use_container_width=True
        )

# =============================================================================
# TAB 7: ANÁLISES AVANÇADAS
# =============================================================================

with tab7:
    st.header("📈 Análises Avançadas")
    
    # F8 - Evolução Temporal
    st.subheader("📅 Evolução Temporal da Execução Orçamentária")
    df_temporal = simular_evolucao_temporal(df_balanco)
    fig_temporal = grafico_evolucao_temporal(df_temporal)
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    if not df_temporal.empty:
        st.info("ℹ️ **Nota:** Dados simulados. Aguardando dados históricos mensais reais.")
    
    st.divider()
    
    # F9 - Comparativo com Anos Anteriores
    st.subheader("📊 Comparativo com Anos Anteriores")
    df_comparativo_anos = simular_comparativo_anos(df_balanco)
    fig_comparativo_anos = grafico_comparativo_anos(df_comparativo_anos)
    st.plotly_chart(fig_comparativo_anos, use_container_width=True)
    
    if not df_comparativo_anos.empty:
        with st.expander("📋 Ver tabela comparativa"):
            st.dataframe(
                df_comparativo_anos.style.format({
                    col: lambda x: formatar_moeda(x) 
                    for col in df_comparativo_anos.columns if col.startswith('Ano_')
                }).hide(axis='index'),
                use_container_width=True
            )
        st.info("ℹ️ **Nota:** Dados mockados. Aguardando arquivos de 2024 e 2023.")

# =============================================================================
# RODAPÉ
# =============================================================================

st.divider()
st.caption(TEXTOS['rodape'])
st.caption("💡 **Navegação:** Use as abas acima | **Filtros:** Cada aba possui filtros específicos")

# Debug
if st.sidebar.checkbox("🔧 Modo Debug", value=False):
    st.divider()
    st.subheader("🔧 Informações de Debug")

    col_debug1, col_debug2 = st.columns(2)

    with col_debug1:
        st.write("**DataFrames:**")
        st.write(f"- Despesas: {df_despesas.shape}")
        st.write(f"- Balanco: {df_balanco.shape}")

    with col_debug2:
        st.write("**Validação:**")
        st.write(f"- Total Recursos OK: {validacao['total_recursos']}")
        st.write(f"- Total Empenhado OK: {validacao['total_empenhado']}")

    with st.expander("Ver dados brutos - Despesas"):
        st.dataframe(df_despesas.head(20))

    with st.expander("Ver dados brutos - Balanco"):
        st.dataframe(df_balanco)
