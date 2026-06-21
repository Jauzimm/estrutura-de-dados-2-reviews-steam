Pessoal,

as informações do trabalho foram disponibilizadas no Aprender-3.
Na próxima aula (dia 10/06) vou conversar com cada grupo individualmente. As informações que desejo saber são:
1) qual será a área de aplicação do seu trabalho?
2)  qual problema você deseja resolver? 
3) qual vai ser o input (dados de entrada)? Dados reais ou fictícios?
4) como você está pensando na modelagem do grafo?
5) qual outra estrutura de dados, além de grafos, você está pensando em utilizar?

---

# Propostas de Resposta — Temática C: Sistema de Sumarização Extrativa Baseado em Grafos

Abaixo, apresentamos **5 opções de áreas de aplicação** detalhadas para responder às perguntas do professor. O grupo poderá escolher a que achar mais interessante ou apresentar as alternativas na reunião.

> 💡 **Lembrete:** A Temática C exige que o sistema represente frases como vértices, conecte-as por similaridade semântica via arestas ponderadas e aplique algoritmos de ranqueamento/centralidade para extrair as frases mais relevantes como resumo.

---

## 📂 Opção 1: Área Jurídica (Sumarização de Acórdãos e Processos)

### 1) Qual será a área de aplicação do trabalho?

A área de aplicação é o **Direito e o Setor Jurídico brasileiro**. O foco está na leitura automatizada de documentos judiciais, especificamente acórdãos (decisões colegiadas de tribunais) e petições. É uma área com alta demanda por ferramentas de PLN porque os documentos jurídicos costumam ter dezenas ou centenas de páginas, escritas em linguagem técnica e formal. Profissionais do Direito — advogados, juízes, assessores e estagiários — gastam grande parte do tempo apenas lendo e identificando os trechos realmente relevantes desses documentos.

### 2) Qual problema você deseja resolver?

O problema concreto é: **dado um acórdão ou petição judicial de grande extensão, gerar automaticamente um resumo contendo apenas as frases mais importantes do documento original** (os fundamentos jurídicos centrais, a decisão tomada e os argumentos-chave).

Por exemplo, um acórdão do STJ sobre responsabilidade civil pode ter 40 páginas. O sistema extrairia automaticamente as 5 a 10 frases que capturam: (a) qual era a questão discutida, (b) quais artigos de lei foram invocados, (c) qual foi a decisão final. Isso economiza tempo de leitura e permite que o profissional avalie rapidamente se o documento é relevante para o seu caso antes de lê-lo integralmente.

### 3) Qual vai ser o input (dados de entrada)? Dados reais ou fictícios?

**Dados reais.** Utilizaremos acórdãos públicos disponibilizados nos portais de jurisprudência dos tribunais brasileiros (STF, STJ e Tribunais de Justiça estaduais). Esses documentos são de acesso público e podem ser baixados diretamente em formato PDF ou texto. A entrada do sistema seria o texto do acórdão, fornecido como arquivo PDF que seria convertido para texto puro pelo programa.

Caso necessário para complementar os testes, poderemos gerar documentos jurídicos fictícios com auxílio de LLM, seguindo o padrão de redação jurídica brasileiro (com ementa, relatório, voto e dispositivo), garantindo coerência com a área.

### 4) Como você está pensando na modelagem do grafo?

A modelagem segue diretamente o que a Temática C pede:

- **Vértices:** Cada vértice do grafo representa **uma frase/sentença** do documento jurídico. Fazemos a segmentação do texto em sentenças usando técnicas de tokenização (por exemplo, com a biblioteca NLTK para Python).
- **Arestas:** Conectamos duas sentenças (dois vértices) **somente quando a similaridade semântica entre elas supera um limiar mínimo** (por exemplo, similaridade de cosseno ≥ 0,10 ou 0,15). Se a similaridade for abaixo do limiar, não criamos aresta — isso funciona como uma técnica de filtragem que mantém o grafo esparso e com conexões significativas.
- **Pesos das arestas:** O peso de cada aresta é o **valor da similaridade de cosseno** calculada entre os vetores TF-IDF das duas sentenças. Quanto maior o peso, mais semanticamente próximas são as duas frases.
- **Representação:** Usamos **lista de adjacência** (dicionário em Python) — é mais eficiente em memória do que matriz de adjacência, especialmente porque o grafo tende a ser esparso.
- **Algoritmo de grafo principal:** Implementamos o algoritmo **TextRank** (uma variação do PageRank do Google adaptada para texto), **manualmente, sem bibliotecas prontas**. O TextRank é um algoritmo iterativo que propaga "votos de importância" entre os vértices do grafo: uma sentença que está conectada a muitas outras sentenças importantes recebe um score maior. Após a convergência, as sentenças com maior score são as mais centrais e informativas do documento — e são extraídas para o resumo.

