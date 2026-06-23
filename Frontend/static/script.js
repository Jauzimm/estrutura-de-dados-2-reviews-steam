// Estado global
let allGames = [];
let activeIndex = -1; // índice da sugestão ativa (navegação por teclado)

// Elementos DOM
const searchInput = document.getElementById("search-input");
const suggestionsEl = document.getElementById("suggestions");
const clearBtn = document.getElementById("clear-btn");
const resultsSection = document.getElementById("results");
const gameTitleEl = document.getElementById("game-title");
const gameAppidEl = document.getElementById("game-appid");
const reviewsCountEl = document.getElementById("reviews-count");
const reviewsListEl = document.getElementById("reviews-list");
const appContainer = document.getElementById("app-container");

// Inicialização — carrega a lista de jogos
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch("/api/games");
        allGames = await res.json();
    } catch (err) {
        console.error("Erro ao carregar lista de jogos:", err);
    }
});

// Pesquisa e autocomplete
searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim().toLowerCase();

    // Mostrar/esconder botão limpar
    toggleClearBtn(query.length > 0);

    if (query.length === 0) {
        hideSuggestions();
        return;
    }

    // Filtra jogos que contenham o texto digitado
    const matches = allGames.filter((g) =>
        g.game.toLowerCase().includes(query)
    );

    renderSuggestions(matches, query);
});

// Navegação por teclado
searchInput.addEventListener("keydown", (e) => {
    const items = suggestionsEl.querySelectorAll("li");

    if (items.length === 0) return;

    if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
        updateActive(items);
    } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
        updateActive(items);
    } else if (e.key === "Enter") {
        e.preventDefault();
        if (activeIndex >= 0 && items[activeIndex]) {
            items[activeIndex].click();
        }
    } else if (e.key === "Escape") {
        hideSuggestions();
        searchInput.blur();
    }
});

// Fecha sugestões ao clicar fora
document.addEventListener("click", (e) => {
    if (!e.target.closest("#search-wrapper")) {
        hideSuggestions();
    }
});

// Botão limpar
clearBtn.addEventListener("click", () => {
    searchInput.value = "";
    toggleClearBtn(false);
    hideSuggestions();
    hideResults();
    searchInput.focus();
});

// Renderização das sugestões

function renderSuggestions(games, query) {
    suggestionsEl.innerHTML = "";
    activeIndex = -1;

    if (games.length === 0) {
        const li = document.createElement("li");
        li.className = "no-match";
        li.style.color = "var(--text-muted)";
        li.style.cursor = "default";
        li.textContent = "Nenhum jogo encontrado";
        suggestionsEl.appendChild(li);
        showSuggestions();
        return;
    }

    games.forEach((game) => {
        const li = document.createElement("li");

        // Texto com destaque no trecho correspondente
        const nameSpan = document.createElement("span");
        nameSpan.innerHTML = highlightMatch(game.game, query);

        const appidSpan = document.createElement("span");
        appidSpan.className = "appid-tag";
        appidSpan.textContent = `#${game.appid}`;

        li.appendChild(nameSpan);
        li.appendChild(appidSpan);

        li.addEventListener("click", () => selectGame(game));
        suggestionsEl.appendChild(li);
    });

    showSuggestions();
}

function highlightMatch(text, query) {
    const idx = text.toLowerCase().indexOf(query);
    if (idx === -1) return escapeHtml(text);

    const before = text.slice(0, idx);
    const match = text.slice(idx, idx + query.length);
    const after = text.slice(idx + query.length);

    return `${escapeHtml(before)}<span class="match-highlight">${escapeHtml(match)}</span>${escapeHtml(after)}`;
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function updateActive(items) {
    items.forEach((item, i) => {
        item.classList.toggle("active", i === activeIndex);
    });

    // Scroll into view
    if (items[activeIndex]) {
        items[activeIndex].scrollIntoView({ block: "nearest" });
    }
}

function showSuggestions() {
    suggestionsEl.classList.remove("hidden");
}

function hideSuggestions() {
    suggestionsEl.classList.add("hidden");
    activeIndex = -1;
}

function toggleClearBtn(show) {
    clearBtn.classList.toggle("hidden", !show);
}

// Seleção do jogo e exibição de reviews
async function selectGame(game) {
    searchInput.value = game.game;
    hideSuggestions();

    try {
        const res = await fetch(`/api/game/${game.appid}`);
        const data = await res.json();

        if (data.error) {
            console.error(data.error);
            return;
        }

        renderResults(data);
    } catch (err) {
        console.error("Erro ao buscar reviews:", err);
    }
}

function renderResults(data) {
    // Muda layout para topo
    appContainer.classList.remove("centered");
    appContainer.classList.add("top-aligned");

    // Header do jogo
    gameTitleEl.textContent = data.game;
    gameAppidEl.textContent = `AppID: ${data.appid}`;

    const count = data.top_reviews.length;
    reviewsCountEl.textContent = `${count} review${count !== 1 ? "s" : ""} mais relevante${count !== 1 ? "s" : ""} (por PageRank)`;

    // Lista de reviews
    reviewsListEl.innerHTML = "";

    data.top_reviews.forEach((review, index) => {
        const card = document.createElement("div");
        card.className = "review-card";

        // Header do card
        const header = document.createElement("div");
        header.className = "review-card-header";

        // Rank
        const rankDiv = document.createElement("div");
        rankDiv.className = "review-rank";

        const rankNum = document.createElement("div");
        rankNum.className = "rank-number";
        rankNum.textContent = `${index + 1}`;

        const rankLabel = document.createElement("span");
        rankLabel.className = "rank-label";
        rankLabel.textContent = `Review #${index + 1}`;

        rankDiv.appendChild(rankNum);
        rankDiv.appendChild(rankLabel);

        // Score
        const scoreDiv = document.createElement("div");
        scoreDiv.className = "review-score";

        const scoreLabel = document.createElement("span");
        scoreLabel.className = "score-label";
        scoreLabel.textContent = "Score";

        const scoreValue = document.createElement("span");
        scoreValue.className = "score-value";
        scoreValue.textContent = review.score.toFixed(6);

        scoreDiv.appendChild(scoreLabel);
        scoreDiv.appendChild(scoreValue);

        header.appendChild(rankDiv);
        header.appendChild(scoreDiv);

        // Texto da review
        const textDiv = document.createElement("div");
        textDiv.className = "review-text";
        textDiv.textContent = review.review;

        card.appendChild(header);
        card.appendChild(textDiv);

        // Se o texto for longo, adicionar collapse
        if (review.review.length > 500) {
            textDiv.classList.add("collapsed");

            const expandBtn = document.createElement("button");
            expandBtn.className = "expand-btn";
            expandBtn.textContent = "Ler mais ▾";

            expandBtn.addEventListener("click", () => {
                const isCollapsed = textDiv.classList.contains("collapsed");
                textDiv.classList.toggle("collapsed");
                expandBtn.textContent = isCollapsed ? "Ler menos ▴" : "Ler mais ▾";
            });

            card.appendChild(expandBtn);
        }

        reviewsListEl.appendChild(card);
    });

    // Mostra a seção de resultados
    resultsSection.classList.remove("hidden");

    // Scroll suave até os resultados
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function hideResults() {
    resultsSection.classList.add("hidden");
    appContainer.classList.remove("top-aligned");
    appContainer.classList.add("centered");
}
