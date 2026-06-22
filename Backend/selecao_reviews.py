"""
Módulo de seleção das melhores reviews por jogo (diversas) e exportação para JSON.
"""

import json
import numpy as np
from pathlib import Path
from tqdm import tqdm
import logging
from excecoes import SelectionError


def _similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    dot = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot / norm if norm > 0 else 0.0


def selecionar_reviews_distintas(
    pagerank_resultado: dict,
    reviews_por_jogo: dict,
    limiar_similaridade: float = 0.8,
) -> dict:
    """
    Seleciona as top-k reviews de cada jogo com maior score PageRank,
    garantindo que sejam distintas entre si (similaridade cosseno < limiar).
    """
    melhores = {}

    for appid, ranking in tqdm(pagerank_resultado.items(), desc="Seleção de reviews distintas"):
        lista_completa = reviews_por_jogo.get(appid, [])
        idx_para_vetor = {item["index"]: item["vector"] for item in lista_completa}

        N = len(ranking)
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


def salvar_reviews_json(melhores_reviews: dict, output_path: Path, appid_para_jogo: dict) -> None:
    resultado_final = []
    for appid, reviews in melhores_reviews.items():
        nome_jogo = appid_para_jogo.get(appid, "Desconhecido")
        resultado_final.append({
            "appid": appid,
            "game": nome_jogo,
            "top_reviews": [
                {"review": r["review"], "score": r["score"]} for r in reviews
            ],
        })

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(resultado_final, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise SelectionError(f"Falha ao salvar JSON de resultados: {e}") from e
    logger = logging.getLogger(__name__)
    logger.info("Resultado salvo em: %s", output_path)
