"""Generate viewer.html from data/aki_normals.yml."""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "aki_normals.yml"
RULES = ROOT / "data" / "rules.yml"
OUT = ROOT / "viewer.html"

GROUPS = [
    ("light", "弱技", ["5LP", "2LP", "5LK", "2LK"]),
    ("medium", "中技", ["5MP", "2MP", "5MK", "2MK"]),
    ("heavy", "強技", ["5HP", "2HP", "5HK", "2HK"]),
]


def h(value):
    return escape(str(value or ""))


def list_items(items):
    if not items:
        return '<li class="todo">TODO</li>'
    return "\n".join(f"<li>{h(item)}</li>" for item in items)


def cancel_label(move):
    source = move.get("cancel", {}).get("source_code", "")
    return source if source else "なし/TODO"


def format_frame(value, signed=False):
    text = str(value or "TODO")
    if text == "TODO" or text == "":
        return "TODO"
    if text == "D":
        return "D"
    if text.startswith("着地後"):
        number = text.removeprefix("着地後")
        return f"着地後{number}F" if number else text
    if signed and text.lstrip("-").isdigit():
        number = int(text)
        return f"{number:+d}F"
    if text.lstrip("-").isdigit():
        return f"{text}F"
    if "-" in text and all(part.isdigit() for part in text.split("-", 1)):
        return f"{text}F"
    return text


def range_cards(move, rules, outcome):
    ranges = rules["normal_case_tree"]["outcomes"][outcome]["ranges"]
    frame_key = "on_block" if outcome == "block" else "on_hit"
    frame_label = "ガード時" if outcome == "block" else "ヒット時"
    cards = []
    for key in ("close", "mid", "tip"):
        item = ranges[key]
        cards.append(
            f"""
            <div class="range-card">
              <div class="range-head">
                <span>{h(item["label"])}</span>
                <strong>{frame_label} {h(format_frame(move.get(frame_key, "TODO"), signed=True))}</strong>
              </div>
              <p>{h(item["action"])}</p>
            </div>
            """
        )
    return "\n".join(cards)


def move_card(move, rules):
    cases = move.get("cases", {})
    uses = move.get("main_use", [])
    return f"""
    <article class="move-card" id="{h(move["id"])}">
      <div class="move-top">
        <div>
          <p class="move-id">{h(move["id"])}</p>
          <h3>{h(move["name"])}</h3>
        </div>
        <span class="range-pill">{h(move.get("range", "TODO"))}</span>
      </div>

      <div class="info-block">
        <div class="stat"><span>発生</span><strong>{h(format_frame(move.get("startup", "TODO")))}</strong></div>
        <div class="stat"><span>持続</span><strong>{h(format_frame(move.get("active", "TODO")))}</strong></div>
        <div class="stat"><span>硬直</span><strong>{h(format_frame(move.get("recovery", "TODO")))}</strong></div>
        <div class="stat"><span>ヒット</span><strong>{h(format_frame(move.get("on_hit", "TODO"), signed=True))}</strong></div>
        <div class="stat"><span>ガード</span><strong>{h(format_frame(move.get("on_block", "TODO"), signed=True))}</strong></div>
        <div class="stat"><span>キャンセル</span><strong>{h(cancel_label(move))}</strong></div>
      </div>

      <div class="use-row">
        {"".join(f'<span>{h(item)}</span>' for item in uses)}
      </div>

      <div class="case-grid">
        <section class="case-block whiff">
          <h4>空振り</h4>
          <ul>{list_items(cases.get("whiff", []))}</ul>
        </section>

        <section class="case-block block">
          <h4>ガードさせた場合</h4>
          <ul>{list_items(cases.get("block", []))}</ul>
          <div class="range-grid">
            {range_cards(move, rules, "block")}
          </div>
        </section>

        <section class="case-block hit">
          <h4>ヒットした場合</h4>
          <ul>{list_items(cases.get("hit", []))}</ul>
          <div class="range-grid">
            {range_cards(move, rules, "hit")}
          </div>
        </section>
      </div>
    </article>
    """


def build_group(slug, label, moves, rules):
    cards = "\n".join(move_card(move, rules) for move in moves)
    return f"""
    <section id="{slug}" class="group {slug}">
      <div class="group-head">
        <span></span>
        <h2>{h(label)}</h2>
      </div>
      <div class="moves">
        {cards}
      </div>
    </section>
    """


