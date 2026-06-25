"""Generate matchup_viewer.html from data/aki_matchups.yml."""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "aki_matchups.yml"
CHARACTER_DATA = ROOT / "data" / "aki_situation_routes.yml"
OUT = ROOT / "matchup_viewer.html"


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


def super_art_rows(items):
    if not items:
        return '<tr><td class="todo" colspan="5">TODO</td></tr>'
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<th>{h(item.get('level', 'TODO'))}</th>"
            f"<td>{h(item.get('name', 'TODO'))}</td>"
            f"<td>{h(item.get('startup', 'TODO'))}</td>"
            f"<td>{h(item.get('on_hit', 'TODO'))}</td>"
            f"<td>{h(item.get('on_block', 'TODO'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def matchup_card(character, matchup):
    matchup = matchup or {}
    tags = matchup.get("tags", ["未入力"])
    super_arts = matchup.get("super_arts", [])
    super_art_search = " ".join(
        " ".join(
            [
                item.get("level", ""),
                item.get("name", ""),
                item.get("startup", ""),
                item.get("on_hit", ""),
                item.get("on_block", ""),
            ]
        )
        for item in super_arts
    )
    search_text = " ".join(
        [
            character,
            " ".join(tags),
            matchup.get("overview", ""),
            " ".join(matchup.get("watch_out", [])),
            " ".join(matchup.get("punish", [])),
            " ".join(matchup.get("effective_options", [])),
            super_art_search,
            matchup.get("notes", ""),
        ]
    )
    return f"""
    <article class="matchup-card" data-character="{h(character)}" data-search="{h(search_text)}">
      <div class="card-head">
        <h2>{h(character)}</h2>
        <div class="tags">{badges(tags)}</div>
      </div>

      <section class="block overview">
        <h3>方針</h3>
        <p>{h(matchup.get("overview", "TODO"))}</p>
      </section>

      <div class="grid">
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

      <section class="block supers">
        <h3>スーパーアーツ</h3>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>SA</th>
                <th>技名</th>
                <th>発生</th>
                <th>ヒット後</th>
                <th>ガード後</th>
              </tr>
            </thead>
            <tbody>{super_art_rows(super_arts)}</tbody>
          </table>
        </div>
      </section>

      <section class="block notes">
        <h3>備考</h3>
        <p>{h(matchup.get("notes", "TODO"))}</p>
      </section>
    </article>
    """


