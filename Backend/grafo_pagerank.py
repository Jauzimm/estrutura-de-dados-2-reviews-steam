"""
Módulo de aplicação do algoritmo PageRank sobre as reviews vetorizadas.
Usa similaridade de cosseno para construir o grafo e power iteration
para calcular os scores.
"""

import numpy as np
from tqdm import tqdm
from excecoes import GraphError


def _matriz_similaridade_cosseno(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = vectors / norms
    sim = np.dot(normalized, normalized.T)
    return sim


def _construir_matriz_transicao(sim: np.ndarray, threshold: float = 0.3) -> np.ndarray:
    N = sim.shape[0]
    adj = np.where(sim > threshold, sim, 0.0)
    col_sum = adj.sum(axis=0)
    mask = (col_sum == 0)
    col_sum[mask] = 1
    M = adj / col_sum
    M[:, mask] = 1.0 / N
    return M


def _pagerank(M: np.ndarray, d: float = 0.85, tol: float = 1e-6, max_iter: int = 100) -> np.ndarray:
    N = M.shape[0]
    pr = np.ones(N) / N
    for _ in range(max_iter):
        pr_new = d * M.dot(pr) + (1 - d) / N
        if np.linalg.norm(pr_new - pr, 2) < tol:
            return pr_new
        pr = pr_new
    return pr


def calcular_pagerank_por_jogo(
    reviews_por_jogo: dict,
    threshold: float = 0.3,
    d: float = 0.85,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> dict:
    """
    Aplica PageRank para cada jogo (appid) baseado na similaridade
    entre as reviews.
    Retorna: dict {appid: [ {"index": int, "review": str, "score": float}, ... ] }
    """
    try:
        resultado = {}
        for appid, lista_reviews in tqdm(reviews_por_jogo.items(), desc="PageRank por jogo"):
            N = len(lista_reviews)
            if N == 0:
                resultado[appid] = []
                continue

            vectors = np.array([item["vector"] for item in lista_reviews])
            sim = _matriz_similaridade_cosseno(vectors)
            M = _construir_matriz_transicao(sim, threshold)
            scores = _pagerank(M, d=d, tol=tol, max_iter=max_iter)

            order = np.argsort(-scores)
            ranked = []
            for idx in order:
                ranked.append({
                    "index": lista_reviews[idx]["index"],
                    "review": lista_reviews[idx]["review"],
                    "score": float(scores[idx]),
                })
            resultado[appid] = ranked

        return resultado
    except Exception as e:
        raise GraphError(f"Erro ao calcular PageRank: {e}") from e
