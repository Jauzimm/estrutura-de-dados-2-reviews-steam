# Prompt Melhorado — Plano de Trabalho para Sistema de Sumarização Extrativa

> **Instruções de Uso:** Copie todo o conteúdo abaixo e cole em uma conversa com uma IA (ChatGPT, Gemini, Claude, etc.) para obter o plano de trabalho completo.

---

Você é um Engenheiro de Software Sênior e Especialista em Estruturas de Dados e Processamento de Linguagem Natural (PLN). 

Com base nas especificações detalhadas abaixo, elabore um **Plano de Trabalho Completo, Arquitetura do Sistema e Divisão de Tarefas** para um grupo de **5 pessoas** desenvolver um **Sistema de Sumarização Extrativa de Avaliações de Jogos da Steam baseado em Grafos**. 

---

## 1. CONTEXTO ACADÊMICO

Este é o projeto final da disciplina de **Estruturas de Dados 2 (EDA2)**. A temática sorteada para o grupo é a **Temática C: Sistema de Sumarização Extrativa Baseado em Grafos**. A apresentação será em **02/07/2026 (Turma T01) ou 03/07/2026 (Turma T03)**. O código-fonte no GitHub deve ter sua **última atualização até 22/06/2026** — atrasos custam **-2,0 pontos por dia**.

### Critérios de Avaliação (Total: 10,0 pontos)
| Critério | Pontuação |
|---|:---:|
| Definição do Problema | 0,5 |
| Qualidade e Coerência dos Dados | 1,0 |
| Implementação da Solução (modularização, estruturas de dados, modelagem do grafo) | 3,5 |
| Algoritmos em Grafos (implementados pelo grupo, SEM bibliotecas prontas) | 2,0 |
| Análise e Interpretação dos Resultados | 2,0 |
| Apresentação Final (slides com todos os itens obrigatórios) | 1,0 |

### Penalizações Críticas
- **Nota ZERO:** Sem grafos, sem GitHub, sem apresentação, sem PLN, código não executa, cópia.
- **-5,0 pontos:** Sem outra estrutura de dados além do grafo; uso de bibliotecas prontas para algoritmos de grafos (como NetworkX).
- **-2,0 pontos/dia:** Atraso no GitHub após 22/06/2026.

### Nota Individual
Cada integrante avalia os demais atribuindo percentual de contribuição. Se a contribuição $C_i$ ficar abaixo do limiar $L$ definido pelos professores: $N_i = N_g \times (1 - \frac{L - C_i}{2L})$.

---

## 2. OBJETIVOS E REQUISITOS DO PROJETO

- **Objetivo:** Dado um conjunto de reviews de jogos da Steam (dataset `steam_reviews.csv`, ~120MB de dados reais), representar frases como vértices de um grafo, conectar frases semanticamente relacionadas por arestas ponderadas, e aplicar algoritmos de ranqueamento para extrair automaticamente as frases mais relevantes como resumo do que os jogadores estão falando.
- **Linguagem:** Python.
- **Restrição Fundamental (Grafos):** É estritamente **PROIBIDO** utilizar bibliotecas prontas de grafos (como `NetworkX`). A estrutura do Grafo e o algoritmo PageRank/TextRank devem ser implementados do zero pelo grupo.
- **Processamento de Texto (PLN):** Deve ser utilizada obrigatoriamente a biblioteca **spaCy** para tokenização, remoção de stopwords, lematização e segmentação de sentenças. Outras bibliotecas de NLP (como NLTK) são permitidas como complemento.
- **Representação do Grafo:** Utilizar **Matriz de Similaridade** como representação principal (conforme orientação do professor), pois facilita a visualização das relações entre frases e a aplicação do PageRank.
- **Limiares de Similaridade:** Inicialmente aplicar um limiar mais alto e reduzi-lo gradualmente para testar diferentes configurações (conforme orientação do professor).

---

## 3. ARQUITETURA DO SISTEMA E ESTRUTURAS DE DADOS CUSTOMIZADAS

