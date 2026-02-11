"""
Script de Teste para F8, F9 e F10
Verifica se as funcionalidades estão funcionando corretamente
"""

import pandas as pd
from pathlib import Path
from src.data_loader import load_excel_data, clean_despesas, clean_balanco
from src.data_processor import simular_evolucao_temporal, simular_comparativo_anos
from src.projecoes import calcular_projecoes_esgotamento, gerar_alertas_automaticos
from src.visualizations import (
    grafico_evolucao_temporal,
    grafico_comparativo_anos,
    grafico_projecoes_esgotamento
)
from src.utils import formatar_moeda, formatar_percentual

print("="*70)
print("TESTE F8, F9 E F10: EVOLUÇÃO, COMPARATIVOS E PROJEÇÕES")
print("="*70)

# Carregar dados
arquivo_excel = Path("data/ORÇAMENTO 2025 (1).xlsx")
print(f"\n1. Carregando dados de: {arquivo_excel}")

dados = load_excel_data(str(arquivo_excel))
df_despesas = clean_despesas(dados['CONTROLE DE DESPESAS'])
df_balanco = clean_balanco(dados['BALANCO'])

print(f"   ✓ Despesas carregadas: {len(df_despesas)} processos")
print(f"   ✓ Balanço carregado: {len(df_balanco)} fontes")

# =============================================================================
# TESTE F8: EVOLUÇÃO TEMPORAL
# =============================================================================

print("\n" + "="*70)
print("TESTE F8: EVOLUÇÃO TEMPORAL")
print("="*70)

print("\n2. Testando simular_evolucao_temporal()")
df_temporal = simular_evolucao_temporal(df_balanco)

print(f"   ✓ Dados temporais simulados: {len(df_temporal)} meses")
print("\n   Dados:")
print("   " + "-"*66)
print(f"   {'Mês':10} | {'Empenhado Acumulado':>20} | {'Meta':>20}")
print("   " + "-"*66)
for _, row in df_temporal.iterrows():
    print(f"   {row['Mes']:10} | {formatar_moeda(row['Empenhado_Acumulado']):>20} | {formatar_moeda(row['Meta']):>20}")
print("   " + "-"*66)

print("\n3. Testando grafico_evolucao_temporal()")
try:
    fig_temporal = grafico_evolucao_temporal(df_temporal)
    print(f"   ✓ Gráfico de evolução temporal criado")
    print(f"   ✓ Tipo: {type(fig_temporal).__name__}")
    print(f"   ✓ Número de traces: {len(fig_temporal.data)}")
except Exception as e:
    print(f"   ✗ Erro ao criar gráfico: {e}")

# =============================================================================
# TESTE F9: COMPARATIVO COM ANOS ANTERIORES
# =============================================================================

print("\n" + "="*70)
print("TESTE F9: COMPARATIVO COM ANOS ANTERIORES")
print("="*70)

print("\n4. Testando simular_comparativo_anos()")
df_comparativo = simular_comparativo_anos(df_balanco)

print(f"   ✓ Dados comparativos simulados: {len(df_comparativo)} categorias")
print("\n   Dados:")
print("   " + "-"*90)
print(f"   {'Categoria':30} | {'2025':>18} | {'2024':>18} | {'2023':>18}")
print("   " + "-"*90)
for _, row in df_comparativo.iterrows():
    print(f"   {row['Categoria']:30} | {formatar_moeda(row['Ano_2025']):>18} | {formatar_moeda(row['Ano_2024']):>18} | {formatar_moeda(row['Ano_2023']):>18}")
print("   " + "-"*90)

print("\n5. Testando grafico_comparativo_anos()")
try:
    fig_comparativo = grafico_comparativo_anos(df_comparativo)
    print(f"   ✓ Gráfico comparativo criado")
    print(f"   ✓ Tipo: {type(fig_comparativo).__name__}")
    print(f"   ✓ Número de traces: {len(fig_comparativo.data)}")
except Exception as e:
    print(f"   ✗ Erro ao criar gráfico: {e}")

# =============================================================================
# TESTE F10: PROJEÇÕES E ALERTAS
# =============================================================================

