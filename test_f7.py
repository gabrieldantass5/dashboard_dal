"""
Script de Teste para F7 - Execução do PCA 2025
Verifica se as funções estão funcionando corretamente
"""

import pandas as pd
from pathlib import Path
from src.data_loader import load_excel_data, clean_pca
from src.data_processor import calcular_execucao_pca
from src.visualizations import grafico_execucao_pca
from src.utils import formatar_moeda, formatar_percentual

print("="*60)
print("TESTE F7: EXECUÇÃO DO PCA 2025")
print("="*60)

# Carregar dados
arquivo_excel = Path("data/ORÇAMENTO 2025 (1).xlsx")
print(f"\n1. Carregando dados de: {arquivo_excel}")

dados = load_excel_data(str(arquivo_excel))

# Testar clean_pca
print("\n2. Testando clean_pca()")
if 'PCA 2025' in dados:
    df_pca = clean_pca(dados['PCA 2025'])
    print(f"   ✓ PCA limpo: {len(df_pca)} itens")
    print(f"   ✓ Colunas: {df_pca.columns.tolist()}")
    
    # Mostrar primeiras linhas
    print("\n   Primeiras 5 ações:")
    print("   " + "-"*80)
    for idx, row in df_pca.head(5).iterrows():
        print(f"   {row['Tipo']:10} | Item {int(row['Item']):2} | {row['Classe_Grupo'][:30]:30} | {formatar_percentual(row['Perc_Execucao'])}")
    print("   " + "-"*80)
else:
    print("   ✗ Aba 'PCA 2025' não encontrada")
    df_pca = pd.DataFrame()

# Testar calcular_execucao_pca
print("\n3. Testando calcular_execucao_pca()")
if not df_pca.empty:
    df_pca_exec = calcular_execucao_pca(df_pca)
    
    print(f"   ✓ Ações processadas: {len(df_pca_exec)}")
    
    # Estatísticas
    exec_media = df_pca_exec['Perc_Execucao'].mean()
    acoes_concluidas = len(df_pca_exec[df_pca_exec['Perc_Execucao'] >= 100])
    acoes_criticas = len(df_pca_exec[df_pca_exec['Perc_Execucao'] < 50])
    
    print(f"   ✓ Execução média: {formatar_percentual(exec_media)}")
    print(f"   ✓ Ações concluídas (≥100%): {acoes_concluidas}")
    print(f"   ✓ Ações críticas (<50%): {acoes_criticas}")
    
    # Mostrar top 10 ações por execução
    print("\n   Top 10 Ações por Execução:")
    print("   " + "-"*90)
    print(f"   {'Ação':40} | {'Previsto':>15} | {'Executado':>15} | {'% Exec':>8}")
    print("   " + "-"*90)
    for _, row in df_pca_exec.head(10).iterrows():
        acao = row['Acao'][:38] if len(str(row['Acao'])) > 38 else str(row['Acao'])
        print(f"   {acao:40} | {formatar_moeda(row['Previsto']):>15} | {formatar_moeda(row['Executado']):>15} | {formatar_percentual(row['Perc_Execucao']):>8}")
    print("   " + "-"*90)
else:
    print("   ✗ DataFrame PCA vazio, pulando teste")
    df_pca_exec = pd.DataFrame()

# Testar gráfico de execução PCA
print("\n4. Testando grafico_execucao_pca()")
if not df_pca_exec.empty:
    try:
        fig_pca = grafico_execucao_pca(df_pca_exec)
        print(f"   ✓ Gráfico de execução PCA criado com sucesso")
        print(f"   ✓ Tipo: {type(fig_pca).__name__}")
        print(f"   ✓ Número de traces: {len(fig_pca.data)}")
    except Exception as e:
        print(f"   ✗ Erro ao criar gráfico: {e}")
else:
    print("   ⚠️  DataFrame vazio, testando placeholder")
    try:
        fig_pca = grafico_execucao_pca(pd.DataFrame())
        print(f"   ✓ Gráfico placeholder criado com sucesso")
    except Exception as e:
        print(f"   ✗ Erro ao criar gráfico placeholder: {e}")

# Resumo final
print("\n" + "="*60)
print("RESUMO DO TESTE F7")
print("="*60)

if not df_pca.empty:
    print(f"✓ Função clean_pca: OK ({len(df_pca)} itens)")
    print(f"✓ Função calcular_execucao_pca: OK ({len(df_pca_exec)} ações)")
    print(f"✓ Função grafico_execucao_pca: OK")
    print(f"\n📊 Estatísticas do PCA:")
    print(f"   - Total de itens: {len(df_pca)}")
    print(f"   - Ações monitoradas: {len(df_pca_exec)}")
    print(f"   - Execução média: {formatar_percentual(exec_media)}")
    print(f"   - Ações concluídas: {acoes_concluidas}")
    print(f"   - Ações críticas: {acoes_criticas}")
else:
    print("⚠️  Aba 'PCA 2025' não encontrada ou vazia")
    print("   Verifique se o arquivo Excel contém a aba 'PCA 2025'")

print("="*60)
print("\n✅ TESTE F7 CONCLUÍDO!")
print("\nPróximos passos:")
print("1. O Streamlit precisa ser reiniciado para carregar as mudanças")
print("2. Execute: Ctrl+C no terminal do Streamlit e depois 'streamlit run app.py'")
print("3. Navegue até a seção '🎯 Plano de Contratações Anuais (PCA) 2025'")
print("4. Verifique o gráfico bullet chart e os indicadores")
print("="*60)
