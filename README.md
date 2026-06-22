# Sumarizador de Avaliações da Steam

## Introdução

Somos o Grupo 11 da disciplina Estruturas de Dados 2 (EDA2), na Universidade de Brasília - Gama (FGA/UnB). Este repositório tem como propósito documentar o projeto de sumarização extrativa de avaliações de jogos da Steam, que consiste na utilização de grafos para extrair informações relevantes de um conjunto de avaliações de jogos da Steam, identificando as opiniões mais relevantes de forma concisa e sem redundâncias.

## Sobre o projeto

O projeto consiste em um sistema capaz de ler grandes volumes de avaliações de jogos da Steam (a partir de uma base de dados em formato CSV) e gerar resumos automáticos compostos pelas frases originais mais representativas (sumarização extrativa).

Link do dataset utilizado: [Steam Review](https://www.kaggle.com/datasets/kieranpoc/steam-reviews/data)

## Como Rodar o Projeto

Primeiro, realize a configuração base:

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

---

### Backend

O backend realiza a leitura da base em CSV, pré-processa os textos, calcula vetores com spaCy e aplica o PageRank para gerar o JSON com os resumos das reviews.

1. **Instale as dependências**

   ```bash
   python -m pip install -r Backend/requirements.txt
   ```

2. **Baixe o modelo de língua portuguesa do spaCy**

   ```bash
   python -m spacy download pt_core_news_md
   ```

3. **Execute o pipeline principal**

   ```bash
   cd Backend
   python main.py
   ```

   O script irá ler, processar os dados e salvar as melhores reviews no formato JSON em `Backend/results/reviews_resumidas.json`.

---

### Frontend 

O frontend oferece uma interface simplificada para buscar os jogos e ler as reviews selecionadas.

1. **Instale as dependências do Flask**

   ```bash
   cd ../Frontend
   python -m pip install -r requirements.txt
   ```

2. **Inicie o servidor de desenvolvimento**

   ```bash
   python app.py
   ```

3. **Acesse no navegador**

   Abra o endereço [http://127.0.0.1:5000](http://127.0.0.1:5000). Observe que o endereço e a porta podem variar. Verifique o endereço no seu terminal.


## Organização do Projeto

O repositório está organizado de forma a separar a lógica de análise de dados da interface visual:

### Backend

Responsável pela implementação e processamento principal do projeto.

- `processamento_dados.py`: Funções de limpeza e filtragem das reviews (remoção de ruídos).
- `processamento_nlp.py`: Processamento com spaCy para gerar vetores de palavras de cada review.
- `grafo_pagerank.py`: Construção do grafo de similaridade e aplicação do PageRank.
- `selecao_reviews.py`: Seleção das melhores reviews distintas.
- `main.py`: Orquestrador principal do pipeline.
- `results/`: Diretório contendo as saídas processadas, inclusive `reviews_resumidas.json`.

### Frontend

Interface com autocomplete e visualização de resumos.

- `Frontend/app.py`: Servidor Flask que serve a interface e os endpoints de API.
- `Frontend/templates/index.html`: Template HTML com o buscador e visualizador de reviews.
- `Frontend/static/style.css`: Folha de estilos contendo o tema escuro.
- `Frontend/static/script.js`: Comportamento dinâmico do autocomplete, suporte a navegação por teclado e busca assíncrona.
- `Frontend/requirements.txt`: Dependências do frontend (Flask).

---

### Outras Pastas

- **Dataset**: Contém os dados originais utilizados.
- **Materials**: Reúne materiais de apoio, referências e outros arquivos auxiliares do grupo.
- **Slides**: Contém as apresentações e slides produzidos sobre o projeto.


## Colaboradores

<font size="3"><p style="text-align: left">**Tabela 1** - Colaboradores.</p></font>

| <img src="https://github.com/Jauzimm.png" width="150px" > | <img src="https://github.com/Antedeguemon21.png" width="150px"> | <img src="https://github.com/KarolineLuz.png" width="150px"> | <img src="https://github.com/Marcelo-Adrian.png" width="150px"> | <img src="https://github.com/navicg.png" width="150px"> |
| :-------------------------------------------------------: | :------------------------------------------------------------: | :----------------------------------------------------------: | :-------------------------------------------------------------: | :----------------------------------------------------: |
|      [João Vitor Santos de Oliveira](https://github.com/Jauzimm)      |          [Leonardo Rodrigues](https://github.com/Antedeguemon21)    |   [Karoline Luz da Conceição](https://github.com/KarolineLuz) |       [Marcelo Adrian](https://github.com/Marcelo-Adrian)       |          [Ana Victória](https://github.com/navicg)             |
