---
name: visual-diagrams-cbmal
description: Orquestrador de Diagramas Estratégicos CBMAL. Usa o framework PaperBanana para planejar, estilizar e validar diagramas (fluxogramas, organogramas, processos) com identidade visual CBMAL v2.0.
---

# 📊 visual-diagrams-cbmal

Esta skill eleva a criação de diagramas técnicos e estratégicos ao padrão **PaperBanana**, garantindo que processos e metodologias do CBMAL sejam visualizados com precisão militar e estética premium.

---

## 🎯 Quando Usar

1. **Documentação de Processos**: Mapear fluxos de trabalho no SEI ou normas internas.
2. **Apresentações Estratégicas**: Criar visualizações de metodologias para o Comando Geral.
3. **Planejamento de Sistemas**: Visualizar arquiteturas de software ou fluxos de dados.

---

## 🏗️ Arquitetura Agêntica (Modo PaperBanana)

A skill opera através de um pipeline de 5 etapas:

| Agente | Ação |
|---|---|
| **Retriever** | Busca modelos de diagramas CBMAL similares no corpus visual. |
| **Planner** | Traduz a descrição textual bruta em uma estrutura lógica (nós e conexões). |
| **Stylist** | Aplica o CBMAL Brand System (Cores: `#DC1B13`, `#4C7695`, `#F2F2F2`). |
| **Visualizer** | Gera o código Mermaid otimizado e renderiza via `mermaid-engine`. |
| **Critic** | Audita a complexidade do diagrama (max 15 nós por visualização para clareza). |

---

## 🛠️ Comandos CLI

### 1. Gerar Diagrama a partir de Texto

```bash
python scripts/diagram_generator_cbmal.py "Descrição do processo..."
```

**Parâmetros opcionais:**

- `--type`: `flowchart`, `sequence`, `gantt`, `class` (default: `flowchart`)
- `--output`: Caminho do arquivo de saída (default: `Inbox/diagrama.svg`)

---

## 🎨 Especificações Visuais (Brand v2.0)

Baseado nos dados empíricos extraídos na Fase 2:

- **Primary Color (Arrows/Nodes)**: `#DC1B13` (Vermelho CBMAL)
- **Secondary Color (Active Modules)**: `#4C7695` (Azul de Destaque)
- **Background/Grouping**: `#F2F2F2` (Cinza Contraste)
- **Font**: Oswald ou Roboto Mono (para códigos).

---

## 🚀 Fluxo de Trabalho

1. O usuário fornece uma descrição textual de um processo.
2. O Agente executa a skill `visual-diagrams-cbmal`.
3. O sistema gera o código Mermaid in-memory.
4. O Critic Agent valida a legibilidade (veto de diagramas "espaguete").
5. O resultado final é salvo como `.svg` e código `.md`.

---
**Skill desenvolvida pela APO/EMG** | Inspirada em PaperBanana (Zhu et al., 2026)
