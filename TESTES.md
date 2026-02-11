# Guia de Testes e Validação
## Dashboard de Controle Orçamentário DAL/CBMAL

**Versão:** 1.0 MVP
**Data:** 11/02/2026

---

## 📋 Checklist de Testes Pré-Execução

Antes de executar o dashboard pela primeira vez, verifique:

- [ ] Python 3.9+ instalado (`python --version`)
- [ ] Arquivo `ORÇAMENTO 2025 (1).xlsx` na pasta `data/`
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)

---

## 🚀 Como Executar o Dashboard

### 1. Ativar Ambiente Virtual

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Executar Streamlit

```bash
streamlit run app.py
```

### 3. Aguardar Carregamento

- O terminal mostrará logs de carregamento
- O navegador abrirá automaticamente em `http://localhost:8501`
- Aguarde 3-5 segundos para carregamento inicial

---

## ✅ Checklist de Validação Funcional

### Carregamento de Dados

- [ ] Excel carrega sem erros
- [ ] Aba "CONTROLE DE DESPESAS" processada corretamente
- [ ] Aba "BALANCO" processada corretamente
- [ ] Logs no terminal mostram "CARREGAMENTO CONCLUÍDO COM SUCESSO"

### KPIs Principais

Verifique se os valores estão corretos (tolerância de ±R$ 100):

- [ ] **Total de Recursos**: ~R$ 27.281.568,51
- [ ] **Total Empenhado**: ~R$ 23.382.410,38
- [ ] **Saldo Disponível**: ~R$ 3.899.158,13
- [ ] **Processos Ativos**: ~279 (número pode variar)
- [ ] **Taxa de Execução**: ~85-86%

### Saldo por Fonte

- [ ] Gráfico exibe 5 fontes (500, 501, 753, 759, 622)
- [ ] Barras agrupadas visíveis (Recursos, Dotado, Empenhado, Saldo)
- [ ] Hover mostra valores formatados em R$
- [ ] Tabela lateral mostra dados corretos
- [ ] % Execução calculada corretamente

### Orçado vs Executado

- [ ] Gráfico compara orçado e executado
- [ ] Barras horizontais lado a lado
- [ ] Ordenação decrescente por valor executado
- [ ] Alerta aparece se categoria > 95%
- [ ] Cores condicionais aplicadas (verde, amarelo, vermelho)

### Filtros

- [ ] Filtro de fontes funciona (multiselect)
- [ ] Filtro de status funciona (multiselect)
- [ ] Todos os gráficos atualizam ao aplicar filtros
- [ ] Resposta em < 1 segundo
- [ ] Botão "Limpar Filtros" funciona

### Tabela Detalhada

- [ ] Exibe todos os processos filtrados
- [ ] Busca por processo funciona
- [ ] Busca por objeto funciona
- [ ] Valores formatados em R$
- [ ] Download CSV funciona
- [ ] CSV abre corretamente no Excel (encoding UTF-8-BOM)

### Performance

- [ ] Carregamento inicial < 5 segundos
- [ ] Aplicação de filtros < 1 segundo
- [ ] Gráficos renderizam < 1 segundo
- [ ] Exportação CSV < 2 segundos
- [ ] Dashboard responsivo (sem travamentos)

---

## 🔍 Validação de Dados (10 Valores-Chave)

Compare os valores do dashboard com o Excel original:

| # | Métrica | Localização Excel | Valor Dashboard | Validado? |
|---|---------|-------------------|-----------------|-----------|
| 1 | Total Recursos | BALANCO, linha RECURSOS, SOMATÓRIO | _______________ | [ ] |
| 2 | Total Empenhado | BALANCO, linha EMPENHADO, SOMATÓRIO | _______________ | [ ] |
| 3 | Recursos Fonte 500 | BALANCO, linha RECURSOS, col 500 | _______________ | [ ] |
| 4 | Empenhado Fonte 500 | BALANCO, linha EMPENHADO, col 500 | _______________ | [ ] |
| 5 | Saldo Fonte 500 | Calculado (R - E) | _______________ | [ ] |
| 6 | % Execução Fonte 500 | (E / D) × 100 | _______________ | [ ] |
| 7 | Número total de processos | Contagem em CONTROLE DE DESPESAS | _______________ | [ ] |
| 8 | Processos Empenhados | Contagem onde Status = "Empenhado" | _______________ | [ ] |
| 9 | Valor processo específico | Escolher 1 processo aleatório | _______________ | [ ] |
| 10 | Total por elemento "CONSUMO" | Soma em CONTROLE DE DESPESAS | _______________ | [ ] |

**Critério de Aprovação:** 10/10 valores corretos (tolerância ±R$ 0,10)

---

## 🧪 Testes de Interatividade

### Teste 1: Filtro por Fonte Única

1. Selecionar apenas fonte 500 no filtro
2. Verificar:
   - [ ] KPI "Total de Recursos" atualiza
   - [ ] Gráfico de saldo mostra apenas fonte 500
   - [ ] Tabela mostra apenas processos da fonte 500
   - [ ] Contadores atualizados

### Teste 2: Filtro por Status

1. Desmarcar "Cancelado" no filtro de status
2. Verificar:
   - [ ] Processos cancelados não aparecem na tabela
   - [ ] Contadores atualizados
   - [ ] KPIs recalculados

### Teste 3: Busca na Tabela

1. Digitar número de processo na busca (ex: "498")
2. Verificar:
   - [ ] Tabela filtra em tempo real
   - [ ] Contador "Processos exibidos" atualiza
   - [ ] Processo correto aparece