### 5) Qual outra estrutura de dados, além de grafos, você está pensando em utilizar?

Utilizaremos **duas estruturas adicionais** (o trabalho exige pelo menos uma):

1. **Fila de Prioridade (Max-Heap):** Implementada manualmente. Depois que o TextRank calcula os scores de importância de todas as sentenças, precisamos selecionar as *k* melhores de forma eficiente. O Max-Heap permite inserir todas as sentenças com seus scores e depois extrair as *k* mais relevantes em tempo $O(k \log n)$, em vez de ordenar toda a lista em $O(n \log n)$.

2. **Tabela Hash (Dicionário):** Usada para indexar o vocabulário de termos únicos do documento e contar as frequências necessárias para o cálculo do TF-IDF. A busca e inserção em tempo $O(1)$ amortizado torna essa etapa de pré-processamento muito eficiente.

**Justificativa técnica:** O Heap é essencial porque em documentos jurídicos longos podemos ter centenas de sentenças (vértices), e queremos apenas as top-*k* sem precisar ordenar tudo. A Tabela Hash é essencial para o cálculo eficiente do TF-IDF, que alimenta os pesos do grafo.

---

## 📂 Opção 2: Área de Notícias e Jornalismo (Sumarização Multi-Documento)

### 1) Qual será a área de aplicação do trabalho?

A área de aplicação é **Jornalismo, Comunicação e Mídia digital**. O foco está na síntese automática de múltiplas matérias jornalísticas que cobrem um mesmo evento ou assunto. Atualmente, quando ocorre um grande acontecimento (eleições, desastres, crises econômicas, eventos esportivos), dezenas de veículos de mídia publicam notícias simultaneamente, muitas vezes com informações repetidas e apenas com pequenas diferenças de enfoque. O leitor não tem tempo de ler todas.

### 2) Qual problema você deseja resolver?

O problema é: **dadas múltiplas notícias de diferentes veículos sobre o mesmo assunto, gerar um resumo único e conciso que consolide as informações mais importantes sem repetição.**

Por exemplo, após uma sessão de votação no Congresso, G1, Folha, UOL e Estadão publicam notícias. Cada uma destaca aspectos ligeiramente diferentes (placar, reações, próximos passos). O sistema leria todas essas matérias, identificaria quais frases são as mais informativas e representativas dos sub-tópicos do evento, e geraria um resumo que cobre todos os ângulos sem redundância.

Isso é diferente de uma sumarização de documento único porque o desafio inclui **eliminar redundância entre fontes** e **cobrir sub-tópicos distintos** do mesmo evento.

### 3) Qual vai ser o input (dados de entrada)? Dados reais ou fictícios?

**Dados reais.** Coletaríamos notícias de portais jornalísticos de acesso público (G1, Folha, BBC Brasil, etc.) sobre um tema específico. A coleta pode ser feita manualmente (copiar e colar) ou via raspagem simples de texto. A entrada do sistema seria uma pasta com vários arquivos de texto, cada um representando uma notícia sobre o mesmo assunto.

Alternativamente, poderíamos gerar conjuntos de notícias fictícias com LLM simulando a cobertura de um evento, garantindo variação de enfoque entre as fontes.

### 4) Como você está pensando na modelagem do grafo?

