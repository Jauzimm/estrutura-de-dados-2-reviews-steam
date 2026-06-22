import re
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# Ativa a barra de progresso nos applys
tqdm.pandas(desc="Filtros de qualidade")

# Arte ASCII global
RE_ASCII_GLOBAL = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s.,!?;:'\"()\-]")
RE_ASCII_LINHA = re.compile(r"[^a-zA-ZÀ-ÿ0-9\s]")

# Template de avaliação
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

# Símbolos de template visual
RE_SIMBOLOS = re.compile(r"[🔲☑️✅●○■□()\-_=]")

# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------
def _possui_ascii_art(texto: str) -> bool:
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
    texto_lower = texto.lower()
    quantidade = 0
    for padrao in PADROES_TEMPLATE:
        if padrao.search(texto_lower):
            quantidade += 1
    return quantidade >= 5


def _possui_muitos_simbolos(texto: str) -> bool:
    if not texto:
        return False
    simbolos = RE_SIMBOLOS.findall(texto)
    return len(simbolos) / len(texto) > 0.05


def _contem_frase_copypasta(texto: str) -> bool:
    """Retorna True se o texto contém a frase típica de copypasta 'eu sou um pai de'."""
    return "eu sou um pai de" in texto.lower()


def _remover_copypastas(dados: pd.DataFrame, limiar: float = 0.85) -> pd.DataFrame:
    """Remove reviews quase duplicadas dentro de cada jogo (Jaccard)."""
    mascaras_remover = []
    for appid, grupo in dados.groupby("appid"):
        itens = []
        for idx, texto in zip(grupo.index, grupo["review"]):
            palavras = set(texto.lower().split())
            itens.append((idx, texto, palavras))
        itens.sort(key=lambda x: len(x[2]), reverse=True)
        sets_aceitos = []
        for idx, texto, palavras in itens:
            duplicado = False
            for aceito in sets_aceitos:
                intersecao = palavras & aceito
                uniao = palavras | aceito
                jaccard = len(intersecao) / len(uniao) if uniao else 0
                if jaccard >= limiar:
                    duplicado = True
                    break
            if duplicado:
                mascaras_remover.append(idx)
            else:
                sets_aceitos.append(palavras)
    return dados.drop(index=mascaras_remover)


# ------------------------------------------------------------
# Função principal
# ------------------------------------------------------------
def tratar_dataset(dataset_path: Path, output_path: Path, remover_vazias: bool = True) -> pd.DataFrame:
    dados = pd.read_csv(dataset_path)
    colunas_desejadas = ["recommendationid", "appid", "game", "review"]
    dados = dados[colunas_desejadas]

    if remover_vazias:
        mascara_valida = dados["review"].notna() & (dados["review"].str.strip() != "")
        dados = dados[mascara_valida]

    dados = dados.dropna(subset=["review"])
    dados["review"] = dados["review"].str.strip()
    dados = dados.drop_duplicates(subset=["review"])
    dados = dados[dados["review"].str.split().str.len() >= 5]

    # Filtro combinado (inclui agora a detecção da frase proibida)
    def _filtro_combinado(texto: str) -> bool:
        if _possui_ascii_art(texto):
            return False
        if _possui_template_avaliacao(texto):
            return False
        if _possui_muitos_simbolos(texto):
            return False
        if _contem_frase_copypasta(texto):   # <-- novo filtro
            return False
        return True

    dados = dados[dados["review"].progress_apply(_filtro_combinado)]

    # Remoção de copypastas genéricas (Jaccard)
    dados = _remover_copypastas(dados, limiar=0.85)

    # Mantém jogos com pelo menos 5 reviews
    quantidade_reviews = dados.groupby("appid").size()
    jogos_validos = quantidade_reviews[quantidade_reviews >= 10].index
    dados = dados[dados["appid"].isin(jogos_validos)]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    dados.to_csv(output_path, index=False)
    return dados