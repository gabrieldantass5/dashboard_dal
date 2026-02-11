# 📊 Dashboard de Controle Orçamentário DAL/CBMAL

Dashboard interativo em Python para análise e controle orçamentário da Diretoria de Apoio Logístico (DAL) do Corpo de Bombeiros Militar de Alagoas (CBMAL).

**🎉 Status:** ✅ **100% OPERACIONAL E VALIDADO**

## 🎯 Objetivo

Substituir a planilha Excel complexa (12 abas, 302 processos) por uma interface visual, dinâmica e intuitiva que permite:
- ✅ Visualizar saldos disponíveis por fonte de recursos em tempo real
- ✅ Comparar orçado vs executado por categoria
- ✅ Filtrar e analisar processos de forma interativa
- ✅ Exportar dados filtrados para análise externa

## 📈 Dados Validados

Os valores foram validados com o Excel original:
- **Total de Recursos:** R$ 27.281.568,51 ✅
- **Total Empenhado:** R$ 23.382.410,38 ✅
- **Saldo Disponível:** R$ 3.899.158,13 ✅
- **Processos Ativos:** 259 (279 total, 20 cancelados) ✅
- **Taxa de Execução:** 89,41% ✅

## 🚀 Funcionalidades (MVP)

### Painel de KPIs
- Total de Recursos
- Total Empenhado
- Saldo Disponível
- Processos Ativos
- Taxa de Execução

### Visualizações Interativas
- **Saldo por Fonte**: Gráfico de barras agrupadas com detalhamento das 5 fontes de recursos (500, 501, 753, 759, 622)
- **Orçado vs Executado**: Comparativo por elemento de despesa com alertas para categorias > 95%
- **Tabela de Despesas**: Tabela completa com busca, ordenação e exportação CSV

### Filtros Globais
- Fontes de Recursos (multiselect)
- Status dos Processos (multiselect)

## 📋 Requisitos

### Sistema
- **Python:** 3.9 ou superior
- **Sistema Operacional:** Windows 10/11, macOS, Linux
- **Navegador:** Chrome 90+, Firefox 88+, Edge 90+

### Dados
- Arquivo `ORÇAMENTO 2025 (1).xlsx` na pasta `data/`

## 🛠️ Instalação

### 1. Clonar ou baixar o projeto

```bash
# Se estiver usando Git
git clone <url-do-repositorio>
cd Dashboard-DAL

# Ou baixar e extrair o ZIP
```

### 2. Criar ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Adicionar arquivo Excel

Copie o arquivo `ORÇAMENTO 2025 (1).xlsx` para a pasta `data/`

```
Dashboard-DAL/
├── data/
│   └── ORÇAMENTO 2025 (1).xlsx  ← Adicionar aqui
```

## ▶️ Como Executar

### Passo 1: Ativar Ambiente Virtual

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Passo 2: Executar Dashboard

```bash
streamlit run app.py
```

Ou com modo headless (sem interação inicial):

```bash
streamlit run app.py --server.headless=true
```

### Passo 3: Acessar

O dashboard será aberto automaticamente em seu navegador ou acesse:

**👉 http://localhost:8501**

### Primeiro Acesso

1. **Aguarde o carregamento** dos dados (3-5 segundos na primeira vez)
   - Você verá logs no terminal indicando o progresso
   - Mensagem "CARREGAMENTO CONCLUÍDO COM SUCESSO" indica que está pronto

2. **Use os filtros** na barra lateral para segmentar a visualização
   - Fontes de Recursos (500, 501, 753, 759, 622)
   - Status dos Processos (Empenhado, Reservado, Em análise, Cancelado)

3. **Interaja com os gráficos**
   - Hover: passe o mouse sobre as barras para ver valores
   - Zoom: use scroll do mouse
   - Pan: arraste o gráfico

4. **Use a busca** na tabela para localizar processos específicos
   - Digite número do processo ou palavra-chave do objeto
   - Busca em tempo real

