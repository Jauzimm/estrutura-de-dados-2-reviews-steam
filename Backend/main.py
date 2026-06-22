from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Frontend" / "reviews_resumidas.json"


def tratar_dataset(dataset_path: Path, output_path: Path) -> pd.DataFrame:
    colunas_desejadas = [
        "recommendationid",
        "appid",
        "game",
        "review"
    ]

    dados = pd.read_csv(dataset_path)

    dados = dados[colunas_desejadas]

    dados.to_csv(
        output_path,
        index=False
    )

    return dados


# def tratar_reviews_com_spacy(dados: pd.DataFrame) -> pd.DataFrame:
#     raise NotImplementedError()


# def aplicar_pagerank_reviews(dados_tratados: pd.DataFrame) -> pd.DataFrame:
#     raise NotImplementedError()


# def selecionar_melhores_reviews_distintas(resultado_pagerank: pd.DataFrame) -> pd.DataFrame:
#     raise NotImplementedError()


# def imprimir_e_salvar_melhores_reviews(melhores_reviews: pd.DataFrame, output_path: Path) -> None:
#     raise NotImplementedError()


# def salvar_dataset_limpo(dados: pd.DataFrame, output_path: Path) -> None:
#     dados.to_csv(output_path, index=False)


def main() -> None:
    dados_tratados = tratar_dataset(DATASET_PATH,CLEAN_DATASET_PATH)

    # dados_tratados = tratar_reviews_com_spacy(dados)

    # resultado_pagerank = aplicar_pagerank_reviews(dados_tratados)

    # melhores_reviews = selecionar_melhores_reviews_distintas(resultado_pagerank)

    # imprimir_e_salvar_melhores_reviews(melhores_reviews, OUTPUT_PATH)


if __name__ == "__main__":
    main()