Projete a implementação manual em Python das seguintes estruturas de dados e algoritmos. **Todas devem ser implementadas do zero pelo grupo**, sem usar implementações prontas do Python (exceto para NLP com spaCy). Explique como cada uma se conecta no pipeline de execução:

### 3.1. Estrutura de Grafo (Implementação Própria)
- Representado por **Matriz de Similaridade** (para armazenar as pontuações de similaridade entre as sentenças) e opcionalmente **Lista de Adjacência** para otimizar operações esparsas.
- Cada **vértice** = uma sentença/review.
- Cada **aresta** = conexão entre sentenças com similaridade acima do limiar, com **peso** = valor da similaridade calculada (ex: similaridade de cosseno entre os vetores de palavras do spaCy, ou proporção de palavras em comum).

### 3.2. Algoritmo PageRank/TextRank (Implementação Própria)
- Implementação iterativa da fórmula de PageRank Ponderado:
  ```
  PR(vi) = (1-d)/N + d × Σ(j∈vizinhos(i)) [ PR(vj) × w(j,i) / Σ(k∈vizinhos(j)) w(j,k) ]
  ```
- Fator de amortecimento: $d = 0.85$.
- Convergência: diferença máxima entre iterações < $10^{-6}$ ou máximo de 100 iterações.
- O professor enfatizou: "Estudem o PageRank. Vocês NÃO podem usar biblioteca pronta."

### 3.3. Fila de Prioridade / Max-Heap (Implementação Própria)
- Recebe os scores das sentenças pós-PageRank.
- Extrai de forma eficiente ($O(k \log n)$) as $k$ sentenças mais relevantes.
- Cada elemento: tupla `(score, índice_original, texto_da_sentença)`.

### 3.4. Tabela Hash / HashMap (Implementação Própria)
- Para armazenar o vocabulário único de palavras e suas frequências nas sentenças.
- Mapeamento eficiente de termos para índices e contagens.
- Controle de palavras-chave e verificação rápida de pertencimento.
- Inserção e busca em $O(1)$ amortizado.

### 3.5. Árvore Binária de Busca (AVL ou BST) (Implementação Própria)
- Indexação ordenada do vocabulário de palavras-chave.
- Permite listar termos mais frequentes em ordem (percurso em-ordem).
- Operações em $O(\log n)$.

---

## 4. PIPELINE DE EXECUÇÃO COMPLETO

O pipeline deve seguir estas etapas, em ordem:

### Etapa 1 — Ingestão de Dados
Ler o dataset `steam_reviews.csv`, filtrar reviews por jogo específico, extrair as colunas de texto relevantes.

### Etapa 2 — Pré-processamento (spaCy)
Segmentar reviews em sentenças usando spaCy, remover stopwords, lematizar termos, remover sentenças muito curtas (< 5 palavras) e duplicatas.

### Etapa 3 — Cálculo de Similaridade
Utilizar os **vetores de palavras (word vectors) do spaCy** para representar cada sentença como um vetor e calcular a similaridade entre pares de sentenças (ex: similaridade de cosseno nativa do spaCy via `doc.similarity()`). Alternativamente, calcular a similaridade pela proporção de palavras-chave em comum (usando a Tabela Hash para busca eficiente).

### Etapa 4 — Criação do Grafo
Construir a Matriz de Similaridade com os valores calculados na etapa anterior. Aplicar limiar mínimo para criar arestas — somente pares com similaridade acima do limiar geram aresta no grafo (iniciar com limiar alto e testar decrescendo).

### Etapa 5 — Ranqueamento (PageRank/TextRank)
Executar o PageRank customizado sobre o grafo para obter o score de importância de cada sentença.

### Etapa 6 — Seleção Inteligente (Greedy Diversificado)
O professor enfatizou que **não basta pegar as frases de maior score** — se as 3 melhores falam de "gráficos", o resumo fica repetitivo. A solução:
1. Inserir todas as sentenças com seus scores na Max-Heap.
2. Extrair a sentença de maior score.
3. Para cada próxima candidata extraída da Heap:
   - Se a similaridade dela com **todas** as frases já selecionadas for menor que um limite de redundância → **aceitar**.
   - Caso contrário → **descartar** e pegar a próxima.
