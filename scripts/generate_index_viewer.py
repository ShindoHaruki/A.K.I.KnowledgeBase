"""Generate single-page index.html for the A.K.I. knowledge base."""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
NEWS = ROOT / "data" / "news.yml"
MATCHUPS = ROOT / "data" / "aki_matchups.yml"
ROUTES = ROOT / "data" / "aki_situation_routes.yml"
OUT = ROOT / "index.html"


def h(value):
    return escape(str(value or ""))


def list_items(items):
    if not items:
        return '<li class="todo">TODO</li>'
    return "\n".join(f"<li>{h(item)}</li>" for item in items)


def badges(items):
    if not items:
        return '<span class="todo">TODO</span>'
    return "".join(f"<span>{h(item)}</span>" for item in items)


def news_item(item):
    tags = " ".join(item.get("tags", []))
    search = " ".join(
        [
            item.get("date", ""),
            item.get("category", ""),
            item.get("title", ""),
            item.get("body", ""),
            tags,
        ]
    )
    return f"""
      <article class="news-item" data-search="{h(search)}">
        <div class="news-meta">
          <span>{h(item.get("date", ""))}</span>
          <strong>{h(item.get("category", "お知らせ"))}</strong>
        </div>
        <h2>{h(item.get("title", "お知らせ"))}</h2>
        <p>{h(item.get("body", ""))}</p>
      </article>
    """


def matchup_card(character, matchup):
    matchup = matchup or {}
    tags = matchup.get("tags", ["未入力"])
    search = " ".join(
        [
            character,
            " ".join(tags),
            matchup.get("overview", ""),
            " ".join(matchup.get("watch_out", [])),
            " ".join(matchup.get("punish", [])),
            " ".join(matchup.get("effective_options", [])),
            matchup.get("notes", ""),
        ]
    )
    return f"""
      <article class="matchup-card" data-character="{h(character)}" data-search="{h(search)}">
        <div class="card-head">
          <h2>{h(character)}</h2>
          <div class="tags">{badges(tags)}</div>
        </div>
        <section class="block overview">
          <h3>方針</h3>
          <p>{h(matchup.get("overview", "TODO"))}</p>
        </section>
        <div class="two-grid">
          <section class="block danger">
            <h3>注意する行動</h3>
            <ul>{list_items(matchup.get("watch_out", []))}</ul>
          </section>
          <section class="block punish">
            <h3>確反・咎め</h3>
            <ul>{list_items(matchup.get("punish", []))}</ul>
          </section>
        </div>
        <section class="block options">
          <h3>有効な選択肢</h3>
          <ul>{list_items(matchup.get("effective_options", []))}</ul>
        </section>
        <section class="block notes">
          <h3>備考</h3>
          <p>{h(matchup.get("notes", "TODO"))}</p>
        </section>
      </article>
    """


def route_card(route):
    premise = route.get("premise", {})
    route_body = route.get("route", {})
    effective_characters = route.get("effective_characters", [])
    search = " ".join(
        [
            route.get("title", ""),
            route.get("status", ""),
            " ".join(route.get("tags", [])),
            premise.get("situation", ""),
            premise.get("range", ""),
            premise.get("opponent_stance", ""),
            premise.get("poison_state", ""),
            " ".join(effective_characters),
            route_body.get("notation", ""),
            route_body.get("goal", ""),
            " ".join(route.get("merits", [])),
            " ".join(route.get("demerits", [])),
            route.get("remarks", ""),
        ]
    )
    return f"""
      <article class="route-card" data-characters="{h(" ".join(effective_characters))}" data-search="{h(search)}">
        <div class="card-head">
          <h2>{h(route.get("title", "TODO"))}</h2>
          <div class="tags">{badges(route.get("tags", []))}</div>
        </div>
        <section class="block">
          <h3>前提</h3>
          <div class="premise-grid">
            <div><span>状況</span><strong>{h(premise.get("situation", "TODO"))}</strong></div>
            <div><span>距離</span><strong>{h(premise.get("range", "TODO"))}</strong></div>
            <div><span>相手姿勢</span><strong>{h(premise.get("opponent_stance", "TODO"))}</strong></div>
            <div><span>毒状態</span><strong>{h(premise.get("poison_state", "TODO"))}</strong></div>
          </div>
        </section>
        <section class="block">
          <h3>有効キャラ</h3>
          <div class="character-tags">{badges(effective_characters)}</div>
        </section>
        <section class="block">
          <h3>内容</h3>
          <p class="notation">{h(route_body.get("notation", "TODO"))}</p>
          <p class="goal">{h(route_body.get("goal", "TODO"))}</p>
        </section>
        <div class="two-grid">
          <section class="block merits">
            <h3>メリット</h3>
            <ul>{list_items(route.get("merits", []))}</ul>
          </section>
          <section class="block demerits">
            <h3>デメリット</h3>
            <ul>{list_items(route.get("demerits", []))}</ul>
          </section>
        </div>
        <section class="block notes">
          <h3>備考</h3>
          <p>{h(route.get("remarks", "TODO"))}</p>
        </section>
      </article>
    """


