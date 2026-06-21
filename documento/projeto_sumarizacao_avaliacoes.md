# Projeto: Sistema de Sumarização Extrativa de Avaliações de Produtos

## 1. Problema

Quando um produto possui muitas avaliações, o usuário dificilmente consegue ler tudo.

Exemplo:

Um celular possui 2.000 avaliações.

Algumas falam sobre:

- bateria
- câmera
- desempenho
- tela
- preço

O objetivo é gerar automaticamente um resumo contendo as informações mais relevantes das avaliações.

---

## Exemplo

### Entrada

```text
A bateria dura o dia inteiro.

Gostei muito da autonomia da bateria.

A câmera é razoável durante o dia.

A câmera tem desempenho ruim à noite.

O celular é muito rápido para jogos.

A bateria é excelente para uso intenso.
```

### Saída

```text
A bateria dura o dia inteiro.
A bateria é excelente para uso intenso.
A câmera tem desempenho ruim à noite.
O celular é muito rápido para jogos.
```

Observe que o sistema extrai frases originais (sumarização extrativa).

---

# 2. Modelagem do Grafo

## Vértices

Cada avaliação ou sentença será um vértice.

Exemplo:

```text
V1 = "A bateria dura o dia inteiro"

V2 = "Gostei muito da autonomia da bateria"

V3 = "A câmera é razoável durante o dia"

V4 = "A câmera tem desempenho ruim à noite"

V5 = "O celular é muito rápido para jogos"
```

---

## Arestas

Conectam frases semanticamente parecidas.

Por exemplo:

```text
V1 ↔ V2
```

porque ambas falam sobre bateria.

---

## Pesos

Peso = similaridade textual.

Exemplo:

```text
sim(V1,V2) = 0.82

sim(V1,V3) = 0.15

sim(V3,V4) = 0.73
```

Quanto maior o peso, mais semelhantes são as frases.

---

# 3. Como calcular a similaridade

Uma abordagem simples:

## Pré-processamento

Transformar:

```text
"A bateria dura o dia inteiro"
```

em

```text
["bateria","dura","dia","inteiro"]
```

Remover:

- pontuação
- stopwords
- palavras muito comuns

---

## Vetorização TF-IDF

Transformar cada frase em vetor.

| Palavra | Frase 1 | Frase 2 |
|----------|----------|----------|
| bateria | 0.8 | 0.7 |
| dura | 0.4 | 0 |
| autonomia | 0 | 0.6 |

---

## Similaridade de Cosseno

Calcular:

```text
cos(v1,v2)
```

Resultado:

```text
0 = totalmente diferentes

1 = idênticas
```

---

# 4. Algoritmo Principal

## TextRank

É uma adaptação do PageRank.

A ideia:

- frases importantes recebem conexões de muitas frases importantes
- frases centrais recebem maior pontuação

Vocês podem implementar o PageRank manualmente.

Isso atende o requisito:

> algoritmos principais implementados pelo grupo

---

## Fórmula

```text
PR(v_i)=((1-d)/N)+d*Σ(PR(v_j)/Out(v_j))
```

Onde:

- d = fator de amortecimento
- N = número de vértices

---

# 5. Estrutura de Dados Adicional

Além do grafo.

## Heap (Priority Queue)

Após calcular o ranking:

```python
[
 ("frase1",0.87),
 ("frase2",0.95),
 ("frase3",0.44)
]
```

A heap permite obter rapidamente as k melhores frases.

---

## HashMap

Para:

- TF
- IDF
- vocabulário

Exemplo:

```python
{
 "bateria": 25,
 "camera": 18,
 "jogos": 12
}
```

---

# 6. Diferencial Interessante

Em vez de apenas resumir, o sistema pode identificar:

## Principais tópicos

Exemplo:

```text
Bateria → 45%

Câmera → 30%

Desempenho → 15%

Tela → 10%
```

---

## Como fazer

Criar um segundo grafo:

### Grafo bipartido

Um lado:

```text
Frases
```

Outro lado:

```text
Palavras-chave
```

Exemplo:

```text
Frase1 ─ bateria
Frase1 ─ autonomia
Frase2 ─ bateria
Frase3 ─ câmera
```

A partir disso vocês podem calcular:

- palavras mais centrais
- temas dominantes

Isso impressiona bastante na apresentação.

---

# 7. Análise de Resultados

Essa parte vale 2 pontos e muita gente faz mal.

Vocês podem testar:

## Teste 1

50 avaliações

Resumo de:

- 10%
- 20%
- 30%

Comparar qualidade.

---

## Teste 2

PageRank vs Grau

Comparar:

```text
Método A: PageRank

Método B: Centralidade de Grau
```

Ver qual produz melhores resumos.

---

## Teste 3

Impacto do limiar

Criar aresta somente se:

```text
similaridade > 0.3
```

Depois:

```text
similaridade > 0.5
```

Analisar:

- número de arestas
- densidade do grafo
- qualidade do resumo

---

# Possível divisão dos integrantes

### Pessoa 1

Pré-processamento NLP

### Pessoa 2

Construção do grafo

### Pessoa 3

PageRank/TextRank

### Pessoa 4

Interface e análise

---

# Diferencial Final

Separar avaliações positivas e negativas antes da sumarização.

Assim o sistema gera dois resumos:

## Pontos positivos

- Bateria possui ótima duração.
- Desempenho é adequado para jogos.

## Pontos negativos

- Câmera apresenta problemas em ambientes escuros.
- Tela possui brilho insuficiente em áreas externas.

Isso deixa o projeto mais próximo de um sistema real usado por e-commerces e ainda mantém a modelagem em grafos relativamente simples.
