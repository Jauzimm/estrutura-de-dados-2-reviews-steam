import spacy
import numpy as np
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
from excecoes import NLPProcessingError

# Carrega o modelo uma única vez, desabilitando componentes desnecessários
try:
    nlp = spacy.load("pt_core_news_md", disable=["parser", "ner", "tagger", "lemmatizer", "textcat"])
except Exception as e:
    raise NLPProcessingError(f"Não foi possível carregar o modelo spaCy 'pt_core_news_md': {e}") from e


def vetorizar_reviews_spacy(dados: pd.DataFrame) -> dict:
    """
    Processa as reviews com spaCy e retorna um dicionário com os vetores
    médios de palavras para cada review, agrupados por jogo.

    Retorno:
        dict: { appid: [ {"review": str, "vector": np.ndarray, "index": int}, ... ] }
    """
    resultado = defaultdict(list)

    try:
        # Agrupa por jogo com barra de progresso
        for appid, grupo in tqdm(dados.groupby("appid"), desc="Processando jogos"):
            textos = grupo["review"].tolist()
            indices = grupo.index.tolist()

            # Processa todos os textos do jogo de uma vez (pipe)
            docs = list(nlp.pipe(textos))

            for idx, doc in zip(indices, docs):
                # Filtra tokens válidos: não stopword, não pontuação, não espaço, com vetor
                vetores_palavras = [
                    token.vector
                    for token in doc
                    if not token.is_stop
                    and not token.is_punct
                    and not token.is_space
                    and not token.is_oov
                ]

                if vetores_palavras:
                    vetor_medio = np.mean(vetores_palavras, axis=0)
                else:
                    vetor_medio = doc.vector

                resultado[appid].append({
                    "review": grupo.loc[idx, "review"],
                    "vector": vetor_medio,
                    "index": idx,
                })

    except Exception as e:
        raise NLPProcessingError(f"Erro ao vetorizar reviews com spaCy: {e}") from e

    return dict(resultado)
