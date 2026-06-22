"""
Módulo de seleção das melhores reviews por jogo (diversas) e exportação para JSON.
"""

import json
import numpy as np
from pathlib import Path
from tqdm import tqdm


def _similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Similaridade de cosseno entre dois vetores."""
    dot = np.dot(vec1, vec2)
    norma = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot / norma if norma > 0 else 0.0


def selecionar_reviews_distintas(
    pagerank_resultado: dict,
    reviews_por_jogo: dict,
    limiar_similaridade: float = 0.8
) -> dict:
    """
    Seleciona as top‑k reviews de cada jogo com maior score PageRank,
    garantindo que sejam distintas entre si (similaridade cosseno < limiar).

    Parâmetros:
        pagerank_resultado: dict {appid: [{"index": int, "review": str, "score": float}, ...]}
                            já ordenado por score decrescente.
        reviews_por_jogo: dict {appid: [{"vector": np.ndarray, "index": int}, ...]}
                          (retornado pelo processamento NLP).
        limiar_similaridade: reviews com similaridade >= isso são consideradas muito parecidas.

    Retorno:
        dict com o mesmo formato de pagerank_resultado, porém apenas com as reviews selecionadas.
    """
    melhores = {}

    for appid, ranking in tqdm(pagerank_resultado.items(), desc="Seleção de reviews distintas"):
        lista_completa = reviews_por_jogo.get(appid, [])
        idx_para_vetor = {item["index"]: item["vector"] for item in lista_completa}

        N = len(ranking)
        # Define quantas reviews selecionar
        if N <= 10:
            k = 1
        elif N <= 25:
            k = 3
        else:
            k = 5

        selecionadas = []
        for item in ranking:
            if len(selecionadas) >= k:
                break
            vetor_atual = idx_para_vetor.get(item["index"])
            if vetor_atual is None:
                continue

            muito_similar = False
            for sel in selecionadas:
                vetor_sel = idx_para_vetor[sel["index"]]
                sim = _similaridade_cosseno(vetor_atual, vetor_sel)
                if sim >= limiar_similaridade:
                    muito_similar = True
                    break

            if not muito_similar:
                selecionadas.append(item)

        melhores[appid] = selecionadas

    return melhores


def salvar_reviews_json(
    melhores_reviews: dict,
    output_path: Path,
    appid_para_jogo: dict
) -> None:
    """
    Salva as reviews selecionadas em um arquivo JSON.

    Parâmetros:
        melhores_reviews: dict {appid: [{"index": int, "review": str, "score": float}, ...]}
        output_path: caminho do arquivo .json de saída.
        appid_para_jogo: dicionário {appid: nome_do_jogo}
    """
    resultado_final = []
    for appid, reviews in melhores_reviews.items():
        nome_jogo = appid_para_jogo.get(appid, "Desconhecido")
        resultado_final.append({
            "appid": appid,
            "game": nome_jogo,
            "top_reviews": [
                {
                    "review": r["review"],
                    "score": r["score"]
                }
                for r in reviews
            ]
        })

    # Cria diretório se necessário
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)