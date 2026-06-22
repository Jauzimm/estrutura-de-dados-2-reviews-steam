# Sumarizador de Avaliações da Steam

## Introdução

Somos o Grupo 11 da disciplina Estruturas de Dados 2 (EDA2), na Universidade de Brasília - Gama (FGA/UnB). Este repositório tem como propósito documentar o projeto de sumarização extrativa de avaliações de jogos da Steam, que consiste na utilização de grafos para extrair informações relevantes de um conjunto de avaliações de jogos da Steam, identificando as opiniões mais relevantes de forma concisa e sem redundâncias.

## Sobre o projeto

O projeto consiste em um sistema capaz de ler grandes volumes de avaliações de jogos da Steam (a partir de uma base de dados em formato CSV) e gerar resumos automáticos compostos pelas frases originais mais representativas (sumarização extrativa).

Link do dataset utilizado: [Steam Review](https://www.kaggle.com/datasets/kieranpoc/steam-reviews/data)

## Como Rodar o Projeto

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu-usuario/estrutura-de-dados-2-reviews-steam.git
   cd estrutura-de-dados-2-reviews-steam
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Instale as dependências**

   ```bash
   python -m pip install -r Backend/requirements.txt
   ```

4. **Baixe o modelo de língua portuguesa do spaCy**

   ```bash
   python -m spacy download pt_core_news_md
   ```

5. **Execute o pipeline principal**

   ```bash
   cd Backend
   python main.py
   ```

O script irá:

- Ler o dataset original (`Dataset/dataset_steamreview_ptbr.csv`)
- Limpar e filtrar as reviews (remoção de arte ASCII, templates de avaliação, símbolos excessivos, etc.)
- Salvar o dataset limpo em `Backend/results/dataset_steamreview_limpo.csv`
- Processar as reviews com spaCy para obter vetores semânticos
- Construir a matriz de similaridade e executar o PageRank
- Selecionar reviews representativas distintas e salvar o resultado em JSON

Observação: é necessário baixar o modelo de língua portuguesa do spaCy antes de executar:

```bash
python -m spacy download pt_core_news_md
```

## Organização do Projeto

O repositório está dividido nas seguintes pastas:

### Backend

Responsável pela implementação e processamento principal do projeto.

Atualmente, o código está modularizado da seguinte forma:

- `processamento_dados.py` → funções de limpeza e filtragem das reviews (detecção de arte ASCII, templates de avaliação, símbolos excessivos).
- `processamento_nlp.py` → processamento com spaCy para gerar vetores de palavras de cada review.
- `grafo_pagerank.py` → construção da matriz de similaridade e aplicação do PageRank sobre as reviews.
- `selecao_reviews.py` → seleção das melhores reviews distintas e exportação para JSON.
- `main.py` → orquestrador que chama as etapas de tratamento, vetorização, PageRank e seleção.
- `results/` → diretório onde os arquivos de saída (dataset limpo, reviews resumidas) são armazenados.

### Dataset

Contém os dados utilizados nos experimentos e avaliações.

### Materials

Reúne materiais de apoio, referências e outros arquivos relevantes para o desenvolvimento do trabalho.

### Slides

Contém as apresentações e slides produzidos sobre o projeto.


## Colaboradores

<font size="3"><p style="text-align: left">**Tabela 1** - Colaboradores.</p></font>

| <img src="https://github.com/Jauzimm.png" width="150px" > | <img src="https://github.com/Antedeguemon21.png" width="150px"> | <img src="https://github.com/KarolineLuz.png" width="150px"> | <img src="https://github.com/Marcelo-Adrian.png" width="150px"> | <img src="https://github.com/navicg.png" width="150px"> |
| :-------------------------------------------------------: | :------------------------------------------------------------: | :----------------------------------------------------------: | :-------------------------------------------------------------: | :----------------------------------------------------: |
|      [João Vitor Santos de Oliveira](https://github.com/Jauzimm)      |          [Leonardo Rodrigues](https://github.com/Antedeguemon21)    |   [Karoline Luz da Conceição](https://github.com/KarolineLuz) |       [Marcelo Adrian](https://github.com/Marcelo-Adrian)       |          [Ana Victória](https://github.com/navicg)             |
