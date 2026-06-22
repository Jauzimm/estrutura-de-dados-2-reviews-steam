from pathlib import Path
import pandas as pd
import re


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "Dataset" / "dataset_steamreview_ptbr.csv"
CLEAN_DATASET_PATH = BASE_DIR / "Backend" / "results" / "dataset_steamreview_limpo.csv"
OUTPUT_PATH = BASE_DIR / "Frontend" / "reviews_resumidas.json"


def possui_ascii_art(texto: str) -> bool:
    if len(texto) == 0:
        return False

    caracteres_arte = re.findall(
        r"[^a-zA-ZÀ-ÿ0-9\s.,!?;:'\"()\-]",
        texto
    )

    proporcao_arte = len(caracteres_arte) / len(texto)

    linhas = texto.split("\n")

    linhas_com_muitos_simbolos = 0

    for linha in linhas:
        if len(linha) > 10:
            simbolos = re.findall(
                r"[^a-zA-ZÀ-ÿ0-9\s]",
                linha
            )

            if len(simbolos) / len(linha) > 0.5:
                linhas_com_muitos_simbolos += 1

    return (
        proporcao_arte > 0.25
        or linhas_com_muitos_simbolos >= 3
    )


def possui_template_avaliacao(texto: str) -> bool:
    texto = texto.lower()

    padroes = [
        r"gráficos",
        r"graficos",
        r"requisitos",
        r"história",
        r"historia",
        r"jogabilidade",
        r"complexidade",
        r"dificuldade",
        r"tempo de jogo",
        r"áudio",
        r"audio",
        r"bugs",
        r"diversão",
        r"diversao",
        r"vale a pena comprar",
        r"compensa comprar",
        r"fator replay",
        r"publico",
        r"comunidade",
    ]

    quantidade = 0

    for padrao in padroes:
        if re.search(padrao, texto):
            quantidade += 1

    return quantidade >= 4


def possui_muitos_simbolos(texto: str) -> bool:
    if len(texto) == 0:
        return False

    simbolos = re.findall(
        r"[🔲☑️✅●○■□()\-_=]",
        texto
    )

    return len(simbolos) / len(texto) > 0.05


def tratar_dataset(dataset_path: Path, output_path: Path) -> pd.DataFrame:

    colunas_desejadas = [
        "recommendationid",
        "appid",
        "game",
        "review"
    ]

    dados = pd.read_csv(dataset_path)

    dados = dados[colunas_desejadas]

    dados = dados.dropna(subset=["review"])

    dados["review"] = dados["review"].str.strip()

    dados = dados.drop_duplicates(subset=["review"])

    dados = dados[
        dados["review"].str.split().str.len() >= 5
    ]

    dados = dados[
        ~dados["review"].apply(possui_ascii_art)
    ]

    dados = dados[
        ~dados["review"].apply(possui_template_avaliacao)
    ]

    dados = dados[
        ~dados["review"].apply(possui_muitos_simbolos)
    ]

    quantidade_reviews = dados.groupby("appid").size()

    jogos_validos = quantidade_reviews[
        quantidade_reviews >= 5
    ].index

    dados = dados[
        dados["appid"].isin(jogos_validos)
    ]

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dados.to_csv(
        output_path,
        index=False
    )

    return dados


def tratar_reviews_com_spacy(dados: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def aplicar_pagerank_reviews(dados_tratados: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def selecionar_melhores_reviews_distintas(resultado_pagerank: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError()


def imprimir_e_salvar_melhores_reviews(
    melhores_reviews: pd.DataFrame,
    output_path: Path
) -> None:
    raise NotImplementedError()


def main() -> None:

    dados_tratados = tratar_dataset(
        DATASET_PATH,
        CLEAN_DATASET_PATH
    )

    # dados_tratados = tratar_reviews_com_spacy(dados_tratados)

    # resultado_pagerank = aplicar_pagerank_reviews(
    #     dados_tratados
    # )

    # melhores_reviews = selecionar_melhores_reviews_distintas(
    #     resultado_pagerank
    # )

    # imprimir_e_salvar_melhores_reviews(
    #     melhores_reviews,
    #     OUTPUT_PATH
    # )


if __name__ == "__main__":
    main()