- **Vértices:** Cada sentença de **todas as notícias selecionadas** se torna um vértice. Por exemplo, se temos 5 notícias com ~20 sentenças cada, o grafo terá ~100 vértices.
- **Arestas:** Conectamos sentenças cuja similaridade textual (cosseno de TF-IDF) supere um limiar mínimo. A filtragem pelo limiar garante que só criamos arestas entre frases realmente relacionadas.
- **Pesos:** O valor da similaridade de cosseno entre as duas sentenças.
- **Algoritmo de grafo:** Aqui usaríamos **dois algoritmos em sequência**:
  1. **Detecção de Comunidades (Girvan-Newman ou baseado em Modularidade):** para identificar automaticamente sub-tópicos no grafo. Cada comunidade de sentenças fortemente conectadas representa um ângulo diferente do evento (ex: "placar da votação", "reações da oposição", "próximos passos").
  2. **PageRank/TextRank em cada comunidade:** para selecionar a sentença mais representativa de cada sub-tópico.
  
  Ambos os algoritmos seriam implementados manualmente.

### 5) Qual outra estrutura de dados, além de grafos, você está pensando em utilizar?

1. **Tabela Hash:** Para detecção e remoção eficiente de frases duplicadas ou quase-duplicatas entre diferentes notícias (hashing das frases normalizadas) e para contagem de frequência de termos no cálculo do TF-IDF.

2. **Fila de Prioridade (Max-Heap):** Após o ranqueamento em cada comunidade, usar o Heap para selecionar e classificar as melhores sentenças de forma eficiente.

**Justificativa técnica:** A Tabela Hash é crucial aqui porque, em sumarização multi-documento, muitas frases de fontes diferentes dizem a mesma coisa com palavras ligeiramente diferentes. A detecção rápida de duplicatas evita redundância no resumo. O Heap permite extrair eficientemente as *k* melhores sentenças do ranqueamento.

---

## 📂 Opção 3: Área Médica / Saúde (Sumarização de Evoluções Clínicas)

### 1) Qual será a área de aplicação do trabalho?

A área de aplicação é **Saúde Digital e Gestão de Prontuários Eletrônicos**. O foco está em ajudar médicos a obterem uma visão rápida do histórico clínico de pacientes com prontuários extensos. Em hospitais e clínicas, prontuários eletrônicos acumulam registros de múltiplas consultas, exames, prescrições e evoluções ao longo de meses ou anos. O médico plantonista que recebe um paciente pela primeira vez precisa entender rapidamente o quadro clínico, sem ter tempo de ler todo o histórico.

### 2) Qual problema você deseja resolver?

O problema é: **dado o prontuário eletrônico completo de um paciente (contendo múltiplas anotações médicas cronológicas), gerar automaticamente um resumo que destaque os sintomas persistentes, diagnósticos confirmados, medicamentos em uso e condutas médicas mais relevantes.**

Por exemplo, um paciente internado há 15 dias tem 15 ou mais registros de evolução diária. O sistema extrairia as frases que melhor sintetizam: "paciente apresenta diabetes tipo 2 controlada com metformina", "relato de dor torácica recorrente", "indicação de acompanhamento cardiológico". Isso permite que o médico do plantão tenha uma visão panorâmica sem ler cada registro individualmente — reduzindo risco de erro por falta de informação.

### 3) Qual vai ser o input (dados de entrada)? Dados reais ou fictícios?

**Dados fictícios**, gerados com auxílio de LLM. Não podemos usar prontuários reais por questões de privacidade e regulamentação (LGPD e sigilo médico). Os dados serão anotações médicas simuladas no padrão SOAP (Subjetivo, Objetivo, Avaliação, Plano), que é o formato mais usado em prontuários brasileiros. A LLM gerará históricos clínicos coerentes com condições médicas reais, incluindo terminologia médica adequada (CID, nomes de medicamentos, procedimentos).

A entrada do sistema seria o texto completo de todas as evoluções clínicas de um paciente (arquivo de texto com múltiplos registros datados).

### 4) Como você está pensando na modelagem do grafo?

