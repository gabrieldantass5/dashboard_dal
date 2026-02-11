# 📚 Guia de Estudos: Data Visualization & Storytelling com Dados

Este guia reúne as melhores referências, livros, cursos e repositórios para você se tornar um especialista em transformar dados brutos em decisões estratégicas através de visualizações eficazes.

---

## 📖 1. Livros Fundamentais (A Base de Tudo)

### **A Bíblia: Storytelling com Dados**

* **Autora:** Cole Nussbaumer Knaflic
* **Foco:** Um guia prático que ensina a eliminar a poluição visual e focar no que realmente importa.
* **O que você aprende:** Escolha de gráficos, foco da atenção do usuário e narrativa.
* **Site:** [storytellingwithdata.com](https://www.storytellingwithdata.com/)

### **A Eficácia: Show Me the Numbers**

* **Autor:** Stephen Few
* **Foco:** Design de tabelas e gráficos para comunicação em negócios.
* **O que você aprende:** Como o cérebro processa números e como exibir dados densos de forma clara em dashboards.

### **O Clássico: The Visual Display of Quantitative Information**

* **Autor:** Edward Tufte
* **Foco:** Teoria acadêmica e histórica da visualização.
* **Conceito chave:** *Data-Ink Ratio* (maximizar a tinta usada para dados, minimizar a tinta decorativa).

---

## 🛠️ 2. Ferramentas de Decisão (Qual gráfico usar?)

Quando você tiver um dado e não souber como mostrar, consulte estes "mapas":

1. **Financial Times Visual Vocabulary:**
    * Um guia que divide gráficos por intenção (Comparação, Correlação, Distribuição, Tempo).
    * [Versão em Português (PDF)](https://github.com/ft-interactive/chart-doctor/blob/master/visual-vocabulary/Visual-vocabulary-Portuguese.pdf)
2. **From Data to Viz:**
    * Um fluxograma interativo: você escolhe o tipo de dado e ele te leva ao gráfico ideal.
    * [data-to-viz.com](https://www.data-to-viz.com/)
3. **The Data Visualisation Catalogue:**
    * Uma enciclopédia interativa de todos os tipos de gráficos existentes.
    * [datavizcatalogue.com](https://datavizcatalogue.com/)
4. **Chart Chooser (Luzerner Richtlinien):**
    * Um site simples para decidir rapidamente entre as opções mais comuns.
    * [chartpicker.com](https://chartpicker.com/)

---

## 💻 3. Repositórios do GitHub (Código e Exemplos)

### **Listas "Awesome" (Curadoria)**

* [**hal9ai/awesome-dataviz**](https://github.com/hal9ai/awesome-dataviz): A maior lista de recursos de DataViz do mundo. Bibliotecas, blogs e catálogos.
* [**ft-interactive/chart-doctor**](https://github.com/ft-interactive/chart-doctor): Repositório do Financial Times com guias de design e o Visual Vocabulary.

### **Prática e Implementação**

* [**streamlit/gallery**](https://github.com/streamlit/gallery): Exemplos reais de dashboards feitos com a ferramenta que usamos no projeto DAL.
* [**The Economist Graphic Detail**](https://github.com/TheEconomist/graphic-detail): Referência em design elegante e minimalista.
* [**Urban Institute Style Guide**](https://github.com/UrbanInstitute/documentation): Um excelente manual de como padronizar cores, fontes e eixos em um dashboard profissional.

---

## 🎓 4. Cursos e Conteúdo Online

* **Google Data Analytics (Coursera):** Possui um módulo excelente apenas sobre visualização.
* **Data Visualization Specialization (UC Davis/Coursera):** Mais focado em ferramentas de mercado e teoria.
* **Escola de Dados (Brasil):** Excelente conteúdo em português focado em transparência e clareza de dados.

---

## 🧠 5. Regras de Ouro do "Designer de Dados"

Para o Dashboard orçamentário, lembre-se sempre:

1. **Menos é Mais:** Se um elemento (borda, grade, sombra) não ajuda a ler o dado, ele deve ser removido.
2. **A Prova dos 5 Segundos:** O usuário deve entender a mensagem principal do gráfico em no máximo 5 segundos.
3. **O Tempo é uma Linha:** Dados temporais pedem gráficos de linha (eixo X sempre para o tempo).
4. **Barras são rainhas:** O olho humano é excepcional em comparar o comprimento de barras. Na dúvida, use barras.
5. **Cor é Informação:** Não use cores apenas para decorar. Use cores para destacar alertas (Vermelho para crítico, Verde para normal) ou para separar categorias.

---

*Compilado por Antigravity AI para o Projeto Dashboard Orçamentário DAL/CBMAL.*
