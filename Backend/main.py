from pathlib import Path
import pandas as pd
from data_processing import tratar_dataset


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Backend" / "results" / "reviews_resumidas.json"

# def tratar_reviews_com_spacy(dados: pd.DataFrame) -> pd.DataFrame:
#     raise NotImplementedError()


# def aplicar_pagerank_reviews(dados_tratados: pd.DataFrame) -> pd.DataFrame:
#     raise NotImplementedError()


# def selecionar_melhores_reviews_distintas(resultado_pagerank: pd.DataFrame) -> pd.DataFrame:
#     raise NotImplementedError()


# def imprimir_e_salvar_melhores_reviews(
#     melhores_reviews: pd.DataFrame,
#     output_path: Path
# ) -> None:
#     raise NotImplementedError()


def main() -> None:
    dados_tratados = tratar_dataset(DATASET_PATH, CLEAN_DATASET_PATH)
    # dados_tratados = tratar_reviews_com_spacy(dados_tratados)
    # resultado_pagerank = aplicar_pagerank_reviews(dados_tratados)
    # melhores_reviews = selecionar_melhores_reviews_distintas(resultado_pagerank)
    # imprimir_e_salvar_melhores_reviews(melhores_reviews, OUTPUT_PATH)


if __name__ == "__main__":
    main()