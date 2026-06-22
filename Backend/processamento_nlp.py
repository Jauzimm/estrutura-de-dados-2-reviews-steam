import spacy
import numpy as np
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
from excecoes import NLPProcessingError

# ------------------------------------------------------------
# Carrega o modelo spaCy uma única vez, desabilitando componentes
# que não são necessários para obter vetores de palavras.
# Isso acelera significativamente o processamento.
# ------------------------------------------------------------
try:
    nlp = spacy.load(
        "pt_core_news_md",
        disable=["parser", "ner", "tagger", "lemmatizer", "textcat"]
    )
except Exception as e:
    raise NLPProcessingError(
        f"Não foi possível carregar o modelo spaCy 'pt_core_news_md': {e}"
    ) from e


def vetorizar_reviews_spacy(dados: pd.DataFrame) -> dict:
    """
    Processa as reviews com spaCy e retorna um dicionário com os vetores
    médios de palavras para cada review, agrupados por jogo.

    Retorno:
        dict: { appid: [ {"review": str, "vector": np.ndarray, "index": int}, ... ] }
    """
    # Dicionário que conterá os resultados, agrupados por appid
    resultado = defaultdict(list)

    try:
        # Itera sobre cada jogo (appid) usando barra de progresso
        for appid, grupo in tqdm(dados.groupby("appid"), desc="Processando jogos"):
            # Obtém os textos das reviews e os índices originais do DataFrame
            textos = grupo["review"].tolist()
            indices = grupo.index.tolist()

            # Processa todos os textos do jogo de uma vez (pipe) para eficiência
            docs = list(nlp.pipe(textos))

            # Para cada review processada, extrai o vetor médio
            for idx, doc in zip(indices, docs):
                # Seleciona apenas tokens que possuem vetor e são relevantes:
                # - não sejam stopwords (palavras muito comuns)
                # - não sejam pontuação
                # - não sejam espaços em branco
                # - não estejam fora do vocabulário (sem vetor)
                vetores_palavras = [
                    token.vector
                    for token in doc
                    if not token.is_stop
                    and not token.is_punct
                    and not token.is_space
                    and not token.is_oov
                ]

                # Se restaram palavras com vetor, calcula a média
                if vetores_palavras:
                    vetor_medio = np.mean(vetores_palavras, axis=0)
                else:
                    # Fallback: usa o vetor do documento inteiro (média de todas as palavras)
                    vetor_medio = doc.vector

                # Armazena a review, seu vetor e o índice original
                resultado[appid].append({
                    "review": grupo.loc[idx, "review"],
                    "vector": vetor_medio,
                    "index": idx,
                })

    except Exception as e:
        raise NLPProcessingError(f"Erro ao vetorizar reviews com spaCy: {e}") from e

    # Converte o defaultdict para um dict normal antes de retornar
    return dict(resultado)