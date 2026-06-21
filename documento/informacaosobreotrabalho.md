# Especificação do Projeto Prático: Processamento de Linguagem Natural (PLN) baseado em Grafos

Este documento apresenta as regras, critérios de avaliação, sistemática de nota individual e as temáticas para o desenvolvimento do projeto prático.

---

## 1. Regras Gerais

1. **Temática:** Os trabalhos estão estritamente relacionados ao **Processamento de Linguagem Natural (PLN)**.
2. **Área de Aplicação:** Cada grupo poderá escolher livremente uma área de aplicação para o problema abordado (ex: área médica, educação, segurança pública, mercado financeiro, jurídico, esportes, entre outras), desde que o problema utilize **dados textuais como entrada** (frases, documentos, comentários, prontuários, notícias, avaliações, mensagens, artigos, etc.).
3. **Dados:** Os dados utilizados no projeto poderão ser reais ou fictícios. Os dados fictícios poderão ser gerados com auxílio de modelos de linguagem (**LLMs**), desde que sejam coerentes com a área de aplicação escolhida.
4. **Linguagem de Programação:** Os trabalhos deverão ser implementados utilizando obrigatoriamente as linguagens **C/C++ ou Python**.
5. **Estruturas de Dados:** O trabalho deverá envolver obrigatoriamente o uso de **Grafos** e pelo menos **uma outra estrutura de dados** em alguma etapa da solução.
6. **Análise de Resultados:** O trabalho deverá apresentar alguma análise ou interpretação dos resultados obtidos.
7. **Bibliotecas Externas:** É permitido utilizar bibliotecas externas para PLN, desde que a modelagem em grafos e os algoritmos principais sejam **implementados pelo próprio grupo**.
8. **Hospedagem e Prazo:** O código-fonte deverá estar hospedado no GitHub de pelo menos um integrante do grupo. A última atualização do repositório no GitHub deverá ocorrer até o dia **22/06/2026**.
9. **Entregáveis da Apresentação:** Além do código-fonte, cada grupo deverá entregar uma apresentação final (slides PowerPoint - sem limite de slides) contendo a seguinte estrutura:
   - Descrição do problema;
   - Modelagem do grafo;
   - Descrição da solução;
   - Implementação;
   - Exemplos de entrada e saída;
   - Análise dos resultados;
   - Um slide indicando explicitamente como uma LLM foi utilizada no desenvolvimento do trabalho.
10. **Originalidade:** Trabalhos semelhantes entre grupos não serão permitidos, mesmo que utilizem bases de dados diferentes. A falta de originalidade será um critério de penalização severo na avaliação.

---

## 2. Critérios de Avaliação

| Critério | Descrição | Pontuação |
| :--- | :--- | :---: |
| **1. Definição do Problema** | Clareza na descrição do problema de PLN, contextualização da área de aplicação e coerência dos objetivos do trabalho. | 0,5 |
| **2. Qualidade e Coerência dos Dados** | Adequação dos dados utilizados ao problema proposto. Organização e representação dos dados textuais. Coerência dos dados fictícios gerados por LLMs (se houver). | 1,0 |
| **3. Implementação da Solução** | Qualidade da implementação em C/C++ ou Python. Funcionamento correto do sistema. Organização, modularização e legibilidade do código. Uso adequado de pelo menos uma estrutura de dados adicional além do grafo com justificativa técnica. Correta definição dos vértices, arestas, pesos, relações e representação do grafo. Complexidade e adequação da modelagem ao problema. Correção e adequação dos algoritmos implementados. | 3,5 |
| **4. Algoritmos em Grafos** | Implementação dos principais algoritmos em grafos pelo próprio grupo, **sem utilização de bibliotecas prontas**. Aplicação correta ao problema proposto. | 2,0 |
| **5. Análise e Interpretação** | Capacidade de interpretar e justificar os resultados obtidos. Discussão sobre padrões, relações, agrupamentos, similaridades, métricas ou conclusões extraídas. | 2,0 |
| **6. Apresentação Final** | Clareza e organização da apresentação. Presença obrigatória dos itens solicitados: problema, modelagem, solução, implementação, exemplos de entrada/saída, análise dos resultados e indicação explícita do uso de LLM. Clara definição da contribuição de todos os integrantes do grupo. | 1,0 |
| **Total** | | **10,0** |

---

## 3. Composição da Nota Individual e Cálculo de Ajuste

A nota do trabalho será inicialmente atribuída ao grupo como um todo. Após a apresentação, cada integrante irá avaliar os outros membros informando o percentual de contribuição de cada um no desenvolvimento do trabalho. A contribuição final de um membro será a média atribuída pelos outros integrantes.

Após todas as apresentações, os professores definirão um percentual mínimo esperado de contribuição individual, denotado como o **limiar $L$**.

