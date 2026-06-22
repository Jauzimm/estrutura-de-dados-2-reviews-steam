from pathlib import Path
import pandas as pd
import numpy as np
from data_processing import tratar_dataset
from nlp_processing import tratar_reviews_com_spacy
from graph_pagerank import aplicar_pagerank_reviews

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Backend" / "results" / "reviews_resumidas.json"

def main() -> None:
    # 1° Tratar o dataset (limpeza e filtragem)
    dados_tratados = tratar_dataset(DATASET_PATH, CLEAN_DATASET_PATH)

    # 2° Processar as reviews com spaCy para obter vetores médios por jogo
    reviews_por_jogo = tratar_reviews_com_spacy(dados_tratados)

    # 3° PageRank
    pagerank_resultado = aplicar_pagerank_reviews(reviews_por_jogo, threshold=0.3, d=0.85)

        # --- INSPEÇÃO TEMPORÁRIA DO PAGERANK ---
    print("\n" + "="*60)
    print("INSPEÇÃO DO PAGERANK")
    print("="*60)
    # Escolha alguns jogos para inspecionar (ex.: os 3 primeiros)
    jogos_amostra = list(pagerank_resultado.keys())[:3]
    for appid in jogos_amostra:
        reviews_rankeadas = pagerank_resultado[appid]
        print(f"\nappid: {appid}")
        print(f"Total de reviews: {len(reviews_rankeadas)}")
        # Mostra as 3 melhores reviews (se existirem)
        for i, item in enumerate(reviews_rankeadas[:3]):
            print(f"  Posição {i+1}: score={item['score']:.6f}")
            print(f"    Texto (150 chars): {item['review'][:150]}...")
        if len(reviews_rankeadas) > 3:
            print(f"  ... e mais {len(reviews_rankeadas)-3} reviews.")
    print("="*60 + "\n")
    # --- FIM DA INSPEÇÃO ---

    # melhores_reviews = selecionar_melhores_reviews_distintas(resultado_pagerank)
    # imprimir_e_salvar_melhores_reviews(melhores_reviews, OUTPUT_PATH)

if __name__ == "__main__":
    main()