def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    character_data = yaml.safe_load(CHARACTER_DATA.read_text(encoding="utf-8"))
    characters = character_data.get("characters", [])
    matchup_by_character = {
        matchup["character"]: matchup for matchup in data.get("matchups", [])
    }
    cards = "\n".join(
        matchup_card(character, matchup_by_character.get(character))
        for character in characters
    )
    options = "\n".join(
        f'<option value="{h(character)}">{h(character)}</option>'
        for character in characters
    )

    html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A.K.I. Knowledge Base - キャラ対</title>
  <style>
    :root {{
      --bg: #111820;
      --panel: #18222d;
      --soft: #202c38;
      --ink: #eef4f8;
      --muted: #9aa8b5;
      --line: #31404f;
      --accent: #59b7c8;
      --danger: #dc5b5b;
      --good: #4ec28b;
      --warn: #e0a35b;
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

    .header-inner, main, .search-panel {{
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

    label {{
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    input, select, button {{
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 7px;
      background: #111820;
      color: var(--ink);
      font: inherit;
      font-size: 14px;
    }}

    input, select {{
      width: 100%;
      padding: 0 12px;
    }}

    button {{
      padding: 0 12px;
      background: var(--soft);
      font-weight: 800;
      cursor: pointer;
    }}

    main {{
      padding: 22px 20px 42px;
    }}

    .matchup-card {{
      margin-bottom: 16px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
      overflow: hidden;
    }}

    .matchup-card[hidden] {{
      display: none;
    }}

    .card-head {{
      display: grid;
      gap: 10px;
      padding: 16px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #202c38 0%, #18222d 100%);
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

    .overview h3 {{ color: var(--accent); }}
    .danger h3 {{ color: var(--danger); }}
    .punish h3 {{ color: var(--warn); }}
    .options h3 {{ color: var(--good); }}
    .supers h3 {{ color: #cfa9ff; }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin: 0 16px;
    }}

    .grid .block {{
      margin: 0 0 14px;
    }}

    p {{
      margin: 0;
      padding: 12px 14px 14px;
      color: #d0dae3;
      font-size: 14px;
      line-height: 1.55;
      white-space: pre-wrap;
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

    .table-wrap {{
      overflow-x: auto;
    }}

    table {{
      width: 100%;
      min-width: 760px;
      border-collapse: collapse;
      font-size: 13px;
    }}

    th, td {{
      padding: 9px 10px;
      border-bottom: 1px solid var(--line);
      color: #d0dae3;
      text-align: left;
      vertical-align: top;
    }}

    thead th {{
      background: #17212c;
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }}

    tbody th {{
      width: 54px;
      color: #f2e7ff;
      white-space: nowrap;
    }}

    tbody tr:last-child th,
    tbody tr:last-child td {{
      border-bottom: 0;
    }}

    .todo {{
      color: var(--muted);
    }}

    .search-side {{
      display: flex;
      flex-direction: column;
      justify-content: end;
      gap: 6px;
      min-width: 118px;
    }}

    #matchupCount {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-align: right;
    }}

    @media (max-width: 720px) {{
      .search-box,
      .grid {{
        grid-template-columns: 1fr;
      }}

      #matchupCount {{
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

      .grid {{
        margin: 0 12px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <h1>A.K.I. Knowledge Base</h1>
      <p class="meta">キャラ対 / {h(data.get("version", "TODO"))}</p>
      <nav class="page-tabs" aria-label="ページ切替">
        <a href="news_viewer.html">お知らせ</a>
        <a href="situation_viewer.html">通常技組み合わせ</a>
        <a class="active" href="matchup_viewer.html">キャラ対</a>
      </nav>
    </div>
  </header>
  <div class="search-panel">
    <div class="search-box">
      <div>
        <label for="matchupSearch">検索</label>
        <input id="matchupSearch" type="search" placeholder="例: ケン ラッシュ 確反">
      </div>
      <div>
        <label for="characterFilter">キャラ</label>
        <select id="characterFilter">
          <option value="">すべて</option>
          {options}
        </select>
      </div>
      <div class="search-side">
        <span id="matchupCount"></span>
        <button id="clearSearch" type="button">クリア</button>
      </div>
    </div>
  </div>
  <main>
    {cards}
  </main>
  <script>
    const input = document.getElementById("matchupSearch");
    const characterFilter = document.getElementById("characterFilter");
    const count = document.getElementById("matchupCount");
    const clear = document.getElementById("clearSearch");
    const cards = Array.from(document.querySelectorAll(".matchup-card"));

    function normalize(value) {{
      return value.toLowerCase().replace(/\\s+/g, " ").trim();
    }}

    function applySearch() {{
      const terms = normalize(input.value).split(" ").filter(Boolean);
      const character = characterFilter.value;
      let visible = 0;

      for (const card of cards) {{
        const matchedKeyword = terms.every((term) => normalize(card.dataset.search || card.textContent).includes(term));
        const matchedCharacter = !character || card.dataset.character === character;
        const matched = matchedKeyword && matchedCharacter;
        card.hidden = !matched;
        if (matched) visible += 1;
      }}

      count.textContent = `${{visible}} / ${{cards.length}}件`;
    }}

    input.addEventListener("input", applySearch);
    characterFilter.addEventListener("change", applySearch);
    clear.addEventListener("click", () => {{
      input.value = "";
      characterFilter.value = "";
      input.focus();
      applySearch();
    }});
    applySearch();
  </script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"generated: {OUT}")


if __name__ == "__main__":
    main()
