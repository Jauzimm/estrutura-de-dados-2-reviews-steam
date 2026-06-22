from pathlib import Path
from data_processing import tratar_dataset
from nlp_processing import tratar_reviews_com_spacy
from graph_pagerank import aplicar_pagerank_reviews
from review_selection import selecionar_melhores_reviews_distintas, salvar_melhores_reviews_json

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Backend" / "results" / "reviews_resumidas.json"


def main() -> None:
    # 1° Tratar o dataset (limpeza e filtragem)
    dados_tratados = tratar_dataset(DATASET_PATH, CLEAN_DATASET_PATH)

    # Prepara mapeamento appid -> nome do jogo (para o JSON final)
    appid_para_jogo = dict(zip(dados_tratados["appid"], dados_tratados["game"]))

    # 2° Processar as reviews com spaCy para obter vetores médios por jogo
    reviews_por_jogo = tratar_reviews_com_spacy(dados_tratados)

    # 3° PageRank
    pagerank_resultado = aplicar_pagerank_reviews(reviews_por_jogo, threshold=0.3, d=0.85)

    # 4° Selecionar melhores reviews distintas
    melhores_reviews = selecionar_melhores_reviews_distintas(pagerank_resultado,reviews_por_jogo,limiar_similaridade=0.8)

    # 5° Salvar resultado em JSON
    salvar_melhores_reviews_json(melhores_reviews, OUTPUT_PATH, appid_para_jogo)

    print(f"Resultado salvo em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()