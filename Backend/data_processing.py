import re
from pathlib import Path
import pandas as pd

# Arte ASCII global: símbolos que não são alfanuméricos, espaços ou pontuação comum
RE_ASCII_GLOBAL = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s.,!?;:'\"()\-]")
# Arte ASCII por linha: ignora apenas alfanuméricos e espaços
RE_ASCII_LINHA = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s]")

# Template de avaliação: cada padrão com word boundary e acentos opcionais
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

# Símbolos específicos de templates visuais
RE_SIMBOLOS = re.compile(r"[🔲☑️✅●○■□()\-_=]")


# ------------------------------------------------------------
# Funções auxiliares 
# ------------------------------------------------------------
def _possui_ascii_art(texto: str) -> bool:
    """Retorna True se o texto parece conter arte ASCII."""
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


def _possui_template_avaliacao(texto: str) -> bool:
    """Retorna True se o texto contiver pelo menos 5 termos de templates de avaliação."""
    texto_lower = texto.lower()
    quantidade = 0
    for padrao in PADROES_TEMPLATE:
        if padrao.search(texto_lower):
            quantidade += 1
    return quantidade >= 5


def _possui_muitos_simbolos(texto: str) -> bool:
    """Retorna True se mais de 5% do texto são símbolos específicos de template visual."""
    if not texto:
        return False
    simbolos = RE_SIMBOLOS.findall(texto)
    return len(simbolos) / len(texto) > 0.05


# ------------------------------------------------------------
# Função principal
# ------------------------------------------------------------
def tratar_dataset(dataset_path: Path,output_path: Path,remover_vazias: bool = True) -> pd.DataFrame:

    dados = pd.read_csv(dataset_path)

    colunas_desejadas = [
        "recommendationid",
        "appid",
        "game",
        "review"
    ]
    dados = dados[colunas_desejadas]

    # Eliminação de reviews vazias
    if remover_vazias:
        mascara_valida = dados["review"].notna() & (dados["review"].str.strip() != "")
        dados = dados[mascara_valida]

    # Garantia extra (redundante se remover_vazias=True, mas seguro)
    dados = dados.dropna(subset=["review"])
    dados["review"] = dados["review"].str.strip()

    # Remove duplicatas e reviews muito curtas
    dados = dados.drop_duplicates(subset=["review"])
    dados = dados[dados["review"].str.split().str.len() >= 5]

    # Aplica os três filtros de qualidade
    dados = dados[~dados["review"].apply(_possui_ascii_art)]
    dados = dados[~dados["review"].apply(_possui_template_avaliacao)]
    dados = dados[~dados["review"].apply(_possui_muitos_simbolos)]

    # Mantém apenas jogos com no mínimo 5 reviews restantes
    quantidade_reviews = dados.groupby("appid").size()
    jogos_validos = quantidade_reviews[quantidade_reviews >= 5].index
    dados = dados[dados["appid"].isin(jogos_validos)]

    # Salva o dataset limpo
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dados.to_csv(output_path, index=False)

    return dados