"""Generate situation_viewer.html from data/aki_situation_routes.yml."""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "aki_situation_routes.yml"
OUT = ROOT / "situation_viewer.html"


def h(value):
    return escape(str(value or ""))


def list_items(items):
    if not items:
        return '<li class="todo">TODO</li>'
    return "\n".join(f"<li>{h(item)}</li>" for item in items)


def badge_items(items):
    if not items:
        return '<span class="todo">TODO</span>'
    return "".join(f"<span>{h(item)}</span>" for item in items)


def route_card(route):
    premise = route.get("premise", {})
    route_body = route.get("route", {})
    effective_characters = route.get("effective_characters", [])
    return f"""
    <article class="route-card" id="{h(route.get("id", ""))}" data-characters="{h(" ".join(effective_characters))}" data-search="{h(" ".join([
        route.get("title", ""),
        route.get("status", ""),
        " ".join(route.get("tags", [])),
        premise.get("situation", ""),
        premise.get("range", ""),
        premise.get("opponent_stance", ""),
        premise.get("poison_state", ""),
        " ".join(route.get("effective_characters", [])),
        route_body.get("notation", ""),
        route_body.get("goal", ""),
        " ".join(route.get("merits", [])),
        " ".join(route.get("demerits", [])),
        route.get("remarks", ""),
    ]))}">
      <div class="route-head">
        <div>
          <p class="status">{h(route.get("status", "TODO"))}</p>
          <h2>{h(route.get("title", "TODO"))}</h2>
        </div>
        <div class="tags">{badge_items(route.get("tags", []))}</div>
      </div>

      <section class="premise block">
        <h3>前提</h3>
        <div class="premise-grid">
          <div><span>状況</span><strong>{h(premise.get("situation", "TODO"))}</strong></div>
          <div><span>距離</span><strong>{h(premise.get("range", "TODO"))}</strong></div>
          <div><span>相手姿勢</span><strong>{h(premise.get("opponent_stance", "TODO"))}</strong></div>
          <div><span>毒状態</span><strong>{h(premise.get("poison_state", "TODO"))}</strong></div>
        </div>
      </section>

      <section class="character-block block">
        <h3>有効キャラ</h3>
        <div class="character-tags">{badge_items(route.get("effective_characters", []))}</div>
      </section>

      <section class="route-main block">
        <h3>内容</h3>
        <p class="notation">{h(route_body.get("notation", "TODO"))}</p>
        <p class="goal">{h(route_body.get("goal", "TODO"))}</p>
      </section>

      <div class="matchup-grid">
        <section class="block merits">
          <h3>メリット</h3>
          <ul>{list_items(route.get("merits", []))}</ul>
        </section>
        <section class="block demerits">
          <h3>デメリット</h3>
          <ul>{list_items(route.get("demerits", []))}</ul>
        </section>
      </div>

      <section class="block remarks">
        <h3>備考</h3>
        <p>{h(route.get("remarks", "TODO"))}</p>
      </section>
    </article>
    """