* **Se $C_i \ge L$**: O aluno receberá a nota integral do grupo ($N_i = N_g$).
* **Se $C_i < L$**: A penalização será aplicada e a nota individual do aluno será calculada através da fórmula matemática abaixo:

$$N_i = N_g \times \left(1 - \frac{L - C_i}{2L}\right)$$

**Onde:**
* $N_i$ = Nota individual final do aluno
* $N_g$ = Nota atribuída ao grupo
* $L$ = Limiar mínimo de contribuição definido pelos professores
* $C_i$ = Percentual de contribuição final do aluno (média das avaliações dos pares)

> ⚠️ **Nota:** A penalização só ocorre quando o aluno fica abaixo do limiar estabelecido ($C_i < L$).

---

## 4. Penalizações na Nota do Grupo

| Situação | Penalização |
| :--- | :--- |
| Trabalho sem uso de grafos | **Nota zero** |
| Trabalho sem outra estrutura de dados além do grafo | **-5,0 pontos** |
| Uso de bibliotecas prontas para algoritmos principais de grafos | **-5,0 pontos** |
| Código-fonte não disponível no GitHub | **Nota zero** |
| Última atualização do código no GitHub após 22/06/2026 | **-2,0 pontos por dia de atraso** |
| Ausência da apresentação final | **Nota zero** |
| Projeto não relacionado a PLN | **Nota zero** |
| Código não executa ou possui falhas graves | **Nota zero** |
| Trabalho similar a outro grupo (inclusive de outra turma) | **-5,0 pontos** |
| Cópia de implementação de outro grupo | **Nota zero** |

---

## 5. Temáticas dos Trabalhos

As temáticas serão definidas por sorteio em sala de aula. Para qualquer uma das temáticas, o grupo deve obrigatoriamente:
1. Definir um problema claro.
2. Definir uma solução (quais algoritmos e estruturas de dados utilizar).
3. Indicar se a solução proposta resolveu satisfatoriamente o problema.

### Temática A: Sistema de Análise Textual Baseado em Grafos
* **Dias de Apresentação:** 25/06/2026 (Turma T01) \| 26/06/2026 (Turma T03)
* **Objetivo:** Dada uma coleção de documentos, construir um grafo de coocorrência de palavras (ou frases/sentenças), onde cada vértice representa uma palavra (ou frase/sentença) e cada aresta representa a ocorrência conjunta de duas palavras no mesmo documento. Utilizar pesos nas arestas, aplicar técnicas de filtragem e identificar grupos de palavras relacionadas no grafo.

### Temática B: Sistema de Recomendação de Textos
* **Dias de Apresentação:** 30/06/2026 (Turma T01) \| 01/07/2026 (Turma T03)
* **Objetivo:** Dada uma coleção de textos e um conjunto de interações de usuários, construir um grafo bipartido usuário-texto (vértices representam usuários e documentos textuais; arestas representam interações como leitura, avaliação, interesse, compartilhamento). A partir deste grafo, gerar projeções texto-texto utilizando medidas de similaridade semântica e/ou relações de coocorrência de usuários. Utilizar pesos nas arestas, aplicar técnicas de filtragem e desenvolver mecanismos de recomendação capazes de sugerir textos relevantes para cada usuário.

### Temática C: Sistema de Sumarização Extrativa Baseado em Grafos
* **Dias de Apresentação:** 02/07/2026 (Turma T01) \| 03/07/2026 (Turma T03)
* **Objetivo:** Dado um texto ou coleção de textos, representar frases como vértices e conectar frases semanticamente relacionadas por meio de arestas ponderadas. Utilizar medidas de similaridade textual para a construção do grafo e aplicar algoritmos de ranqueamento, centralidade ou análise estrutural para identificar as frases mais relevantes. O sistema deverá gerar automaticamente resumos compostos por frases extraídas do texto original.

### Temática D: Sistema de Detecção de Tópicos (Comunidades)
* **Dias de Apresentação:** 07/07/2026 (Turma T01) \| 08/07/2026 (Turma T03)
* **Objetivo:** Dada uma coleção de textos, construir uma representação relacional envolvendo palavras, frases e/ou documentos. As arestas deverão representar relações de similaridade, coocorrência ou associação semântica. Aplique técnicas de filtragem e algoritmos de detecção de comunidades para identificar grupos semanticamente relacionados, interpretando cada grupo como um tópico presente na coleção textual.

### Temática E: Sistema de Classificação Textual Baseado em Grafos
* **Dias de Apresentação:** 09/07/2026 (Turma T01) \| 10/07/2026 (Turma T03)
* **Objetivo:** Modelar relações semânticas, estruturais ou estatísticas entre textos, palavras e categorias, utilizando medidas de similaridade, frequência ou coocorrência. A partir dessa representação, o sistema deverá inferir automaticamente a categoria de novos textos por meio de algoritmos de propagação, ranqueamento, vizinhança ou análise estrutural do grafo.