4. Repetir até atingir $k$ sentenças no resumo.

### Etapa 7 — Saída
Exibir o resumo final com as sentenças selecionadas na ordem original de aparição.

---

## 5. PLANO DE ANÁLISE DE RESULTADOS (VALOR: 2,0 PONTOS)

O professor alertou que "essa parte vale 2 pontos e muita gente faz mal." O sistema deve expor parâmetros configuráveis para experimentos documentados:

### Experimento 1 — Taxa de Compressão
Gerar resumos variando a quantidade de sentenças extraídas: **10%, 20% e 30%** do total. Comparar a qualidade e cobertura temática dos resumos.

### Experimento 2 — PageRank vs. Centralidade de Grau
Comparar a qualidade das sentenças selecionadas usando:
- **Método A:** Score do PageRank (algoritmo iterativo sofisticado).
- **Método B:** Centralidade de Grau simples (soma dos pesos das arestas de cada vértice).
Avaliar qual produz resumos mais representativos.

### Experimento 3 — Impacto do Limiar de Similaridade
Testar limiares de similaridade decrescentes (ex: 0.5 → 0.3 → 0.15 → 0.10). Analisar:
- Número de arestas criadas em cada caso.
- Densidade do grafo.
- Qualidade e coerência do resumo gerado.
- Determinar o limiar ideal que equilibra cobertura e relevância.

### Diferencial Opcional — Separação Positivo/Negativo
Separar reviews positivas e negativas antes da sumarização, gerando **dois resumos independentes**: "Pontos Positivos" e "Pontos Negativos" — simulando um sistema real de e-commerce.

### Diferencial Opcional — Detecção de Tópicos
Criar um grafo bipartido (frases ↔ palavras-chave) para identificar automaticamente os tópicos dominantes nas reviews (ex: Bateria → 45%, Câmera → 30%).

---

## 6. PRINCÍPIO DE MODIFICAÇÕES ATÔMICAS

Todo o desenvolvimento deve seguir rigorosamente o princípio de **modificações atômicas**, para que cada integrante possa acompanhar a evolução do código e compreender exatamente o que cada mudança faz:

### Regras de Commits Atômicos:
- Cada commit deve realizar **UMA ÚNICA modificação lógica e testável** (ex: criar a classe `MaxHeap` com operações básicas; adicionar a função `cosseno_similaridade`; integrar o spaCy para tokenização).
- Commits gigantes do tipo "projeto finalizado", "várias correções" ou "update" são **PROIBIDOS**.
- Cada commit deve ser **compilável e testável** isoladamente — nunca "quebrar" o código.

### Padrão de Mensagens (Conventional Commits):
```
feat(módulo): descrição curta do que foi adicionado
fix(módulo): descrição da correção
test(módulo): descrição do teste adicionado
refactor(módulo): descrição da refatoração
docs(módulo): descrição da documentação adicionada
```

**Exemplos concretos:**
```
feat(heap): implementa classe MaxHeap com insert e extract_max
feat(heap): adiciona metodo heapify_up para balanceamento
test(heap): adiciona testes unitarios para insert e extract_max
feat(grafo): implementa classe Grafo com matriz de similaridade
feat(grafo): adiciona metodo adicionar_aresta com limiar minimo
feat(hash): implementa tabela hash customizada com insert e search
feat(similaridade): implementa calculo de similaridade usando spacy word vectors
feat(pagerank): implementa iteracao basica do algoritmo com damping 0.85
fix(pagerank): corrige divisao por zero quando vertice nao tem vizinhos
feat(nlp): integra spacy para tokenizacao e remocao de stopwords
feat(pipeline): conecta modulo nlp ao modulo de similaridade
feat(selecao): implementa greedy diversificado para evitar redundancia
test(pipeline): adiciona teste end-to-end com 10 reviews de exemplo
docs(readme): adiciona instrucoes de instalacao e execucao
feat(analise): implementa experimento de variacao de limiar de similaridade
```

---

## 7. PLANO DE COLABORAÇÃO E FLUXO DO GITHUB (5 INTEGRANTES)