def main():
    news_data = yaml.safe_load(NEWS.read_text(encoding="utf-8"))
    matchup_data = yaml.safe_load(MATCHUPS.read_text(encoding="utf-8"))
    route_data = yaml.safe_load(ROUTES.read_text(encoding="utf-8"))

    news_html = "\n".join(news_item(item) for item in news_data.get("items", []))

    matchup_by_character = {
        matchup["character"]: matchup for matchup in matchup_data.get("matchups", [])
    }
    characters = route_data.get("characters", [])
    matchup_html = "\n".join(
        matchup_card(character, matchup_by_character.get(character))
        for character in characters
    )
    matchup_options = "\n".join(
        f'<option value="{h(character)}">{h(character)}</option>'
        for character in characters
    )

    route_html = "\n".join(route_card(route) for route in route_data.get("routes", []))
    route_options = matchup_options

    html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A.K.I. Knowledge Base</title>
  <style>
    :root {{
      --bg: #111820;
      --panel: #18222d;
      --soft: #202c38;
      --ink: #eef4f8;
      --muted: #9aa8b5;
      --line: #31404f;
      --accent: #59b7c8;
      --accent-soft: #173845;
      --danger: #dc5b5b;
      --good: #4ec28b;
      --warn: #e0a35b;
      --merit: #6ea8fe;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: system-ui, "Meiryo", sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }}

    header {{
      position: sticky;
      top: 0;
      z-index: 10;
      padding: 16px 20px;
      background: rgba(17, 24, 32, 0.94);
      border-bottom: 1px solid var(--line);
      box-shadow: 0 2px 22px rgba(0, 0, 0, 0.34);
      backdrop-filter: blur(10px);
    }}

    .header-inner,
    main {{
      max-width: 1120px;
      margin: 0 auto;
    }}

    h1 {{
      margin: 0 0 4px;
      font-size: 21px;
    }}

    .meta {{
      margin: 0 0 12px;
      color: var(--muted);
      font-size: 13px;
    }}

    .site-notice {{
      margin: 0 0 12px;
      padding: 9px 11px;
      border: 1px solid rgba(220, 91, 91, 0.45);
      border-radius: 8px;
      background: rgba(220, 91, 91, 0.12);
      color: #ff9b9b;
      font-size: 13px;
      font-weight: 800;
      line-height: 1.55;
    }}

    .page-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .page-tabs button,
    .pager button,
    .clear-button {{
      min-height: 34px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--soft);
      color: var(--ink);
      font: inherit;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
    }}

    .page-tabs button.active,
    .pager button.active {{
      border-color: var(--accent);
      background: var(--accent-soft);
      color: #d7f7ff;
    }}

    main {{
      padding: 22px 20px 42px;
    }}

    .view[hidden],
    .news-item[hidden],
    .route-card[hidden],
    .matchup-card[hidden] {{
      display: none;
    }}

    .tool-box {{
      display: grid;
      grid-template-columns: 1fr minmax(180px, 240px) auto;
      gap: 10px;
      margin-bottom: 14px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.24);
    }}

    .tool-box.news-tools {{
      grid-template-columns: 1fr auto;
    }}

    label {{
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    input,
    select {{
      width: 100%;
      min-height: 40px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #111820;
      color: var(--ink);
      font: inherit;
      font-size: 14px;
    }}

    .summary {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 800;
    }}

    .news-list,
    .card-list {{
      display: grid;
      gap: 10px;
    }}

    .news-item,
    .route-card,
    .matchup-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      overflow: hidden;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.2);
    }}

    .news-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: var(--soft);
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    .news-meta strong,
    .tags span,
    .character-tags span {{
      padding: 3px 7px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: #d7f7ff;
      font-size: 12px;
      font-weight: 800;
    }}

    .news-item h2,
    .card-head h2 {{
      margin: 0;
      padding: 12px 14px 4px;
      color: var(--ink);
      font-size: 17px;
      line-height: 1.35;
    }}

    .news-item p,
    .block p,
    .goal {{
      margin: 0;
      padding: 4px 14px 14px;
      color: #d0dae3;
      font-size: 14px;
      line-height: 1.55;
      white-space: pre-wrap;
    }}

    .card-head {{
      display: grid;
      gap: 8px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
      background: var(--soft);
    }}

    .tags,
    .character-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 0 14px;
    }}

    .character-tags {{
      padding: 12px 14px;
      background: #151f29;
    }}

    .block {{
      margin: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #141e28;
      overflow: hidden;
    }}

    .block h3 {{
      margin: 0;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: var(--soft);
      font-size: 14px;
    }}

    .overview h3 {{ color: var(--accent); }}
    .danger h3 {{ color: var(--danger); }}
    .punish h3 {{ color: var(--warn); }}
    .options h3,
    .merits h3 {{ color: var(--good); }}
    .demerits h3 {{ color: var(--warn); }}

    .two-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin: 0 14px;
    }}

    .two-grid .block {{
      margin: 0 0 12px;
    }}

    ul {{
      margin: 0;
      padding: 11px 14px 12px 30px;
    }}

    li {{
      margin-bottom: 6px;
      color: #d0dae3;
      font-size: 14px;
      line-height: 1.45;
    }}

    .premise-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(130px, 1fr));
      gap: 1px;
      background: var(--line);
    }}

    .premise-grid div {{
      padding: 12px;
      background: #151f29;
    }}

    .premise-grid span {{
      display: block;
      margin-bottom: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    .premise-grid strong {{
      font-size: 14px;
    }}

    .notation {{
      margin: 0;
      padding: 12px 14px 6px;
      font-family: Consolas, "Meiryo", monospace;
      font-size: 17px;
      font-weight: 800;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }}

    .todo {{
      color: var(--muted);
    }}

    .pager {{
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-top: 16px;
      flex-wrap: wrap;
    }}

    @media (max-width: 720px) {{
      .tool-box,
      .tool-box.news-tools,
      .two-grid,
      .premise-grid {{
        grid-template-columns: 1fr;
      }}

      .summary {{
        align-items: flex-start;
        flex-direction: column;
      }}
    }}

    @media (max-width: 520px) {{
      header {{
        padding: 14px;
      }}

      main {{
        padding: 18px 14px 34px;
      }}

      .page-tabs button {{
        flex: 1 1 100%;
        justify-content: center;
      }}

      .block {{
        margin: 12px;
      }}

      .two-grid {{
        margin: 0 12px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <h1>A.K.I. Knowledge Base</h1>
      <p class="meta">お知らせ / 通常技組み合わせ / キャラ対</p>
      <p class="site-notice">時間を見つけて開発しながら随時更新しています。AIと共同開発しているため、表記ゆれや整理途中の内容が含まれる可能性があります。</p>
      <nav class="page-tabs" aria-label="ページ切替">
        <button class="active" type="button" data-view-button="news">お知らせ</button>
        <button type="button" data-view-button="routes">通常技組み合わせ</button>
        <button type="button" data-view-button="matchups">キャラ対</button>
      </nav>
    </div>
  </header>

  <main>
    <section class="view" data-view="news">
      <div class="tool-box news-tools">
        <div>
          <label for="newsSearch">検索</label>
          <input id="newsSearch" type="search" placeholder="例: リリー 風 スパイア">
        </div>
        <button class="clear-button" id="clearNews" type="button">クリア</button>
      </div>
      <div class="summary">
        <span id="newsCount"></span>
        <span>10件ごとに表示</span>
      </div>
      <section class="news-list" aria-label="お知らせ一覧">
        {news_html}
      </section>
      <nav class="pager" id="newsPager" aria-label="お知らせページ"></nav>
    </section>

    <section class="view" data-view="routes" hidden>
      <div class="tool-box">
        <div>
          <label for="routeSearch">検索</label>
          <input id="routeSearch" type="search" placeholder="例: ケン 6F 投げ抜け">
        </div>
        <div>
          <label for="routeCharacter">有効キャラ</label>
          <select id="routeCharacter">
            <option value="">すべて</option>
            {route_options}
          </select>
        </div>
        <button class="clear-button" id="clearRoutes" type="button">クリア</button>
      </div>
      <div class="summary"><span id="routeCount"></span></div>
      <section class="card-list" aria-label="通常技組み合わせ一覧">
        {route_html}
      </section>
    </section>

    <section class="view" data-view="matchups" hidden>
      <div class="tool-box">
        <div>
          <label for="matchupSearch">検索</label>
          <input id="matchupSearch" type="search" placeholder="例: ルーク サンドブラスト">
        </div>
        <div>
          <label for="matchupCharacter">キャラ</label>
          <select id="matchupCharacter">
            <option value="">すべて</option>
            {matchup_options}
          </select>
        </div>
        <button class="clear-button" id="clearMatchups" type="button">クリア</button>
      </div>
      <div class="summary"><span id="matchupCount"></span></div>
      <section class="card-list" aria-label="キャラ対一覧">
        {matchup_html}
      </section>
    </section>
  </main>

  <script>
    const pageSize = 10;

    function normalize(value) {{
      return value.toLowerCase().replace(/\\s+/g, " ").trim();
    }}

    function termsFrom(input) {{
      return normalize(input.value).split(" ").filter(Boolean);
    }}

    function setView(name) {{
      for (const view of document.querySelectorAll("[data-view]")) {{
        view.hidden = view.dataset.view !== name;
      }}
      for (const button of document.querySelectorAll("[data-view-button]")) {{
        button.classList.toggle("active", button.dataset.viewButton === name);
      }}
    }}

    for (const button of document.querySelectorAll("[data-view-button]")) {{
      button.addEventListener("click", () => setView(button.dataset.viewButton));
    }}

    const newsInput = document.getElementById("newsSearch");
    const newsItems = Array.from(document.querySelectorAll(".news-item"));
    const newsPager = document.getElementById("newsPager");
    const newsCount = document.getElementById("newsCount");
    let newsPage = 1;

    function filteredNews() {{
      const terms = termsFrom(newsInput);
      return newsItems.filter((item) => {{
        const haystack = normalize(item.dataset.search || item.textContent);
        return terms.every((term) => haystack.includes(term));
      }});
    }}

    function renderNewsPager(pageCount) {{
      newsPager.innerHTML = "";
      if (pageCount <= 1) return;
      for (let page = 1; page <= pageCount; page += 1) {{
        const button = document.createElement("button");
        button.type = "button";
        button.textContent = page;
        button.className = page === newsPage ? "active" : "";
        button.addEventListener("click", () => {{
          newsPage = page;
          applyNews();
          window.scrollTo({{ top: 0, behavior: "smooth" }});
        }});
        newsPager.appendChild(button);
      }}
    }}

    function applyNews() {{
      const visible = filteredNews();
      const pageCount = Math.max(1, Math.ceil(visible.length / pageSize));
      newsPage = Math.min(newsPage, pageCount);
      const visibleSet = new Set(visible.slice((newsPage - 1) * pageSize, newsPage * pageSize));
      for (const item of newsItems) item.hidden = !visibleSet.has(item);
      newsCount.textContent = `${{visible.length}} / ${{newsItems.length}}件`;
      renderNewsPager(pageCount);
    }}

    newsInput.addEventListener("input", () => {{
      newsPage = 1;
      applyNews();
    }});
    document.getElementById("clearNews").addEventListener("click", () => {{
      newsInput.value = "";
      newsPage = 1;
      newsInput.focus();
      applyNews();
    }});

    const routeInput = document.getElementById("routeSearch");
    const routeCharacter = document.getElementById("routeCharacter");
    const routeCards = Array.from(document.querySelectorAll(".route-card"));
    const routeCount = document.getElementById("routeCount");

    function applyRoutes() {{
      const terms = termsFrom(routeInput);
      const character = routeCharacter.value;
      let visible = 0;
      for (const card of routeCards) {{
        const haystack = normalize(card.dataset.search || card.textContent);
        const characters = card.dataset.characters || "";
        const matchedKeyword = terms.every((term) => haystack.includes(term));
        const matchedCharacter = !character || characters.split(" ").includes(character);
        const matched = matchedKeyword && matchedCharacter;
        card.hidden = !matched;
        if (matched) visible += 1;
      }}
      routeCount.textContent = `${{visible}} / ${{routeCards.length}}件`;
    }}

    routeInput.addEventListener("input", applyRoutes);
    routeCharacter.addEventListener("change", applyRoutes);
    document.getElementById("clearRoutes").addEventListener("click", () => {{
      routeInput.value = "";
      routeCharacter.value = "";
      routeInput.focus();
      applyRoutes();
    }});

    const matchupInput = document.getElementById("matchupSearch");
    const matchupCharacter = document.getElementById("matchupCharacter");
    const matchupCards = Array.from(document.querySelectorAll(".matchup-card"));
    const matchupCount = document.getElementById("matchupCount");

    function applyMatchups() {{
      const terms = termsFrom(matchupInput);
      const character = matchupCharacter.value;
      let visible = 0;
      for (const card of matchupCards) {{
        const haystack = normalize(card.dataset.search || card.textContent);
        const matchedKeyword = terms.every((term) => haystack.includes(term));
        const matchedCharacter = !character || card.dataset.character === character;
        const matched = matchedKeyword && matchedCharacter;
        card.hidden = !matched;
        if (matched) visible += 1;
      }}
      matchupCount.textContent = `${{visible}} / ${{matchupCards.length}}件`;
    }}

    matchupInput.addEventListener("input", applyMatchups);
    matchupCharacter.addEventListener("change", applyMatchups);
    document.getElementById("clearMatchups").addEventListener("click", () => {{
      matchupInput.value = "";
      matchupCharacter.value = "";
      matchupInput.focus();
      applyMatchups();
    }});

    applyNews();
    applyRoutes();
    applyMatchups();
  </script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"generated: {OUT}")


if __name__ == "__main__":
    main()