### Teste 4: Download CSV

1. Aplicar filtros (ex: apenas fonte 500, status "Empenhado")
2. Clicar em "Baixar CSV"
3. Abrir CSV no Excel
4. Verificar:
   - [ ] Arquivo abre sem erros
   - [ ] Acentos estão corretos (UTF-8-BOM)
   - [ ] Apenas dados filtrados estão presentes
   - [ ] Valores numéricos corretos

### Teste 5: Hover nos Gráficos

1. Passar mouse sobre barras do gráfico de saldo
2. Verificar:
   - [ ] Tooltip aparece
   - [ ] Valores formatados em R$
   - [ ] Informações corretas

---

## ⚠️ Testes de Edge Cases

### Caso 1: Nenhum Filtro Selecionado

1. Desmarcar todas as fontes no filtro
2. Verificar:
   - [ ] Dashboard mostra mensagem de "nenhum dado" ou array vazio
   - [ ] Não ocorre erro fatal

### Caso 2: Busca Sem Resultados

1. Buscar por termo inexistente (ex: "XYZABC123")
2. Verificar:
   - [ ] Tabela vazia
   - [ ] Contador mostra 0 processos
   - [ ] Não ocorre erro

### Caso 3: Planilha com Dados Inconsistentes

1. (Teste opcional) Modificar Excel com valores nulos/inválidos
2. Verificar:
   - [ ] Dashboard trata valores nulos
   - [ ] Logs mostram warnings
   - [ ] Não ocorre crash

---

## 🐛 Problemas Conhecidos e Soluções

### Problema 1: Dashboard não abre

**Erro:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solução:**
```bash
pip install -r requirements.txt
```

---

### Problema 2: Excel não encontrado

**Erro:**
```
FileNotFoundError: data/ORÇAMENTO 2025 (1).xlsx
```

**Solução:**
1. Verificar se arquivo está na pasta `data/`
2. Verificar nome exato (incluindo espaços e parênteses)
3. Verificar extensão (.xlsx, não .xls)

---

### Problema 3: Valores não batem com Excel

**Possível Causa:**
- Versão desatualizada do Excel
- Cache do Streamlit desatualizado

**Solução:**
1. Verificar se está usando a versão mais recente do Excel
2. Limpar cache do Streamlit:
   - Pressionar `C` na interface do dashboard
   - Ou reiniciar o servidor

---

### Problema 4: Performance lenta

**Possível Causa:**
- Excel muito grande
- Muitos processos abertos

**Solução:**
1. Aguardar carregamento inicial (só ocorre 1 vez)
2. Fechar outras aplicações
3. Verificar se Excel não está aberto simultaneamente

---

### Problema 5: Erro ao importar módulos

**Erro:**
```
ModuleNotFoundError: No module named 'src'
```

**Solução:**
1. Verificar se arquivo `src/__init__.py` existe
2. Executar `streamlit run app.py` da raiz do projeto
3. Não executar de dentro da pasta `src/`

---

## 📊 Logs de Debug

### Ativar Modo Debug

1. No dashboard, marcar checkbox "🔧 Modo Debug" na sidebar
2. Verificar seção de debug no rodapé
3. Expandir "Ver dados brutos" para inspecionar DataFrames

### Logs no Terminal

Durante execução, o terminal mostra:

```
INFO - 📂 Carregando Excel: data/ORÇAMENTO 2025 (1).xlsx
INFO - ✓ Aba 'CONTROLE DE DESPESAS' carregada: (303, 9)
INFO - ✓ Aba 'BALANCO' carregada: (67, 15)
INFO - 🧹 Limpando aba CONTROLE DE DESPESAS...
INFO -    Linhas após remover vazias: 279
INFO -    ✓ Processos limpos: 279
INFO -    ✓ Total de recursos: R$ 23.382.410,38
INFO - 🧹 Limpando aba BALANCO...
INFO -    ✓ Total de Recursos: R$ 27.281.568,51
INFO -    ✓ Total Empenhado: R$ 23.382.410,38
INFO - ✅ VALIDAÇÃO: Valores batem com Excel
```

---

## ✅ Checklist de Entrega Final

- [ ] Todos os 10 valores validados com Excel
- [ ] Performance atende requisitos (< 5s carregamento)
- [ ] Todos os filtros funcionam
- [ ] Busca na tabela funciona
- [ ] Download CSV funciona
- [ ] Gráficos são interativos
- [ ] Não há erros no terminal
- [ ] README.md está atualizado
- [ ] Documentação completa em docs/

---

## 📝 Relatório de Testes

**Data dos Testes:** ___/___/______

**Testador:** _________________________

**Resultado:** [ ] APROVADO  [ ] REPROVADO

**Observações:**

_______________________________________________________

_______________________________________________________

_______________________________________________________

---

## 🎯 Próximos Passos (Pós-Validação)

1. **Demo para Usuários**
   - Apresentar dashboard para Diretor e Gestores
   - Coletar feedback inicial
   - Documentar sugestões

2. **Treinamento**
   - Treinar usuários em como usar filtros
   - Mostrar como exportar CSV
   - Explicar como interpretar gráficos

3. **Ajustes Finais**
   - Implementar feedback urgente
   - Corrigir bugs encontrados
   - Atualizar documentação

4. **Planejamento v2.0**
   - Priorizar features Post-MVP
   - Definir cronograma
   - Alocar recursos

---

**Documento elaborado por:** Claude Code
**Versão:** 1.0 MVP
**Status:** ✅ Pronto para testes