Como a avaliação individual é baseada na contribuição de cada membro (avaliação por pares com limiar $L$), o desenvolvimento precisa de **rastreabilidade inequívoca** — cada pessoa precisa ter commits significativos e visíveis no histórico.

### Divisão de Papéis (Componentes Modulares):

| Membro | Papel | Responsabilidades Principais | Estruturas de Dados |
|:---:|---|---|---|
| **1** | Engenheiro de Dados e NLP | Ler `steam_reviews.csv`, integrar spaCy, pré-processamento de texto, cálculo de similaridade entre sentenças | **Similaridade** e **NLP** |
| **2** | Engenheiro de Estruturas Core | Implementar Grafo (matriz de similaridade + lista adjacência), Tabela Hash | **Grafo** e **Tabela Hash** |
| **3** | Engenheiro de Algoritmos | Implementar PageRank/TextRank, Greedy Diversificado, Centralidade de Grau | **PageRank** e **Seleção** |
| **4** | Engenheiro de Otimização | Implementar Max-Heap, Árvore AVL | **Max-Heap** e **Árvore AVL** |
| **5** | Engenheiro de Integração | Pipeline central, CLI, experimentos (1, 2 e 3), análise de resultados | **Pipeline** e **Testes** |

### Fluxo de Trabalho Git (Git Flow Simplificado):
1. Branch `main` protegida — nunca commitar diretamente.
2. Cada funcionalidade em branch específica: `feature/custom-heap`, `feature/spacy-nlp`, `feature/pagerank`, etc.
3. Para integrar na `main`: abrir **Pull Request (PR)** descrevendo o que foi feito.
4. PR deve ser **revisado e aprovado por pelo menos 1 outro integrante** antes do merge.
5. Isso garante que o histórico do repositório mostra colaboração ativa de todos.

### Ordem de Desenvolvimento (Dependências):
```
Fase 1 (Paralela — Todos ao mesmo tempo):
  Membro 1: Leitura CSV + spaCy          Membro 4: MaxHeap + AVL
  Membro 2: Grafo + Hash                 Membro 3: PageRank (lógica)
  Membro 5: Estrutura de diretórios + testes base

Fase 2 (Integração — Sequencial):
  Membro 1 entrega frases pré-processadas + similaridades → Membro 2 constrói grafo
  Membro 2 entrega grafo → Membro 3 roda PageRank
  Membro 3 entrega scores → Membro 4 usa na Heap

Fase 3 (Pipeline Final):
  Membro 5 conecta tudo e roda experimentos
  Todos revisam e ajudam na documentação
```

---

## 8. ENTREGÁVEIS DA APRESENTAÇÃO (Checklist)

A apresentação final (PowerPoint, sem limite de slides) deve conter obrigatoriamente:
- [ ] Descrição do problema
- [ ] Modelagem do grafo (vértices, arestas, pesos, representação)
- [ ] Descrição da solução (algoritmos e estruturas de dados usados, com justificativa)
- [ ] Implementação (trechos de código relevantes, diagramas de classes)
- [ ] Exemplos de entrada e saída
- [ ] Análise dos resultados (Experimentos 1, 2 e 3 com gráficos)
- [ ] Slide explícito indicando como uma LLM foi utilizada no desenvolvimento
- [ ] Slide indicando a contribuição de cada integrante

---

**Com base em TODAS estas especificações, estruture a resposta gerando:**

1. **Cronograma de desenvolvimento acelerado** passo a passo, dia a dia, até a data limite do repositório (22/06/2026), considerando que hoje o desenvolvimento está começando.
2. **Estrutura de diretórios do projeto** com a organização dos módulos Python.
3. **Especificação dos esqueletos (interfaces) das classes Python** que serão implementadas por cada integrante, com docstrings, type hints e métodos definidos.
4. **Sequência completa de commits atômicos** esperados de cada membro, na ordem cronológica, mostrando a evolução incremental do repositório.
5. **Contratos de integração** entre os módulos (quais métodos o Membro X precisa que o Membro Y implemente para poder trabalhar).