- **Vértices:** Cada sentença das anotações médicas cronológicas se torna um vértice. As sentenças são segmentadas a partir de todos os registros de evolução do paciente.
- **Arestas:** Conectamos sentenças que compartilham **termos médicos em comum** (identificados através de um dicionário/léxico médico pré-definido contendo nomes de doenças, medicamentos, sintomas, etc.) ou que possuem alta similaridade semântica via TF-IDF.
- **Pesos:** A similaridade de cosseno base é **ponderada com bônus para frases contendo termos críticos**. Por exemplo, frases que mencionam "alergia", nomes de medicamentos, diagnósticos (CIDs) ou termos de urgência recebem multiplicador no peso, pois são clinicamente mais importantes.
- **Algoritmo de grafo:** Usamos **Centralidade de Grau Ponderada (Degree Centrality)** para encontrar as sentenças mais "conectadas" — a intuição é que a frase que compartilha termos médicos com o maior número de outras frases é a que melhor resume uma condição clínica recorrente. Implementado manualmente.

### 5) Qual outra estrutura de dados, além de grafos, você está pensando em utilizar?

1. **Trie (Árvore de Prefixos):** Implementada manualmente para armazenar o dicionário de termos médicos. Permite buscas rápidas por prefixo — por exemplo, ao buscar "metro", encontra "metformina", "metotrexato", "metronidazol". Isso é útil para identificar variações de termos médicos nas anotações (abreviações, formas parciais). Complexidade de busca $O(m)$ onde $m$ é o tamanho da palavra buscada, independente do tamanho do dicionário.

2. **Fila de Prioridade (Max-Heap):** Para ordenar as sentenças tanto por relevância clínica (score do grafo) quanto cronologicamente, e extrair as *k* mais importantes de forma eficiente.

**Justificativa técnica:** A Trie é particularmente adequada aqui porque o vocabulário médico é muito específico e muitas vezes os médicos escrevem abreviações (ex: "HAS" para hipertensão arterial sistêmica, "DM2" para diabetes mellitus tipo 2). A Trie permite buscar eficientemente se um token do texto corresponde a algum termo médico do dicionário.

---

## 📂 Opção 4: Área Acadêmica (Resumos de Artigos Científicos)

### 1) Qual será a área de aplicação do trabalho?

A área de aplicação é **Educação, Pesquisa Acadêmica e Biblioteconomia**. O foco está em ajudar pesquisadores, estudantes de pós-graduação e profissionais que precisam processar uma grande quantidade de literatura científica. Na rotina acadêmica, é comum precisar avaliar dezenas de artigos por semana durante uma revisão bibliográfica, e ler cada um integralmente consome muito tempo. Uma ferramenta de sumarização automática permite ao pesquisador ter uma visão rápida do conteúdo e decidir se o artigo merece leitura completa.

### 2) Qual problema você deseja resolver?

O problema é: **dado um artigo científico em formato PDF, gerar automaticamente um resumo extrativo composto pelas frases mais relevantes do documento, focando nas contribuições principais, metodologia e resultados.**

Por exemplo, um artigo de 12 páginas sobre "Relações entre jogos digitais e aprendizagem" seria processado pelo sistema, que identificaria e extrairia as 5 sentenças mais informativas — como a descrição do objetivo da pesquisa, as principais descobertas e a conclusão do autor. Isso permite que o pesquisador avalie em segundos se o artigo é relevante para sua revisão bibliográfica.

O diferencial em relação a simplesmente ler o "Abstract" do artigo é que o sistema analisa **todo o corpo do texto** e pode capturar frases importantes que estão nas seções de desenvolvimento e conclusão, que o resumo original do autor não necessariamente cobre.

### 3) Qual vai ser o input (dados de entrada)? Dados reais ou fictícios?

**Dados reais.** A entrada é um arquivo **PDF de artigo científico** que o usuário fornece ao programa. O sistema extrai automaticamente o texto do PDF usando a biblioteca PyPDF2 (permitida pelas regras, pois é apenas para extração de texto — os algoritmos de grafo são implementados por nós). 

As fontes dos artigos podem ser bases de dados acadêmicas abertas como **Google Scholar, SciELO, PubMed ou repositórios institucionais de universidades**. Como os artigos acadêmicos são publicações públicas, não há problema de privacidade.

O sistema aceita artigos em **português e inglês** (o processamento usa stopwords de ambos os idiomas).