def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    cards = "\n".join(route_card(route) for route in data.get("routes", []))
    character_options = "\n".join(
        f'<option value="{h(character)}">{h(character)}</option>'
        for character in data.get("characters", [])
    )
    html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A.K.I. Knowledge Base - 通常技組み合わせ</title>
  <style>
    :root {{
      --bg: #111820;
      --panel: #18222d;
      --soft: #202c38;
      --ink: #eef4f8;
      --muted: #9aa8b5;
      --line: #31404f;
      --accent: #59b7c8;
      --good: #4ec28b;
      --bad: #dc5b5b;
      --merit: #6ea8fe;
      --demerit: #e0a35b;
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

    .header-inner, main {{
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

    .page-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .page-tabs a {{
      min-height: 34px;
      display: inline-flex;
      align-items: center;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--soft);
      color: var(--ink);
      text-decoration: none;
      font-size: 14px;
      font-weight: 700;
    }}

    .page-tabs a.active {{
      border-color: var(--accent);
      background: #173845;
      color: #d7f7ff;
    }}

    .search-panel {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 14px 20px 0;
    }}

    .search-box {{
      display: grid;
      grid-template-columns: 1fr minmax(180px, 240px) auto;
      gap: 10px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.24);
    }}

    .search-box label {{
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    .search-box input,
    .search-box select {{
      width: 100%;
      min-height: 40px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 7px;
      color: var(--ink);
      background: #111820;
      font: inherit;
      font-size: 14px;
    }}

    .search-box input:focus,
    .search-box select:focus {{
      outline: 2px solid rgba(31, 122, 140, 0.24);
      border-color: var(--accent);
    }}

    .search-side {{
      display: flex;
      flex-direction: column;
      justify-content: end;
      gap: 6px;
      min-width: 118px;
    }}

    #searchCount {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-align: right;
    }}

    #clearSearch {{
      min-height: 40px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: var(--soft);
      color: var(--ink);
      font: inherit;
      font-size: 14px;
      font-weight: 800;
      cursor: pointer;
    }}

    .route-card[hidden] {{
      display: none;
    }}

    main {{
      padding: 22px 20px 42px;
    }}

    .route-card {{
      margin-bottom: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
      overflow: hidden;
    }}

    .route-head {{
      display: grid;
      gap: 10px;
      padding: 16px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #202c38 0%, #18222d 100%);
    }}

    .status {{
      margin: 0 0 4px;
      color: var(--accent);
      font-size: 12px;
      font-weight: 800;
    }}

    h2 {{
      margin: 0;
      font-size: 17px;
      line-height: 1.35;
    }}

    .tags {{
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-start;
      gap: 6px;
    }}

    .tags span {{
      padding: 4px 8px;
      border-radius: 999px;
      background: #173845;
      color: #d7f7ff;
      font-size: 12px;
      font-weight: 800;
    }}

    .character-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      padding: 12px;
      background: #151f29;
    }}

    .character-tags span {{
      padding: 5px 9px;
      border: 1px solid #315466;
      border-radius: 999px;
      background: #173845;
      color: #d7f7ff;
      font-size: 12px;
      font-weight: 800;
    }}

    .block {{
      margin: 14px 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #141e28;
      overflow: hidden;
    }}

    .block h3 {{
      margin: 0;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: #202c38;
      font-size: 14px;
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
      font-size: 15px;
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

    .goal {{
      margin: 0;
      padding: 0 14px 14px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.55;
    }}

    .matchup-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin: 0 16px;
    }}

    .matchup-grid .block {{
      margin: 0 0 14px;
    }}

    .good h3 {{ color: var(--good); }}
    .bad h3 {{ color: var(--bad); }}
    .merits h3 {{ color: var(--merit); }}
    .demerits h3 {{ color: var(--demerit); }}

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

    h4 {{
      margin: 0;
      padding: 10px 12px 0;
      font-size: 14px;
    }}

    .remarks p {{
      margin: 0;
      padding: 12px 14px 14px;
      color: #d0dae3;
      font-size: 14px;
      line-height: 1.55;
      white-space: pre-wrap;
    }}

    .todo {{
      color: var(--muted);
    }}

    @media (max-width: 720px) {{
      .premise-grid,
      .matchup-grid {{
        grid-template-columns: 1fr;
      }}

      .search-box {{
        grid-template-columns: 1fr;
      }}

      .search-side {{
        min-width: 0;
      }}

      #searchCount {{
        text-align: left;
      }}
    }}

    @media (max-width: 520px) {{
      header {{
        padding: 14px 14px;
      }}

      .search-panel {{
        padding: 12px 14px 0;
      }}

      main {{
        padding: 18px 14px 34px;
      }}

      .page-tabs a {{
        flex: 1 1 100%;
        justify-content: center;
      }}

      .block {{
        margin: 12px 12px;
      }}

      .matchup-grid {{
        margin: 0 12px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <h1>A.K.I. Knowledge Base</h1>
      <p class="meta">通常技組み合わせ / {h(data.get("version", "TODO"))}</p>
      <nav class="page-tabs" aria-label="ページ切替">
        <a href="news_viewer.html">お知らせ</a>
        <a class="active" href="situation_viewer.html">通常技組み合わせ</a>
        <a href="matchup_viewer.html">キャラ対</a>
      </nav>
    </div>
  </header>
  <div class="search-panel">
    <div class="search-box">
      <div>
        <label for="routeSearch">検索</label>
        <input id="routeSearch" type="search" placeholder="例: ケン 6F 投げ抜け 2中K パリィ">
      </div>
      <div>
        <label for="characterFilter">有効キャラ</label>
        <select id="characterFilter">
          <option value="">すべて</option>
          {character_options}
        </select>
      </div>
      <div class="search-side">
        <span id="searchCount"></span>
        <button id="clearSearch" type="button">クリア</button>
      </div>
    </div>
  </div>
  <main>
    {cards}
  </main>
  <script>
    const input = document.getElementById("routeSearch");
    const characterFilter = document.getElementById("characterFilter");
    const clear = document.getElementById("clearSearch");
    const count = document.getElementById("searchCount");
    const cards = Array.from(document.querySelectorAll(".route-card"));

    function normalize(value) {{
      return value.toLowerCase().replace(/\\s+/g, " ").trim();
    }}

    function applySearch() {{
      const terms = normalize(input.value).split(" ").filter(Boolean);
      const character = characterFilter.value;
      let visible = 0;

      for (const card of cards) {{
        const haystack = normalize(card.dataset.search || card.textContent);
        const characters = card.dataset.characters || "";
        const matchedKeyword = terms.every((term) => haystack.includes(term));
        const matchedCharacter = !character || characters.split(" ").includes(character);
        const matched = matchedKeyword && matchedCharacter;
        card.hidden = !matched;
        if (matched) visible += 1;
      }}

      count.textContent = `${{visible}} / ${{cards.length}}件`;
    }}

    input.addEventListener("input", applySearch);
    clear.addEventListener("click", () => {{
      input.value = "";
      characterFilter.value = "";
      input.focus();
      applySearch();
    }});
    characterFilter.addEventListener("change", applySearch);
    applySearch();
  </script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"generated: {OUT}")


if __name__ == "__main__":
    main()
