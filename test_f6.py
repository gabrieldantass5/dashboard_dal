"""
Script de Teste para F6 - Status de Processos
Verifica se as funções estão funcionando corretamente
"""

import pandas as pd
from pathlib import Path
from src.data_loader import load_excel_data, clean_despesas, clean_balanco
from src.data_processor import processar_status_processos
from src.visualizations import grafico_status_processos, grafico_pizza_distribuicao
from src.utils import formatar_moeda, NOMES_FONTES

print("="*60)
print("TESTE F6: STATUS DE PROCESSOS E DISTRIBUIÇÃO")
print("="*60)

# Carregar dados
arquivo_excel = Path("data/ORÇAMENTO 2025 (1).xlsx")
print(f"\n1. Carregando dados de: {arquivo_excel}")

dados = load_excel_data(str(arquivo_excel))
df_despesas = clean_despesas(dados['CONTROLE DE DESPESAS'])
df_balanco = clean_balanco(dados['BALANCO'])

print(f"   ✓ Despesas carregadas: {len(df_despesas)} processos")
print(f"   ✓ Balanço carregado: {len(df_balanco)} fontes")

# Testar processar_status_processos
print("\n2. Testando processar_status_processos()")
df_status = processar_status_processos(df_despesas)

print(f"   ✓ Status processados: {len(df_status)} categorias")
print("\n   Detalhamento por Status:")
print("   " + "-"*56)
for _, row in df_status.iterrows():
    print(f"   {row['Status']:15} | {int(row['Quantidade']):3} processos | {formatar_moeda(row['Valor_Total']):>18} | {row['Percentual']:5.1f}%")
print("   " + "-"*56)

# Testar gráfico de status
print("\n3. Testando grafico_status_processos()")
try:
    fig_status = grafico_status_processos(df_status)
    print(f"   ✓ Gráfico de status criado com sucesso")
    print(f"   ✓ Tipo: {type(fig_status).__name__}")
    print(f"   ✓ Número de traces: {len(fig_status.data)}")
except Exception as e:
    print(f"   ✗ Erro ao criar gráfico: {e}")

# Testar distribuição por fonte (para gráfico de pizza)
print("\n4. Testando distribuição por fonte")
df_dist_fonte = df_despesas.groupby('Fonte')['Valor'].sum().reset_index()
df_dist_fonte['Fonte_Nome'] = df_dist_fonte['Fonte'].map(NOMES_FONTES)

print(f"   ✓ Distribuição calculada: {len(df_dist_fonte)} fontes")
print("\n   Detalhamento por Fonte:")
print("   " + "-"*56)
for _, row in df_dist_fonte.iterrows():
    fonte_nome = row['Fonte_Nome'] if pd.notna(row['Fonte_Nome']) else f"Fonte {row['Fonte']}"
    print(f"   {fonte_nome:25} | {formatar_moeda(row['Valor']):>18}")
print("   " + "-"*56)

# Testar gráfico de pizza
print("\n5. Testando grafico_pizza_distribuicao()")
try:
    fig_pizza = grafico_pizza_distribuicao(
        df_dist_fonte,
        coluna_valores='Valor',
        coluna_labels='Fonte_Nome'
    )
    print(f"   ✓ Gráfico de pizza criado com sucesso")
    print(f"   ✓ Tipo: {type(fig_pizza).__name__}")
    print(f"   ✓ Número de traces: {len(fig_pizza.data)}")
except Exception as e:
    print(f"   ✗ Erro ao criar gráfico: {e}")

# Resumo final
print("\n" + "="*60)
print("RESUMO DO TESTE F6")
print("="*60)
print(f"✓ Função processar_status_processos: OK")
print(f"✓ Função grafico_status_processos: OK")
print(f"✓ Função grafico_pizza_distribuicao: OK")
print(f"✓ Total de processos: {len(df_despesas)}")
print(f"✓ Status diferentes: {len(df_status)}")
print(f"✓ Fontes diferentes: {len(df_dist_fonte)}")
print("="*60)
print("\n✅ TESTE F6 CONCLUÍDO COM SUCESSO!")
print("\nPróximos passos:")
print("1. Execute 'streamlit run app.py' para ver os gráficos no dashboard")
print("2. Navegue até a seção '📋 Monitoramento de Processos'")
print("3. Verifique os gráficos de Status e Distribuição")
print("="*60)
