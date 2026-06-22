from pathlib import Path
import pandas as pd
import numpy as np
from data_processing import tratar_dataset
from nlp_processing import tratar_reviews_com_spacy

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Backend" / "results" / "reviews_resumidas.json"

def main() -> None:
    # 1° Tratar o dataset (limpeza e filtragem)
    dados_tratados = tratar_dataset(DATASET_PATH, CLEAN_DATASET_PATH)

    # 2° Processar as reviews com spaCy para obter vetores médios por jogo
    reviews_por_jogo = tratar_reviews_com_spacy(dados_tratados)
    
    # resultado_pagerank = aplicar_pagerank_reviews(reviews_por_jogo)
    # melhores_reviews = selecionar_melhores_reviews_distintas(resultado_pagerank)
    # imprimir_e_salvar_melhores_reviews(melhores_reviews, OUTPUT_PATH)

if __name__ == "__main__":
    main()