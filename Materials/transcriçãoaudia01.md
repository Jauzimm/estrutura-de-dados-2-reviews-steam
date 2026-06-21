Professor: ...usar esse grafo. Como é que você vai pegar de fato quais são os reviews mais importantes dado esse grafo?

Aluno 1: É, mas a gente pode fazer primeiro o... sink node, flood node. Pode ver quantos reviews são conectados a um, se for direcionado um, ou a outra mencionando a outra, a da direcionalidade a eles.

Professor: Não, não. Muito mais complexo. Você não tem isso não. Então vamos lá, ó. As suas arestas vão ter pesinhos, né? Que é a quantidade de palavras em comum. Ah, vamos supor que essa daqui tem três palavras, essa daqui tem quatro, essa daqui tem em cinco, essa daqui tem sete, essa daqui tem uma, né? Beleza. E aí? Como é que você vai decidir, ó, você tem uma, duas, três, quatro... quatro reviews. Você quer duas reviews só. Quais são as duas reviews que você vai pegar aí?

Aluno 1: A gente pode pegar as que têm um caminho que somam o maior número de palavras...

Aluno 2: São duas... eu diria que são duas reviews que não estão interligadas entre a outra, mas têm um grau de correlacionalidade entre outras, entre elas, maior. Mas se você pegar as duas...

Professor: Mas como é que você vai transformar isso daí em algoritmo, hein?

Aluno 2: Você tirando as pontes. Tirando as de menores valores.

Professor: Hum... Mais ou menos. Aí o que que você tá fazendo é detecção de tópicos. Aí vocês vão entrar na... na do pessoal do tema de hoje.

Aluno 2: Mas a sumarização é a partir de tópicos. Saber sumarizar o tópico de...

Professor: Não, porque não necessariamente. Porque olha, eh... o pessoal de tópicos é: eu quero dois tópicos, né? Dois tópicos. É isso e isso, ou isso e isso, né? O de vocês não, é... é sumarizar, é pegar menos vértices. Hum... Então olha, quais são os vértices que vocês vão pegar? É quais são os vértices mais representativos. Como é que você vai definir isso? Ó, você tem... em escala menor, você tem quatro reviews aqui. Você quer pegar só duas. Mas quais são as duas que vocês vão pegar aí?

Aluno 1: Acho que as que têm mais conexões...

Aluno 2: É, eu ia falar...

Professor: Mais conexões? Hum, não necessariamente. E que...

Aluno 1: Ou as arestas têm o valor maior?

Professor: Não necessariamente. A gente quer... provavelmente o que eu ia falar é... eh... provavelmente arestas que têm mais conexões com outras, com outras, e também são reviews que são distintas.

Aluno 2: Então, tem que ser esses dois... esses dois trade-offs... trade-offs, né? Porque olha aqui ó: essa daqui com essa daqui, tá vendo que são três ligações, né? Se eu pegar essas duas...

Aluno 2: Elas são correlacionadas, vão falar a mesma coisa.

Professor: Não, eu não pegaria essas duas não, porque elas tão... são quase parecidas. Elas têm cinco palavras em comum. Eu prefiro pegar reviews que são diferentes entre si, porque aí eu consigo mais... variedade, né?

Aluno 2: Elas são... elas são diferentes entre si e ao mesmo tempo têm várias correlacionando com elas. Por exemplo, a melhor opção nesse caso aqui seria as duas da ponta. Porque elas são diferentes, mas é a maior quantidade que tem de diferente...

Professor: É, mas o problema é: como é que a gente traduz isso daí de forma algorítmica?

Aluno 2: Qual dos algoritmos que você passou em sala seria melhor pra isso?

Professor: Ó, então olha. Estuda o PageRank. Vocês não... não podem usar biblioteca pronta do PageRank não. Mas entendam qual que é a lógica do PageRank. O PageRank, ele vai te retornar qual que é o peso de cada vértice. Ele vai te retornar um score. "Ah, esse aqui tem peso 10, esse aqui tem peso 9, esse aqui tem peso 5, esse aqui tem peso 3". Ele vai... ele vai te dar um peso, né, pra cada vértice. E aí o problema de vocês é: qual desses aqui você vai escolher? Tá, os que têm mais peso, né? Mas e aí, vai pegar dois? Três? Um? Tá vendo que tem o probleminha que é a quantidade que a gente não sabe, né?

Aluno 1: Pode correlacionar com a quantidade de reviews lidos, proporcional?

Professor: Não sei, aí é vocês que vão decidir. Então ó, o algoritmo PageRank ele só vai te dar os valorzinhos aqui. Então estuda ele lá, vê qual que é a ideia dele, tenta implementar. Vocês não podem pegar a biblioteca pronta dele não, viu?

Alunos: Beleza.

Professor: Vê qual que é a ideia dele de dar esses pesinhos aqui pros vértices. E aí, beleza. Uma vez que os vértices têm pesos, quais são os vértices mais importantes que eu vou pegar? Vou pegar os três? Por que que eu vou pegar três e por que que não pego dois? Tá vendo? Tem um... uma heurística aí que eu não sei definir. Por que que... por que quatro, cinco, seis, 10%, 20%? Como é que a gente vai definir isso?

Então amadurece essa ideia, vamos... vamos conversar nessa sexta-feira como é que vocês vão definir, olha: como... como definir... não, como definir não, como pegar quais são os vértices mais importantes. Entendeu?

Alunos: Sim.

Professor: Então amadurece como é que vocês vão fazer isso e me contem na sexta-feira.

Aluno 1: Professor, antes de o senhor ir, tem mais algum algoritmo que o senhor passou em sala que seria bom a gente estudar para esse aqui, para esse nosso caso?

Professor: Para sumarização? Não.

Aluno 1: Não?

Professor: Só o PageRank. É, estuda o PageRank. Já vai ser difícil.

Aluno 1: Ok, beleza.

Professor: Beleza? Deixa eu atender o próximo grupo aí. Próximo! Assina a lista de presença só.

Alunos: Ah, obrigado. Valeu, professor.