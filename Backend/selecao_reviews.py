import json
import numpy as np
from pathlib import Path
from tqdm import tqdm


def _similaridade_cosseno(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Similaridade de cosseno entre dois vetores."""
    # Produto escalar entre os dois vetores
    dot = np.dot(vec1, vec2)
    # Produto das normas de cada vetor
    norma = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    # Retorna similaridade; se norma for zero, retorna 0.0
    return dot / norma if norma > 0 else 0.0


def selecionar_reviews_distintas(
    pagerank_resultado: dict,
    reviews_por_jogo: dict,
    limiar_similaridade: float = 0.8,
    politica_k: list = None
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
        politica_k: lista de pares (limite_superior, quantidade) que define
                    quantas reviews selecionar conforme o total disponível.
                    Exemplo: [(10, 1), (25, 3), (float("inf"), 5)].
                    Se None, usa a política padrão: ≤10 → 1, ≤25 → 3, >25 → 5.

    Retorno:
        dict com o mesmo formato de pagerank_resultado, porém apenas com as reviews selecionadas.
    """
    # Define política padrão se nenhuma for passada
    if politica_k is None:
        politica_k = [(10, 1), (25, 3), (float("inf"), 5)]

    melhores = {}

    # Itera sobre cada jogo com barra de progresso
    for appid, ranking in tqdm(pagerank_resultado.items(), desc="Seleção de reviews distintas"):
        # Lista completa de itens (com vetores) para este jogo
        lista_completa = reviews_por_jogo.get(appid, [])
        # Mapeia índice original para o vetor da review (acesso rápido)
        idx_para_vetor = {item["index"]: item["vector"] for item in lista_completa}

        N = len(ranking)
        # Determina o número k de reviews a selecionar segundo a política
        k = 1  # fallback mínimo
        for limite, quantidade in politica_k:
            if N <= limite:
                k = quantidade
                break

        selecionadas = []
        # Percorre o ranking (ordenado por score) tentando preencher as k vagas
        for item in ranking:
            if len(selecionadas) >= k:
                break

            # Vetor da review candidata atual
            vetor_atual = idx_para_vetor.get(item["index"])
            if vetor_atual is None:
                continue  # caso raro: vetor ausente

            # Verifica se a review atual é muito similar a alguma já selecionada
            muito_similar = False
            for sel in selecionadas:
                vetor_sel = idx_para_vetor[sel["index"]]
                sim = _similaridade_cosseno(vetor_atual, vetor_sel)
                # Se a similaridade atinge o limiar, descarta a candidata
                if sim >= limiar_similaridade:
                    muito_similar = True
                    break

            # Se passou no teste de diversidade, adiciona às selecionadas
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

    # Para cada jogo, monta o dicionário de saída com nome e top reviews
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

    # Garante que o diretório de saída existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Grava o JSON formatado (acentos e indentação)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)