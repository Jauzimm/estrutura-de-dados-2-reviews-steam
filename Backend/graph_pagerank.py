"""
Módulo de aplicação do algoritmo PageRank sobre as reviews vetorizadas.
Usa similaridade de cosseno para construir o grafo e power iteration
para calcular os scores, sem recorrer a bibliotecas prontas de PageRank.
"""

import numpy as np
from tqdm import tqdm


def _cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    """
    Calcula a matriz de similaridade de cosseno entre um conjunto de vetores.
    vectors: array de shape (N, D)
    Retorna: array (N, N) com valores entre -1 e 1.
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = vectors / norms
    sim = np.dot(normalized, normalized.T)
    return sim


def _build_transition_matrix(sim: np.ndarray, threshold: float = 0.3) -> np.ndarray:
    """
    Constrói a matriz de transição column‑stochastic M.
    sim: matriz de similaridade (N, N)
    threshold: arestas com similaridade abaixo disso são descartadas.
    """
    N = sim.shape[0]
    adj = np.where(sim > threshold, sim, 0.0)
    col_sum = adj.sum(axis=0)
    mask = (col_sum == 0)
    col_sum[mask] = 1
    M = adj / col_sum
    M[:, mask] = 1.0 / N
    return M


def _pagerank(M: np.ndarray, d: float = 0.85, tol: float = 1e-6,
              max_iter: int = 100) -> np.ndarray:
    """
    Power iteration para PageRank.
    M: matriz de transição column‑stochastic (N, N)
    """
    N = M.shape[0]
    pr = np.ones(N) / N
    for _ in range(max_iter):
        pr_new = d * M.dot(pr) + (1 - d) / N
        if np.linalg.norm(pr_new - pr, 2) < tol:
            return pr_new
        pr = pr_new
    return pr


def aplicar_pagerank_reviews(
    reviews_por_jogo: dict,
    threshold: float = 0.3,
    d: float = 0.85,
    tol: float = 1e-6,
    max_iter: int = 100
) -> dict:
    """
    Aplica PageRank para cada jogo (appid) baseado na similaridade
    entre as reviews.
    """
    resultado = {}
    for appid, lista_reviews in tqdm(reviews_por_jogo.items(),
                                     desc="PageRank por jogo"):
        N = len(lista_reviews)
        if N == 0:
            resultado[appid] = []
            continue

        vectors = np.array([item["vector"] for item in lista_reviews])
        sim = _cosine_similarity_matrix(vectors)
        M = _build_transition_matrix(sim, threshold)
        scores = _pagerank(M, d=d, tol=tol, max_iter=max_iter)

        order = np.argsort(-scores)
        ranked = []
        for idx in order:
            ranked.append({
                "index": lista_reviews[idx]["index"],
                "review": lista_reviews[idx]["review"],
                "score": float(scores[idx])
            })
        resultado[appid] = ranked

    return resultado