5. **Exporte dados** clicando em "⬇️ Baixar CSV"
   - Arquivo compatível com Excel (UTF-8-BOM)

## 📁 Estrutura do Projeto

```
Dashboard-DAL/
├── app.py                      # Aplicação principal Streamlit
├── src/
│   ├── data_loader.py         # Carregamento e limpeza de dados
│   ├── data_processor.py      # Processamento e cálculos
│   ├── visualizations.py      # Gráficos Plotly
│   └── utils.py               # Funções auxiliares
├── data/
│   └── ORÇAMENTO 2025 (1).xlsx # Planilha de dados (não versionada)
├── docs/
│   ├── 01_BRIEFING.md         # Contexto do projeto
│   ├── 02_PRD.md              # Product Requirements Document
│   ├── 03_MVP.md              # Definição do MVP
│   └── 04_SPECS_TECNICAS.md   # Especificações técnicas
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
├── CLAUDE.md                  # Guia para Claude Code
└── .gitignore                 # Arquivos ignorados pelo Git
```

## 📊 Fontes de Dados

O dashboard processa as seguintes abas do Excel:

### Abas Utilizadas (MVP)
- **CONTROLE DE DESPESAS**: Processos, valores, status
- **BALANCO**: Recursos, dotado, empenhado por fonte

### Abas para Versões Futuras
- PCA 2025
- Despesas 2025
- RECURSOS TESOURO 2025

## 🎨 Funcionalidades Detalhadas

### Filtros
- **Fontes de Recursos**: 500 (Tesouro), 501, 753 (Convênios), 759 (Fundos), 622 (SUS)
- **Status**: Empenhado, Reservado, Em análise, Cancelado

### Exportação
- Formato: CSV com encoding UTF-8-BOM (compatível com Excel)
- Conteúdo: Dados filtrados visíveis na tabela
- Colunas: Processo, Objeto, Valor, Fonte, Elemento, Status

## 🔧 Solução de Problemas

### ❌ Dashboard não abre

**Erro:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solução:**
```bash
# Ativar ambiente virtual primeiro
venv\Scripts\activate

# Instalar/atualizar dependências
pip install -r requirements.txt
```

---

### ❌ Erro ao carregar Excel

**Erro:**
```
FileNotFoundError: data/ORÇAMENTO 2025 (1).xlsx
```

**Solução:**
1. Verificar se o arquivo está na pasta `data/`
2. Verificar nome exato (incluindo espaços e parênteses)
3. Verificar extensão (.xlsx, não .xls)

**Comando para verificar:**
```bash
ls -la data/
# Deve mostrar: ORÇAMENTO 2025 (1).xlsx
```

---

### ❌ Valores não batem com Excel

**Solução:**
1. Verificar se está usando a versão mais recente da planilha
2. Limpar cache do Streamlit:
   - Pressionar `C` na interface do dashboard
   - Ou clicar no menu ☰ → "Clear cache"
   - Ou reiniciar o servidor (Ctrl+C e executar novamente)

3. Verificar logs no terminal:
   - Deve mostrar "✅ VALIDAÇÃO: Valores batem com Excel"
   - Se não mostrar, verificar se a planilha foi modificada

---

### ❌ Performance lenta

**Causas:**
- Primeira execução (sem cache)
- Muitos processos abertos
- Excel aberto simultaneamente

**Solução:**
1. **Primeira vez:** Aguardar carregamento inicial (3-5s)
   - Cache será aplicado automaticamente
   - Próximos acessos serão instantâneos

2. **Excel aberto:** Fechar o arquivo Excel
   - Pode causar conflito de acesso ao arquivo

3. **Recursos limitados:** Fechar outras aplicações

---

### ❌ Gráficos não aparecem

**Solução:**
1. Verificar console do navegador (F12)
2. Atualizar página (Ctrl+F5 ou Cmd+R)
3. Testar em navegador diferente (Chrome, Firefox, Edge)
4. Verificar logs no terminal para erros

