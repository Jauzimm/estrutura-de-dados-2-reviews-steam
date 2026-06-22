"""
Módulo de aplicação do algoritmo PageRank sobre as reviews vetorizadas.
Usa similaridade de cosseno para construir o grafo e power iteration
para calcular os scores.
"""

import numpy as np
from tqdm import tqdm
from excecoes import GraphError


def _matriz_similaridade_cosseno(vetores: np.ndarray) -> np.ndarray:
    """Calcula a matriz de similaridade de cosseno entre vetores."""
    normas = np.linalg.norm(vetores, axis=1, keepdims=True)
    normas[normas == 0] = 1
    normalizados = vetores / normas
    return np.dot(normalizados, normalizados.T)


def _construir_matriz_transicao(similaridade: np.ndarray, limiar: float = 0.3) -> np.ndarray:
    """
    Constrói a matriz de transição column‑stochastic M.
    Arestas com similaridade abaixo do limiar são descartadas.
    """
    N = similaridade.shape[0]
    adj = np.where(similaridade > limiar, similaridade, 0.0)
    soma_colunas = adj.sum(axis=0)
    mascara = soma_colunas == 0
    soma_colunas[mascara] = 1
    M = adj / soma_colunas
    M[:, mascara] = 1.0 / N
    return M


def _pagerank(
    M: np.ndarray,
    amortecimento: float = 0.85,
    tolerancia: float = 1e-6,
    max_iter: int = 100,
) -> np.ndarray:
    """
    Power iteration para PageRank.
    amortecimento: damping factor.
    """
    N = M.shape[0]
    pr = np.ones(N) / N
    for _ in range(max_iter):
        pr_novo = amortecimento * M.dot(pr) + (1 - amortecimento) / N
        if np.linalg.norm(pr_novo - pr, 2) < tolerancia:
            return pr_novo
        pr = pr_novo
    return pr


def calcular_pagerank_por_jogo(
    reviews_por_jogo: dict,
    limiar: float = 0.3,
    amortecimento: float = 0.85,
    tolerancia: float = 1e-6,
    max_iter: int = 100,
) -> dict:
    """
    Aplica PageRank para cada jogo (appid) baseado na similaridade
    entre as reviews.

    Parâmetros:
        reviews_por_jogo: dicionário {appid: [ {"vector", "review", "index"}, ... ]}
        limiar:          similaridade mínima para criar arestas.
        amortecimento:   damping factor.
        tolerancia:      tolerância para convergência.
        max_iter:        máximo de iterações.

    Retorno:
        dict: {appid: [ {"index": int, "review": str, "score": float}, ... ]}
              ordenado por score decrescente.
    """
    try:
        resultado = {}
        for appid, lista_reviews in tqdm(reviews_por_jogo.items(), desc="PageRank por jogo"):
            N = len(lista_reviews)
            if N == 0:
                resultado[appid] = []
                continue

            vetores = np.array([item["vector"] for item in lista_reviews])
            similaridade = _matriz_similaridade_cosseno(vetores)
            M = _construir_matriz_transicao(similaridade, limiar)
            scores = _pagerank(M, amortecimento=amortecimento, tolerancia=tolerancia, max_iter=max_iter)

            ordem = np.argsort(-scores)
            ranqueadas = []
            for idx in ordem:
                ranqueadas.append({
                    "index": lista_reviews[idx]["index"],
                    "review": lista_reviews[idx]["review"],
                    "score": float(scores[idx]),
                })
            resultado[appid] = ranqueadas

        return resultado
    except Exception as e:
        raise GraphError(f"Erro ao calcular PageRank: {e}") from e