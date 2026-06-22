import re
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from excecoes import DataProcessingError

# Ativa a barra de progresso para o apply
tqdm.pandas(desc="Filtros de qualidade")

# Expressões regulares pré‑compiladas
RE_ASCII_GLOBAL = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s.,!?;:'\"()\-]")
RE_ASCII_LINHA = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s]")

PADROES_TEMPLATE = [
    re.compile(r"\bgr[aá]ficos\b"),
    re.compile(r"\brequisitos\b"),
    re.compile(r"\bhist[óo]rias?\b"),
    re.compile(r"\bjogabilidade\b"),
    re.compile(r"\bcomplexidade\b"),
    re.compile(r"\bdificuldade\b"),
    re.compile(r"\btempo de jogo\b"),
    re.compile(r"\b[áa]udio\b"),
    re.compile(r"\bbugs\b"),
    re.compile(r"\bdivers[ãa]o\b"),
    re.compile(r"\bvale a pena comprar\b"),
    re.compile(r"\bcompensa comprar\b"),
    re.compile(r"\bfator replay\b"),
    re.compile(r"\bp[úu]blico\b"),
    re.compile(r"\bcomunidade\b"),
]

RE_SIMBOLOS = re.compile(r"[🔲☑️✅●○■□()\-_=]")


# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------
def _tem_arte_ascii(texto: str) -> bool:
    if not texto:
        return False
    caracteres_arte = RE_ASCII_GLOBAL.findall(texto)
    proporcao_arte = len(caracteres_arte) / len(texto)

    linhas = texto.split("\n")
    linhas_com_muitos_simbolos = 0
    for linha in linhas:
        if len(linha) > 10:
            simbolos = RE_ASCII_LINHA.findall(linha)
            if len(simbolos) / len(linha) > 0.5:
                linhas_com_muitos_simbolos += 1
    return proporcao_arte > 0.20 or linhas_com_muitos_simbolos >= 3


def _tem_template_avaliacao(texto: str) -> bool:
    texto_min = texto.lower()
    quantidade = 0
    for padrao in PADROES_TEMPLATE:
        if padrao.search(texto_min):
            quantidade += 1
    return quantidade >= 5


def _tem_muitos_simbolos(texto: str) -> bool:
    if not texto:
        return False
    simbolos = RE_SIMBOLOS.findall(texto)
    return len(simbolos) / len(texto) > 0.05


def _contem_frase_copypasta(texto: str) -> bool:
    return "eu sou um pai de" in texto.lower()


# ------------------------------------------------------------
# Função principal
# ------------------------------------------------------------
def limpar_e_filtrar_dataset(caminho_dataset: Path, caminho_saida: Path, min_palavras: int = 5, min_reviews_por_jogo: int = 10) -> tuple[pd.DataFrame, dict]:
    """
    Limpa e filtra o dataset de reviews, removendo automaticamente
    reviews nulas ou strings vazias.

    Parâmetros:
        caminho_dataset      : caminho do CSV bruto.
        caminho_saida        : onde gravar o dataset limpo.
        min_palavras         : número mínimo de palavras por review.
        min_reviews_por_jogo : quantidade mínima de reviews para manter o jogo.

    Retorna:
        (DataFrame limpo, dicionário {appid: nome_do_jogo})
    """
    if not Path(caminho_dataset).exists():
        raise DataProcessingError(f"Arquivo de dataset não encontrado: {caminho_dataset}")

    try:
        dados = pd.read_csv(caminho_dataset)
    except Exception as e:
        raise DataProcessingError(f"Erro ao ler o dataset: {e}") from e

    colunas = ["recommendationid", "appid", "game", "review"]
    dados = dados[colunas]

    # Filtra reviews que não são nulas e que, após strip, não ficam vazias
    mascara = dados["review"].notna() & (dados["review"].str.strip() != "")
    dados = dados[mascara]

    # Remove qualquer NaN ainda presente na coluna "review" (redundância segura)
    dados = dados.dropna(subset=["review"])

    # Limpa espaços em branco do início e do fim de todas as reviews
    dados["review"] = dados["review"].str.strip()

    # Elimina reviews com exatamente o mesmo texto
    dados = dados.drop_duplicates(subset=["review"])

    # Mantém apenas reviews que possuem pelo menos 'min_palavras' palavras
    dados = dados[dados["review"].str.split().str.len() >= min_palavras]

    # Filtro combinado
    def _aprovado(texto: str) -> bool:
        if _tem_arte_ascii(texto):
            return False
        if _tem_template_avaliacao(texto):
            return False
        if _tem_muitos_simbolos(texto):
            return False
        if _contem_frase_copypasta(texto):
            return False
        return True

    dados = dados[dados["review"].progress_apply(_aprovado)]

    # Mantém apenas jogos com número suficiente de reviews
    contagem = dados.groupby("appid").size()
    jogos_validos = contagem[contagem >= min_reviews_por_jogo].index
    dados = dados[dados["appid"].isin(jogos_validos)]

    # Grava o resultado
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    try:
        dados.to_csv(caminho_saida, index=False)
    except Exception as e:
        raise DataProcessingError(f"Falha ao gravar dataset limpo: {e}") from e

    if dados.empty:
        raise DataProcessingError("Nenhuma review restante após a limpeza e filtragem")

    appid_para_jogo = dict(zip(dados["appid"], dados["game"]))
    return dados, appid_para_jogo