---

### ❌ Filtros não funcionam

**Solução:**
1. Verificar se há dados para os filtros selecionados
2. Limpar filtros clicando em "🔄 Limpar Filtros"
3. Recarregar página (F5)

---

### ⚠️ Warnings sobre `use_container_width`

**Mensagem:**
```
Please replace `use_container_width` with `width`.
```

**Explicação:** São avisos de deprecação do Streamlit, **não são erros**. O dashboard funciona perfeitamente. Serão atualizados em versão futura.

---

### 🛑 Para Parar o Dashboard

```bash
# Pressionar Ctrl+C no terminal
# Ou fechar a janela do terminal
```

## 📚 Documentação Disponível

### Para Usuários Finais

- **📘 [`MANUAL_USUARIO.md`](MANUAL_USUARIO.md)** ⭐ **COMECE AQUI!**
  - Guia completo passo a passo
  - Como usar cada funcionalidade
  - Exemplos práticos de uso
  - Perguntas frequentes
  - 11 seções detalhadas

- **📄 [`README.md`](README.md)** (este arquivo)
  - Guia rápido de instalação
  - Visão geral do projeto
  - Comandos essenciais

- **✅ [`TESTES.md`](TESTES.md)**
  - Checklist de validação
  - Guia de testes
  - Solução de problemas

### Para Desenvolvedores

- **🤖 [`CLAUDE.md`](CLAUDE.md)**
  - Guia técnico do projeto
  - Arquitetura e estrutura
  - Convenções de código

- **📋 [`docs/01_BRIEFING.md`](docs/01_BRIEFING.md)**
  - Contexto do projeto
  - Objetivos e requisitos

- **📊 [`docs/02_PRD.md`](docs/02_PRD.md)**
  - Product Requirements Document
  - Funcionalidades detalhadas
  - User stories

- **🎯 [`docs/03_MVP.md`](docs/03_MVP.md)**
  - Definição do MVP
  - Roadmap de versões

- **⚙️ [`docs/04_SPECS_TECNICAS.md`](docs/04_SPECS_TECNICAS.md)**
  - Especificações técnicas
  - Estrutura de dados
  - Design de implementação

## 🗺️ Roadmap

### ✅ Versão 1.0 (MVP) - Atual
- Painel de KPIs
- Saldo por fonte
- Orçado vs executado (por elemento)
- Filtros básicos
- Tabela de despesas

### 🔄 Versão 2.0 (Próxima)
- Gráficos de status de processos
- Execução do PCA 2025
- Granularidades adicionais (por fonte, por ação PCA)
- Formatação condicional na tabela

### 🚀 Versão 3.0 (Futuro)
- Evolução temporal (gráficos de linha)
- Comparativos com anos anteriores
- Projeções de execução

### 🌐 Versão 4.0+ (Longo Prazo)
- Deploy em servidor/nuvem
- Autenticação de usuários
- Integração com Google Sheets API
- Alertas automáticos por email

## 🤝 Contribuindo

Este projeto é mantido pela DAL/CBMAL. Para sugestões ou correções:
1. Documente o problema ou sugestão
2. Entre em contato com a equipe responsável
3. Aguarde revisão e aprovação

## 📄 Licença

Uso interno - Corpo de Bombeiros Militar de Alagoas (CBMAL)

## 👥 Equipe

- **Desenvolvimento**: Claude Code + Analista de Dados DAL
- **Patrocinador**: Diretor de Apoio Logístico
- **Usuários**: Equipe DAL e Diretoria Financeira CBMAL

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a documentação em `docs/`
- Entre em contato com a equipe de TI do CBMAL
- Verifique issues conhecidas no repositório

---

**Desenvolvido com ❤️ em Python | Streamlit + Plotly + Pandas**

**Última atualização**: 11/02/2026 | Versão 1.0 MVP
