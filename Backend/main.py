from pathlib import Path
import logging
import sys

from processamento_dados import limpar_e_filtrar_dataset
from processamento_nlp import vetorizar_reviews_spacy
from grafo_pagerank import calcular_pagerank_por_jogo
from selecao_reviews import selecionar_reviews_distintas, salvar_reviews_json
from excecoes import PipelineError

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Backend" / "results" / "reviews_resumidas.json"

# Parâmetros ajustáveis do pipeline
LIMIAR_PAGERANK = 0.3
AMORTECIMENTO_PAGERANK = 0.85
LIMIAR_SIMILARIDADE_SELECAO = 0.8

# Parâmetros de limpeza
MIN_PALAVRAS_POR_REVIEW = 5          # mínimo de palavras por review
MIN_REVIEWS_POR_JOGO = 10            # mínimo de reviews para manter o jogo
LIMIAR_JACCARD_COPYPASTA = 0.85      # limiar para remoção de quase‑duplicatas


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logger = logging.getLogger(__name__)

    try:
        # 1° Limpeza e filtragem
        dados_tratados = limpar_e_filtrar_dataset(
            DATASET_PATH,
            CLEAN_DATASET_PATH,
            min_palavras=MIN_PALAVRAS_POR_REVIEW,
            min_reviews_por_jogo=MIN_REVIEWS_POR_JOGO,
            limiar_jaccard=LIMIAR_JACCARD_COPYPASTA
        )

        # Mapeamento appid -> nome do jogo
        appid_para_jogo = dict(zip(dados_tratados["appid"], dados_tratados["game"]))

        # 2° Vetorização com spaCy
        reviews_por_jogo = vetorizar_reviews_spacy(dados_tratados)

        # 3° PageRank
        pagerank_resultado = calcular_pagerank_por_jogo(
            reviews_por_jogo,
            limiar=LIMIAR_PAGERANK,
            amortecimento=AMORTECIMENTO_PAGERANK
        )

        # 4° Seleção das melhores reviews distintas
        melhores_reviews = selecionar_reviews_distintas(
            pagerank_resultado,
            reviews_por_jogo,
            limiar_similaridade=LIMIAR_SIMILARIDADE_SELECAO
        )

        # 5° Exportação para JSON
        salvar_reviews_json(melhores_reviews, OUTPUT_PATH, appid_para_jogo)
        logger.info("Pipeline concluído com sucesso. Resultado em: %s", OUTPUT_PATH)

    except PipelineError as e:
        logger.error("Erro no pipeline: %s", e)
        sys.exit(1)
    except Exception:
        logger.exception("Erro inesperado no pipeline")
        sys.exit(2)


if __name__ == "__main__":
    main()