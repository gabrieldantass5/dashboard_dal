"""
Script de Análise para F8, F9 e F10
Verifica dados disponíveis para implementação
"""

import pandas as pd
from pathlib import Path

print("="*60)
print("ANÁLISE DE DADOS PARA F8, F9 E F10")
print("="*60)

arquivo_excel = Path("data/ORÇAMENTO 2025 (1).xlsx")
excel = pd.ExcelFile(arquivo_excel)

print("\n1. Abas disponíveis no Excel:")
print("-"*60)
for idx, aba in enumerate(excel.sheet_names, 1):
    print(f"   {idx}. {aba}")

print("\n2. Análise para F8 - Evolução Temporal:")
print("-"*60)
print("   Verificando se há dados de datas/meses...")

# Verificar CONTROLE DE DESPESAS
df_despesas = pd.read_excel(excel, 'CONTROLE DE DESPESAS', header=None)
print(f"   - CONTROLE DE DESPESAS: {df_despesas.shape}")

# Procurar colunas com datas
colunas_com_data = []
for col in df_despesas.columns:
    sample = df_despesas[col].dropna().head(10)
    if any(isinstance(x, pd.Timestamp) for x in sample):
        colunas_com_data.append(col)

if colunas_com_data:
    print(f"   ✓ Encontradas {len(colunas_com_data)} colunas com datas")
else:
    print("   ⚠️  Nenhuma coluna com datas encontrada")
    print("   → F8 requer dados históricos mensais (não disponível)")

print("\n3. Análise para F9 - Comparativos com Anos Anteriores:")
print("-"*60)
print("   Verificando se há dados de 2024 ou 2023...")

# Procurar abas ou arquivos de anos anteriores
anos_anteriores = [aba for aba in excel.sheet_names if '2024' in aba or '2023' in aba]
if anos_anteriores:
    print(f"   ✓ Encontradas abas: {anos_anteriores}")
else:
    print("   ⚠️  Nenhuma aba de anos anteriores encontrada")
    print("   → F9 requer arquivo de orçamento 2024 (não disponível)")

# Verificar se há arquivo de 2024
arquivo_2024 = Path("data/ORÇAMENTO 2024.xlsx")
if arquivo_2024.exists():
    print(f"   ✓ Arquivo encontrado: {arquivo_2024}")
else:
    print(f"   ⚠️  Arquivo não encontrado: {arquivo_2024}")

print("\n4. Análise para F10 - Projeções e Alertas:")
print("-"*60)
print("   Verificando dados necessários para projeções...")

# Para projeções, precisamos de:
# 1. Saldo atual por fonte (✓ já temos)
# 2. Taxa de execução mensal (precisa de dados temporais)
# 3. Processos em pipeline (reservados)

print("   ✓ Saldo atual por fonte: DISPONÍVEL")
print("   ✓ Processos reservados: DISPONÍVEL")
print("   ⚠️  Taxa de execução mensal: REQUER DADOS TEMPORAIS")
print("   → F10 pode ser implementado com projeção linear simplificada")

print("\n" + "="*60)
print("RESUMO E RECOMENDAÇÕES")
print("="*60)

print("\n✅ VIÁVEL COM DADOS ATUAIS:")
print("   - F10: Projeções e Alertas Automáticos")
print("     → Usar projeção linear baseada em taxa de execução atual")
print("     → Alertar quando saldo < 10% ou < R$ 500k")

print("\n⚠️  REQUER DADOS ADICIONAIS:")
print("   - F8: Evolução Temporal")
print("     → Requer datas de empenho ou dados mensais")
print("     → Alternativa: Simular com dados agregados")
print("   - F9: Comparativos com Anos Anteriores")
print("     → Requer arquivo de orçamento 2024")
print("     → Alternativa: Criar dados mockados para demonstração")

print("\n💡 ESTRATÉGIA RECOMENDADA:")
print("   1. Implementar F10 com dados reais (viável)")
print("   2. Implementar F8 e F9 com placeholders/simulação")
print("   3. Documentar requisitos para versão completa")

print("="*60)
