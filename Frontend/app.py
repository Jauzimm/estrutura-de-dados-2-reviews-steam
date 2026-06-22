import json
import re
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Caminho para o JSON gerado pelo pipeline de processamento
JSON_PATH = Path(__file__).resolve().parent.parent / "Backend" / "results" / "reviews_resumidas.json"

# Carrega os dados uma vez ao iniciar
with open(JSON_PATH, "r", encoding="utf-8") as f:
    GAMES_DATA = json.load(f)


def limpar_tags_steam(texto: str) -> str:
    """Remove tags de formatação da Steam como [b], [i], [h1], [list], etc."""
    # Remove tags Steam no formato [tag]...[/tag] mantendo o conteúdo
    texto = re.sub(r"\[/?\w+\]", "", texto)
    # Remove [*] (marcadores de lista)
    texto = re.sub(r"\[\*\]", "• ", texto)
    # Remove espaços múltiplos
    texto = re.sub(r"  +", " ", texto)
    return texto.strip()


@app.route("/")
def index():
    """Página principal com a barra de pesquisa."""
    return render_template("index.html")


@app.route("/api/games")
def api_games():
    """Retorna a lista de todos os jogos (appid + nome) para o autocomplete."""
    games_list = [{"appid": g["appid"], "game": g["game"]} for g in GAMES_DATA]
    return jsonify(games_list)


@app.route("/api/game/<int:appid>")
def api_game(appid: int):
    """Retorna os dados completos de um jogo pelo appid, com reviews limpas."""
    for game in GAMES_DATA:
        if game["appid"] == appid:
            cleaned_reviews = []
            for r in game.get("top_reviews", []):
                cleaned_reviews.append({
                    "review": limpar_tags_steam(r["review"]),
                    "score": r["score"],
                })
            return jsonify({
                "appid": game["appid"],
                "game": game["game"],
                "top_reviews": cleaned_reviews,
            })
    return jsonify({"error": "Jogo não encontrado"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