### 4) Como você está pensando na modelagem do grafo?

- **Vértices:** Cada sentença do artigo se torna um vértice do grafo. O texto do PDF é limpo (remoção de cabeçalhos de página, rodapés, URLs, referências bibliográficas) e segmentado em sentenças usando o NLTK. Sentenças muito curtas (menos de 8 palavras), duplicatas e metadados são filtrados automaticamente.
- **Arestas:** Dois vértices (sentenças) são conectados **somente se a similaridade de cosseno entre seus vetores TF-IDF for superior a um limiar mínimo** (padrão: 0,10). Esse limiar funciona como técnica de filtragem: arestas fracas demais são descartadas, mantendo no grafo apenas conexões significativas.
- **Pesos das arestas:** O valor numérico da similaridade de cosseno entre os vetores TF-IDF das duas sentenças. Cada sentença é representada como um vetor esparso onde cada dimensão corresponde a um termo do vocabulário, ponderado pelo TF-IDF (Term Frequency × Inverse Document Frequency).
- **Representação do grafo:** Lista de adjacência usando dicionário Python (`{vertice: [(vizinho, peso), ...]}`) — mais eficiente que matriz de adjacência para grafos esparsos.
- **Algoritmo de grafo principal:** **TextRank (PageRank adaptado para texto)**, implementado inteiramente do zero, sem NetworkX nem bibliotecas de grafos. O algoritmo é iterativo:
  1. Inicializa todos os scores uniformemente ($1/n$).
  2. Em cada iteração, o novo score de um vértice é calculado como soma ponderada dos scores dos vizinhos, dividido pelo grau ponderado de cada vizinho, multiplicado por um fator de amortecimento (damping = 0,85).
  3. Repete até convergência (diferença máxima entre iterações < $10^{-6}$) ou até 100 iterações.
  4. O resultado é um score de importância para cada sentença: quanto mais conectada a sentença está a outras sentenças importantes, maior seu score.

### 5) Qual outra estrutura de dados, além de grafos, você está pensando em utilizar?

Utilizaremos **duas estruturas adicionais**, ambas implementadas manualmente:

1. **Árvore AVL (Árvore Binária de Busca Balanceada):** Usada para armazenar o vocabulário de termos técnicos do documento de forma **ordenada**. Cada nó da árvore contém um termo e sua frequência total no documento. As operações de inserção, busca e atualização de frequência são realizadas em $O(\log n)$ graças ao balanceamento automático (rotações simples e duplas). Isso permite:
   - Buscar rapidamente se um termo já existe no vocabulário.
   - Listar os termos mais frequentes em ordem (percurso em-ordem).
   - Manter o vocabulário organizado sem custo adicional de ordenação.
   
   **Por que AVL e não apenas um dicionário Python?** A AVL demonstra domínio de uma estrutura de dados avançada (requisito da matéria) e oferece a capacidade de listar termos em ordem alfabética naturalmente, além de permitir operações de range query (buscar todos os termos entre "A" e "B") que um dicionário hash não suporta.

2. **Fila de Prioridade (Max-Heap):** Implementada manualmente com operações de `inserir` ($O(\log n)$) e `extrair_máximo` ($O(\log n)$). Após o TextRank calcular os scores de todas as sentenças, o Max-Heap é usado para selecionar eficientemente as *k* sentenças com maior score para compor o resumo. Cada elemento do heap é uma tupla `(score, índice_original, texto_da_sentença)`.

**Justificativa técnica:** A AVL garante complexidade logarítmica para manipulação do vocabulário (que em artigos científicos pode ter 1.000+ termos únicos) e demonstra uso de estrutura de dados não-trivial. O Heap evita a necessidade de ordenar toda a lista de sentenças quando queremos apenas as top-*k*.

---

## 📂 Opção 5: Área Financeira (Análise de Relatórios Trimestrais de Empresas)

### 1) Qual será a área de aplicação do trabalho?

