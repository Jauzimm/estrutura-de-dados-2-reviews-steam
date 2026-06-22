# Prompt Melhorado — Roteiro para Canva em 3 Partes

Este arquivo reorganiza o conteúdo do `prompt_melhorado.md` em três blocos visuais para montar uma apresentação clara no Canva.

---

# Parte 1 — Problema, Contexto e Regras do Projeto

## Ideia central
Criar um sistema de sumarização extrativa para avaliações de jogos da Steam usando grafos. O sistema deve selecionar frases originais das reviews que representem bem a opinião dos jogadores, evitando repetição.

## O que mostrar no Canva
- Capa: nome do projeto, disciplina EDA2, Grupo 11 e tema sorteado.
- Problema: muitas avaliações são longas e repetitivas; o objetivo é gerar um resumo curto e representativo.
- Solução proposta: transformar frases em vértices de um grafo e ranquear as frases mais importantes.
- Restrições principais:
  - Linguagem: Python.
  - PLN obrigatório com spaCy.
  - Grafo e PageRank/TextRank implementados do zero.
  - Não usar NetworkX ou bibliotecas prontas de grafos.
  - Última atualização no GitHub até 22/06/2026.

## Slides sugeridos

### Slide 1 — Título
**Sistema de Sumarização Extrativa de Reviews da Steam com Grafos**

Texto curto:
Projeto final de Estruturas de Dados 2, com foco em grafos, PLN e estruturas de dados implementadas manualmente.

### Slide 2 — Problema
Reviews da Steam podem conter milhares de opiniões sobre gráficos, jogabilidade, desempenho, bugs e preço. Ler tudo manualmente é demorado.

### Slide 3 — Objetivo
Gerar automaticamente um resumo com as frases mais relevantes das avaliações, preservando o texto original dos usuários.

### Slide 4 — Critérios e Restrições
Destacar os critérios de maior peso:
- Implementação da solução: 3,5 pontos.
- Algoritmos em grafos: 2,0 pontos.
- Análise dos resultados: 2,0 pontos.

---

# Parte 2 — Solução Técnica, Grafos e Pipeline

## Ideia central
Explicar como o sistema transforma reviews em um grafo, calcula a importância das frases e monta o resumo final.

## O que mostrar no Canva
- Pipeline em formato de fluxo.
- Modelagem do grafo:
  - Vértice: frase ou sentença.
  - Aresta: similaridade entre frases.
  - Peso: valor da similaridade.
  - Representação principal: matriz de similaridade.
- Estruturas de dados implementadas pelo grupo:
  - Grafo.
  - Tabela Hash.
  - Max-Heap.
  - Árvore AVL ou BST.
- Algoritmos:
  - PageRank/TextRank.
  - Centralidade de grau.
  - Seleção greedy para reduzir redundância.

## Slides sugeridos

### Slide 5 — Pipeline do Sistema
Fluxo recomendado:
Dataset CSV → spaCy → frases limpas → cálculo de similaridade → grafo → PageRank → seleção final → resumo.

### Slide 6 — Modelagem do Grafo
Cada frase vira um vértice. Frases parecidas são conectadas por arestas ponderadas. Quanto maior a similaridade, mais forte a conexão.

### Slide 7 — Estruturas de Dados
Usar uma tabela com:
- Grafo: guarda conexões entre frases.
- HashMap: vocabulário e frequências.
- Max-Heap: seleciona frases de maior score.
- AVL/BST: organiza palavras-chave em ordem.

### Slide 8 — PageRank/TextRank
O PageRank calcula quais frases são mais centrais no grafo. Uma frase é importante quando está conectada a outras frases também importantes.

### Slide 9 — Resumo sem Redundância
Não basta pegar as frases com maior score. A seleção greedy evita frases muito parecidas, garantindo mais variedade no resumo.

---

# Parte 3 — Experimentos, Colaboração e Entrega Final

## Ideia central
Mostrar como o grupo vai provar que a solução funciona, dividir responsabilidades e garantir rastreabilidade no GitHub.

## O que mostrar no Canva
- Experimentos obrigatórios:
  - Taxa de compressão: 10%, 20% e 30%.
  - PageRank vs. centralidade de grau.
  - Impacto do limiar de similaridade.
- Resultados esperados:
  - Gráficos comparando densidade do grafo.
  - Exemplos de entrada e saída.
  - Análise da qualidade dos resumos.
- Divisão entre 5 integrantes.
- Fluxo de GitHub com commits atômicos e Pull Requests.
- Checklist da apresentação final.

## Slides sugeridos

### Slide 10 — Plano de Experimentos
Comparar diferentes configurações para entender como o sistema se comporta e justificar as escolhas técnicas.

### Slide 11 — Análise dos Resultados
Apresentar gráficos e comentários sobre:
- Número de arestas.
- Densidade do grafo.
- Coerência do resumo.
- Redundância entre frases selecionadas.

### Slide 12 — Divisão do Grupo
Tabela sugerida:
- Membro 1: Dados, spaCy e similaridade.
- Membro 2: Grafo e HashMap.
- Membro 3: PageRank, centralidade e seleção greedy.
- Membro 4: Max-Heap e AVL/BST.
- Membro 5: Pipeline, testes, CLI e experimentos.

### Slide 13 — GitHub e Commits Atômicos
Cada commit deve ter uma mudança pequena, testável e rastreável. O histórico precisa mostrar a contribuição individual de cada integrante.

### Slide 14 — Checklist Final
Confirmar que a apresentação inclui:
- Definição do problema.
- Modelagem do grafo.
- Algoritmos e estruturas de dados.
- Implementação.
- Entrada e saída.
- Análise dos resultados.
- Uso de LLM.
- Contribuição de cada integrante.

---

# Organização Visual Recomendada

## Padrão de cores
- Azul: problema e contexto.
- Verde: solução técnica.
- Roxo ou vinho: experimentos e entrega.

## Layout
- Usar pouco texto por slide.
- Preferir diagramas, fluxos, tabelas e ícones.
- Colocar detalhes técnicos maiores nas notas de apresentação, não no corpo do slide.
- Manter a mesma ordem visual nas três partes: título, ideia principal e evidência.

## Estrutura final no Canva
- Parte 1: 4 slides.
- Parte 2: 5 slides.
- Parte 3: 5 slides.
- Total sugerido: 14 slides.
