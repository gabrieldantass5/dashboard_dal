# BRIEFING - Dashboard Orçamentário DAL/CBMAL

## 1. CONTEXTO

**Cliente/Organização:** CBMAL (Corpo de Bombeiros Militar de Alagoas)
**Área:** Diretoria de Apoio Logístico (DAL) + Diretoria Financeira
**Data:** Fevereiro 2025

### Situação Atual
- Planilha Excel complexa com 12 abas gerenciada manualmente
- Sincronização manual com Google Sheets
- Análise visual limitada e estática
- Dificuldade em extrair insights rápidos
- Processo de atualização e consulta demorado

### Problema
Falta de ferramentas interativas e automatizadas para:
- Acompanhamento em tempo real do orçamento
- Visualização dinâmica de despesas e recursos
- Análise comparativa entre fontes de recursos
- Monitoramento do status de processos e empenhos
- Geração de relatórios gerenciais

## 2. OBJETIVO

Criar um **Dashboard Interativo em Python** para visualização e análise do orçamento 2025 da DAL/CBMAL, com foco em:
- **Didático:** Fácil de entender para todos os níveis hierárquicos
- **Informativo:** Mostrar métricas e KPIs relevantes
- **Dinâmico:** Interatividade e filtros para drill-down
- **Completo:** Atender todas as necessidades de análise orçamentária

## 3. DADOS DISPONÍVEIS

### Fonte de Dados
- **Arquivo:** ORÇAMENTO 2025 (1).xlsx
- **Origem:** Cópia de planilha Google Sheets atualizada manualmente
- **Atualização:** Manual (a definir periodicidade)

### Estrutura de Dados

#### Aba: CONTROLE DE DESPESAS (303 registros)
- Número do Processo
- Objeto (descrição da despesa)
- Valor
- Fonte (500, 501, 753, 759...)
- Elemento de Despesa (CONSUMO, PERMANENTE, SERVIÇO PJ)
- Nota de Reserva (True/False)
- Nota de Empenho (True/False)
- Ação do PCA 2025
- Observação/Status

#### Aba: BALANCO (67 registros)
- Saldos de recursos
- Controle de dotações

#### Aba: RECURSOS MODERNIZAÇÃO 2025 (43 registros)
- Recursos específicos de modernização

#### Aba: RECURSOS TESOURO 2025 (28 registros)
- Recursos do tesouro estadual

#### Aba: PCA 2025 (43 registros)
- Plano de Contratações Anual

#### Outras Abas
- PAINEL (21 registros) - Dashboard consolidado
- AUX BALANCO - Dados auxiliares
- RELATÓRIO - Relatórios customizados
- CONTROLE - Controles gerais
- Despesas 2025 - Categorização de despesas

## 4. PÚBLICO-ALVO (PERSONAS)

### Persona 1: Diretor de Apoio Logístico
- **Necessidade:** Visão estratégica e consolidada do orçamento
- **Uso:** Acompanhamento mensal, tomada de decisão, apresentações
- **Nível técnico:** Básico

### Persona 2: Gestor Financeiro
- **Necessidade:** Controle detalhado de empenhos e saldos
- **Uso:** Análise diária, controle de processos, relatórios
- **Nível técnico:** Intermediário

### Persona 3: Analista de Dados/Controladoria
- **Necessidade:** Análises aprofundadas e cruzamentos de dados
- **Uso:** Estudos, projeções, auditorias
- **Nível técnico:** Avançado

## 5. REQUISITOS PRELIMINARES

### Funcionais
- [ ] Importar dados do Excel automaticamente
- [ ] Visualizar despesas por categoria, fonte e elemento
- [ ] Filtrar por status (reservado, empenhado, cancelado)
- [ ] Comparar orçado vs executado
- [ ] Acompanhar saldo disponível por fonte
- [ ] Visualizar evolução temporal das despesas
- [ ] Exportar gráficos e relatórios

### Não-Funcionais
- [ ] Interface amigável e intuitiva
- [ ] Responsivo (adaptável a diferentes tamanhos de tela)
- [ ] Performance: carregar dados em < 5 segundos
- [ ] Código limpo e documentado (fins educacionais)
- [ ] Facilidade de manutenção e evolução

## 6. RESTRIÇÕES E PREMISSAS

### Restrições
- Desenvolvedor iniciante em Python
- Orçamento zero (uso de bibliotecas open-source)
- Dados sensíveis (não compartilhar publicamente)
- Atualização manual dos dados (sem integração automática inicial)

### Premissas
- Usuário tem Python instalado
- Conhecimento básico de análise de dados
- Acesso à planilha Excel atualizada periodicamente
- Ambiente local (não precisa de deploy em servidor inicialmente)

## 7. SUCESSO DO PROJETO

### Critérios de Sucesso
1. Dashboard funcional com mínimo 5 visualizações diferentes
2. Redução de 70% no tempo de análise orçamentária
3. Interface intuitiva aprovada pelos usuários
4. Código documentado servindo como material de estudo
5. Facilidade de atualização dos dados (< 2 minutos)

### Métricas de Acompanhamento
- Tempo de carregamento dos dados
- Número de visualizações implementadas
- Feedback dos usuários (escala 1-5)
- Cobertura de requisitos atendidos

## 8. PRÓXIMOS PASSOS

1. ✅ Briefing aprovado
2. → Criar PRD (Product Requirements Document)
3. → Definir MVP
4. → Especificações técnicas
5. → Desenvolvimento
6. → Testes e validação

---

**Documento criado em:** 11/02/2025
**Versão:** 1.0
**Status:** Em aprovação