A área de aplicação é **Mercado Financeiro e Análise de Investimentos**. O foco está na sumarização automática de relatórios corporativos — os documentos que empresas listadas em bolsa publicam periodicamente (relatórios trimestrais, anuais, formulários de referência da CVM, ou os equivalentes internacionais como 10-K da SEC). Esses documentos são extensos (frequentemente 50 a 200+ páginas) e contêm informações cruciais sobre faturamento, endividamento, riscos, perspectivas e estratégia da empresa. Analistas financeiros, gestores de fundos e investidores individuais precisam processar essas informações rapidamente para tomar decisões de investimento.

### 2) Qual problema você deseja resolver?

O problema é: **dado o texto de um relatório financeiro de uma empresa, gerar automaticamente um resumo executivo contendo as frases que descrevem os dados de desempenho mais relevantes (receita, lucro, crescimento, endividamento) e os principais fatores de risco mencionados.**

Por exemplo, um relatório trimestral da Petrobras pode ter 80 páginas. O sistema extrairia frases como "A receita líquida cresceu 12% no trimestre, impulsionada pelo aumento do preço do barril" e "Os principais riscos identificados incluem a volatilidade cambial e mudanças na regulação ambiental". Isso permite que o analista obtenha uma visão geral do desempenho da empresa em segundos.

### 3) Qual vai ser o input (dados de entrada)? Dados reais ou fictícios?

**Dados reais ou fictícios, dependendo da disponibilidade.** Como primeira opção, usaríamos relatórios reais obtidos de portais de Relações com Investidores (RI) de empresas brasileiras listadas na B3 (ex: Petrobras, Vale, Itaú, Magazine Luiza). Esses documentos são públicos e disponíveis em PDF. 

Como alternativa ou complemento, poderíamos gerar relatórios financeiros fictícios com auxílio de LLM, simulando o padrão de redação corporativa com indicadores financeiros realistas (receita, EBITDA, margem líquida, dívida/EBITDA, etc.).

A entrada do sistema seria o arquivo PDF ou texto do relatório.

### 4) Como você está pensando na modelagem do grafo?

- **Vértices:** Cada sentença do relatório financeiro se torna um vértice. O texto é previamente limpo para remover índices, sumários, disclaimers legais e notas explicativas puramente numéricas (tabelas).
- **Arestas:** Conectamos sentenças por similaridade de cosseno (TF-IDF), com a mesma técnica de filtragem por limiar mínimo.
- **Pesos:** A similaridade de cosseno base recebe um **bônus multiplicador** quando ambas as sentenças contêm termos de um **léxico financeiro pré-definido** (ex: receita, lucro, EBITDA, margem, endividamento, risco, crescimento, queda, inadimplência). Isso faz com que frases com conteúdo financeiro relevante tenham arestas mais fortes entre si e, consequentemente, recebam scores maiores no TextRank.
- **Algoritmo de grafo:** **TextRank** implementado manualmente, com a adaptação de que os vértices que contêm termos do léxico financeiro recebem um peso inicial levemente maior (em vez de $1/n$ uniforme), sinalizando ao algoritmo que essas sentenças têm potencial de serem mais relevantes. Isso se chama "biased PageRank" e é uma variação legítima do algoritmo.

### 5) Qual outra estrutura de dados, além de grafos, você está pensando em utilizar?

1. **Tabela Hash (Dicionário):** Usada para armazenar o **léxico de termos financeiros de alto interesse** e seus respectivos fatores de relevância. Por exemplo: `{"ebitda": 2.0, "receita": 1.8, "risco": 1.5, "crescimento": 1.3}`. Quando uma sentença contém um desses termos, o peso de suas arestas é multiplicado pelo fator correspondente. A Tabela Hash permite verificar em $O(1)$ se um termo pertence ao léxico financeiro. Além disso, é usada para o cálculo do TF-IDF (frequência de termos).

2. **Fila de Prioridade (Max-Heap):** Para selecionar e ordenar as *k* sentenças financeiras mais impactantes para compor o resumo executivo. Mesma justificativa técnica das opções anteriores.

**Justificativa técnica:** A Tabela Hash é especialmente adequada aqui porque o léxico financeiro é consultado para cada termo de cada sentença do documento — consultas $O(1)$ são essenciais para não criar um gargalo de desempenho. O Heap garante extração eficiente das top-*k* sentenças do ranqueamento.