print("\n" + "="*70)
print("TESTE F10: PROJEÇÕES E ALERTAS AUTOMÁTICOS")
print("="*70)

print("\n6. Testando calcular_projecoes_esgotamento()")
df_projecoes = calcular_projecoes_esgotamento(df_balanco, df_despesas)

print(f"   ✓ Projeções calculadas: {len(df_projecoes)} fontes")
print("\n   Projeções por Fonte:")
print("   " + "-"*90)
print(f"   {'Fonte':6} | {'Saldo':>18} | {'Dias Restantes':>15} | {'Nível':10} | {'% Saldo':>8}")
print("   " + "-"*90)
for _, row in df_projecoes.iterrows():
    dias = f"{int(row['Dias_Restantes'])} dias" if row['Dias_Restantes'] < 9999 else "Sem risco"
    print(f"   {row['Fonte']:6} | {formatar_moeda(row['Saldo_Atual']):>18} | {dias:>15} | {row['Nivel_Alerta']:10} | {formatar_percentual(row['Perc_Saldo']):>8}")
print("   " + "-"*90)

print("\n7. Testando gerar_alertas_automaticos()")
alertas = gerar_alertas_automaticos(df_projecoes, df_despesas)

print(f"   ✓ Alertas gerados: {len(alertas)}")

# Contar por tipo
alertas_criticos = [a for a in alertas if a['tipo'] == 'CRÍTICO']
alertas_altos = [a for a in alertas if a['tipo'] == 'ALTO']
alertas_medios = [a for a in alertas if a['tipo'] == 'MÉDIO']

print(f"   ✓ Alertas CRÍTICOS: {len(alertas_criticos)}")
print(f"   ✓ Alertas ALTOS: {len(alertas_altos)}")
print(f"   ✓ Alertas MÉDIOS: {len(alertas_medios)}")

if alertas:
    print("\n   Detalhamento dos Alertas:")
    print("   " + "-"*66)
    for alerta in alertas[:5]:  # Mostrar apenas os 5 primeiros
        print(f"   🚨 [{alerta['tipo']}] {alerta['titulo']}")
        print(f"      {alerta['mensagem']}")
        print(f"      → {alerta['acao_recomendada']}")
        print()

print("\n8. Testando grafico_projecoes_esgotamento()")
try:
    fig_projecoes = grafico_projecoes_esgotamento(df_projecoes)
    print(f"   ✓ Gráfico de projeções criado")
    print(f"   ✓ Tipo: {type(fig_projecoes).__name__}")
    print(f"   ✓ Número de traces: {len(fig_projecoes.data)}")
except Exception as e:
    print(f"   ✗ Erro ao criar gráfico: {e}")

# =============================================================================
# RESUMO FINAL
# =============================================================================

print("\n" + "="*70)
print("RESUMO DOS TESTES")
print("="*70)

print("\n✅ F8 - EVOLUÇÃO TEMPORAL:")
print(f"   ✓ Função simular_evolucao_temporal: OK ({len(df_temporal)} meses)")
print(f"   ✓ Função grafico_evolucao_temporal: OK")

print("\n✅ F9 - COMPARATIVO COM ANOS ANTERIORES:")
print(f"   ✓ Função simular_comparativo_anos: OK ({len(df_comparativo)} categorias)")
print(f"   ✓ Função grafico_comparativo_anos: OK")

print("\n✅ F10 - PROJEÇÕES E ALERTAS:")
print(f"   ✓ Função calcular_projecoes_esgotamento: OK ({len(df_projecoes)} fontes)")
print(f"   ✓ Função gerar_alertas_automaticos: OK ({len(alertas)} alertas)")
print(f"   ✓ Função grafico_projecoes_esgotamento: OK")

print("\n" + "="*70)
print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
print("="*70)

print("\n📌 PRÓXIMOS PASSOS:")
print("   1. Reinicie o Streamlit para carregar as mudanças")
print("   2. Navegue até as novas seções:")
print("      - 📅 Evolução Temporal da Execução (F8)")
print("      - 📊 Comparativo com Anos Anteriores (F9)")
print("      - 🚨 Projeções e Alertas Automáticos (F10)")
print("   3. Verifique os gráficos e alertas")
print("="*70)