def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    rules = yaml.safe_load(RULES.read_text(encoding="utf-8"))
    by_id = {move["id"]: move for move in data.get("normals", [])}

    groups = []
    for slug, label, ids in GROUPS:
        moves = [by_id[move_id] for move_id in ids if move_id in by_id]
        groups.append(build_group(slug, label, moves, rules))

    html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A.K.I. Knowledge Base - 通常技カード</title>
  <style>
    :root {{
      --bg: #111820;
      --panel: #18222d;
      --panel-soft: #202c38;
      --ink: #eef4f8;
      --muted: #9aa8b5;
      --line: #31404f;
      --light: #d8a83f;
      --medium: #48a982;
      --heavy: #dc5b5b;
      --whiff: #7b8794;
      --block: #6ea8fe;
      --hit: #4ec28b;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: system-ui, "Meiryo", sans-serif;
      background: var(--bg);
      color: var(--ink);
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

    .header-inner {{
      max-width: 1180px;
      margin: 0 auto;
    }}

    h1 {{
      margin: 0 0 4px;
      font-size: 21px;
      line-height: 1.25;
    }}

    .meta {{
      margin: 0 0 14px;
      color: var(--muted);
      font-size: 13px;
    }}

    .page-tabs,
    .section-nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .page-tabs {{
      margin-bottom: 10px;
    }}

    .page-tabs a,
    .section-nav a {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      min-height: 34px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel-soft);
      color: var(--ink);
      text-decoration: none;
      font-size: 14px;
      font-weight: 700;
    }}

    .page-tabs a {{
      border-color: #c8d3dd;
      background: #16202a;
    }}

    .page-tabs a.active {{
      border-color: var(--accent);
      background: #173845;
      color: #d7f7ff;
    }}

    .section-nav a::before, .group-head span {{
      content: "";
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--light);
    }}

    .section-nav a[href="#medium"]::before, .medium .group-head span {{ background: var(--medium); }}
    .section-nav a[href="#heavy"]::before, .heavy .group-head span {{ background: var(--heavy); }}

    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 22px 20px 42px;
    }}

    .group {{
      margin-bottom: 26px;
    }}

    .group-head {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }}

    h2 {{
      margin: 0;
      font-size: 18px;
    }}

    .moves {{
      display: grid;
      gap: 14px;
    }}

    .move-card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
      overflow: hidden;
    }}

    .move-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #202c38 0%, #18222d 100%);
    }}

    .move-id {{
      margin: 0 0 3px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0;
    }}

    h3 {{
      margin: 0;
      font-size: 18px;
    }}

    .range-pill {{
      flex: 0 0 auto;
      padding: 5px 9px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: #dce6ee;
      background: #111820;
      font-size: 12px;
      font-weight: 700;
    }}

    .info-block {{
      display: grid;
      grid-template-columns: repeat(6, minmax(88px, 1fr));
      gap: 1px;
      background: var(--line);
      border-bottom: 1px solid var(--line);
    }}

    .stat {{
      min-height: 68px;
      padding: 11px 12px;
      background: #151f29;
    }}

    .stat span {{
      display: block;
      margin-bottom: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }}

    .stat strong {{
      font-size: 20px;
      line-height: 1;
    }}

    .use-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 12px 16px 0;
    }}

    .use-row span {{
      padding: 4px 8px;
      border-radius: 999px;
      background: #263444;
      color: #d8e4ec;
      font-size: 12px;
      font-weight: 700;
    }}

    .case-grid {{
      display: grid;
      grid-template-columns: minmax(180px, 0.8fr) minmax(260px, 1.1fr) minmax(260px, 1.1fr);
      gap: 12px;
      padding: 14px 16px 16px;
    }}

    .case-block {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #141e28;
      overflow: hidden;
    }}

    .case-block h4 {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 0;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      font-size: 14px;
    }}

    .case-block h4::before {{
      content: "";
      width: 8px;
      height: 8px;
      border-radius: 999px;
      background: var(--whiff);
    }}

    .block h4::before {{ background: var(--block); }}
    .hit h4::before {{ background: var(--hit); }}

    ul {{
      margin: 0;
      padding: 10px 12px 10px 28px;
    }}

    li {{
      margin: 0 0 5px;
      color: #d0dae3;
      font-size: 13px;
    }}

    .todo {{
      color: var(--muted);
    }}

    .range-grid {{
      display: grid;
      gap: 8px;
      padding: 0 10px 10px;
    }}

    .range-card {{
      border: 1px solid #dde4ec;
      border-radius: 7px;
      background: #18222d;
      overflow: hidden;
    }}

    .range-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 8px 9px;
      background: #202c38;
      border-bottom: 1px solid #31404f;
    }}

    .range-head span {{
      font-size: 13px;
      font-weight: 800;
    }}

    .range-head strong {{
      padding: 2px 6px;
      border-radius: 6px;
      background: #111820;
      color: #e8f3f8;
      font-size: 12px;
    }}

    .range-card p {{
      margin: 0;
      padding: 8px 9px 9px;
      color: #c7d2dc;
      font-size: 13px;
      line-height: 1.5;
    }}

    @media (max-width: 980px) {{
      .info-block {{
        grid-template-columns: repeat(3, minmax(88px, 1fr));
      }}

      .case-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 560px) {{
      header {{
        padding: 14px;
      }}

      main {{
        padding: 14px;
      }}

      .move-top {{
        align-items: flex-start;
        flex-direction: column;
      }}

      .info-block {{
        grid-template-columns: repeat(2, minmax(88px, 1fr));
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <h1>A.K.I. Knowledge Base</h1>
      <p class="meta">通常技カード / {h(data.get("version", "TODO"))}</p>
      <nav class="page-tabs" aria-label="ページ切替">
        <a class="active" href="viewer.html">通常技カード</a>
        <a href="situation_viewer.html">通常技組み合わせ</a>
        <a href="matchup_viewer.html">キャラ対</a>
        <a href="submit_viewer.html">投稿</a>
      </nav>
      <nav class="section-nav" aria-label="通常技カテゴリ">
        <a href="#light">弱技</a>
        <a href="#medium">中技</a>
        <a href="#heavy">強技</a>
      </nav>
    </div>
  </header>
  <main>
    {"".join(groups)}
  </main>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"generated: {OUT}")


if __name__ == "__main__":
    main()
