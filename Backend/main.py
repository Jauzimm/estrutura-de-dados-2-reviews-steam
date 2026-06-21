from pathlib import Path

import networkx as nx
import pandas as pd
import spacy


DATASET_PATH = Path("../Dataset/dataset_steamreview_ptbr.csv")
OUTPUT_PATH = Path("../Frontend/reviews_resumidas.json")


def tratar_dados_dataset_com_spacy(dataset_path: Path) -> pd.DataFrame:
    raise NotImplementedError()


def aplicar_pagerank_reviews(dados_tratados: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def selecionar_melhores_reviews_distintas(resultado_pagerank: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def imprimir_e_salvar_melhores_reviews(melhores_reviews: pd.DataFrame, output_path: Path) -> None:
    raise NotImplementedError()


def main() -> None:
    dados_tratados = tratar_dados_dataset_com_spacy(DATASET_PATH)
    resultado_pagerank = aplicar_pagerank_reviews(dados_tratados)
    melhores_reviews = selecionar_melhores_reviews_distintas(resultado_pagerank)
    imprimir_e_salvar_melhores_reviews(melhores_reviews, OUTPUT_PATH)


if __name__ == "__main__":
    main()
