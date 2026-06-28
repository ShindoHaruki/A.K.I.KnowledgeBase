"""Generate single-page index.html for the A.K.I. knowledge base."""

from html import escape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
NEWS = ROOT / "data" / "news.yml"
MATCHUPS = ROOT / "data" / "aki_matchups.yml"
ROUTES = ROOT / "data" / "aki_situation_routes.yml"
TECHNIQUES = ROOT / "data" / "techniques.yml"
REFERENCE_TABLES = ROOT / "data" / "reference_tables.yml"
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


def super_art_rows(items):
    if not items:
        return '<tr><td class="todo" colspan="5">TODO</td></tr>'
    rows = []
    for item in items:
        level = item.get('level', 'TODO')
        level_class = str(level).lower()
        rows.append(
            "<tr>"
            f'<th class="sa-level {h(level_class)}">{h(level)}</th>'
            f"<td>{h(item.get('name', 'TODO'))}</td>"
            f"<td>{h(item.get('startup', 'TODO'))}</td>"
            f"<td>{h(item.get('on_hit', 'TODO'))}</td>"
            f"<td>{h(item.get('on_block', 'TODO'))}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def youtube_embed_url(url):
    parsed = urlparse(url or "")
    host = parsed.netloc.lower().replace("www.", "")
    video_id = ""

    if host in {"youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif parsed.path.startswith("/shorts/") or parsed.path.startswith("/embed/"):
            video_id = parsed.path.strip("/").split("/", 1)[1]
    elif host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]

    if not video_id:
        return ""
    return f"https://www.youtube.com/embed/{h(video_id)}"


def google_sheet_embed_url(table):
    embed_url = table.get("embed_url", "")
    if embed_url and embed_url != "TODO":
        return embed_url

    url = table.get("spreadsheet_url", "")
    parsed = urlparse(url or "")
    host = parsed.netloc.lower().replace("www.", "")
    if host != "docs.google.com" or "/spreadsheets/d/" not in parsed.path:
        return ""

    parts = parsed.path.split("/")
    try:
        sheet_id = parts[parts.index("d") + 1]
    except (ValueError, IndexError):
        return ""

    query = parse_qs(parsed.query)
    gid = query.get("gid", [""])[0]
    suffix = f"?gid={gid}&rm=minimal" if gid else "?rm=minimal"
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/preview{suffix}"


def reference_items(items):
    if not items:
        return '<p class="todo-text">TODO</p>'

    rendered = []
    for item in items:
        title = item.get("title", "参考資料") if isinstance(item, dict) else "参考資料"
        url = item.get("url", "") if isinstance(item, dict) else str(item)
        note = item.get("note", "") if isinstance(item, dict) else ""
        embed_url = youtube_embed_url(url)
        link = (
            f'<a href="{h(url)}" target="_blank" rel="noopener noreferrer">{h(title)}</a>'
            if url and url != "TODO"
            else f"<span>{h(title)}</span>"
        )
        embed = (
            f'<div class="video-frame"><iframe src="{embed_url}" title="{h(title)}" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            "allowfullscreen></iframe></div>"
            if embed_url
            else ""
        )
        rendered.append(
            f"""
            <div class="reference-item">
              {link}
              <p>{h(note)}</p>
              {embed}
            </div>
            """
        )
    return "\n".join(rendered)


def table_items(tables):
    if not tables:
        return '<p class="todo-text">TODO</p>'

    rendered = []
    for table in tables:
        title = table.get("title", "参考表")
        sheet_name = table.get("sheet_name", "")
        url = table.get("spreadsheet_url", "")
        note = table.get("note", "")
        embed_url = google_sheet_embed_url(table)
        sheet_label = f'<span class="sheet-name">{h(sheet_name)}</span>' if sheet_name else ""
        link = (
            f'<a href="{h(url)}" target="_blank" rel="noopener noreferrer">別タブで開く</a>'
            if url and url != "TODO"
            else ""
        )
        embed = (
            f'<div class="sheet-frame"><iframe src="{h(embed_url)}" title="{h(title)}" loading="lazy"></iframe></div>'
            if embed_url
            else '<p class="todo-text">埋め込みURLまたはGoogle Sheets URLを追加すると表を表示できます。</p>'
        )
        rendered.append(
            f"""
            <section class="reference-table">
              <div class="reference-table-head">
                <h3>{h(title)}</h3>
                <div class="reference-links">{sheet_label}{link}</div>
              </div>
              <p>{h(note)}</p>
              {embed}
            </section>
            """
        )
    return "\n".join(rendered)


def reference_theme(item, index):
    theme = item.get("theme", "テーマ")
    description = item.get("description", "")
    tables = item.get("tables", [])
    search = " ".join(
        [
            theme,
            description,
            " ".join(
                " ".join(
                    [
                        table.get("title", ""),
                        table.get("sheet_name", ""),
                        table.get("spreadsheet_url", ""),
                        table.get("note", ""),
                    ]
                )
                for table in tables
            ),
        ]
    )
    hidden = "" if index == 0 else " hidden"
    return f"""
      <article class="reference-card" data-reference-panel="{index}" data-search="{h(search)}"{hidden}>
        <div class="card-head">
          <h2>{h(theme)}</h2>
        </div>
        <section class="block overview">
          <h3>概要</h3>
          <p>{h(description or "TODO")}</p>
        </section>
        <section class="block references">
          <h3>表</h3>
          {table_items(tables)}
        </section>
      </article>
    """


def news_item(item):
    tags = " ".join(item.get("tags", []))
    published_at = " ".join(
        part for part in [item.get("date", ""), item.get("time", "")] if part
    )
    search = " ".join(
        [
            item.get("date", ""),
            item.get("time", ""),
            item.get("category", ""),
            item.get("title", ""),
            item.get("body", ""),
            tags,
        ]
    )
    return f"""
      <article class="news-item" data-search="{h(search)}">
        <div class="news-meta">
          <span>{h(published_at)}</span>
          <strong>{h(item.get("category", "お知らせ"))}</strong>
        </div>
        <h2>{h(item.get("title", "お知らせ"))}</h2>
        <p>{h(item.get("body", ""))}</p>
      </article>
    """.strip()


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
    search = " ".join(
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


def technique_card(item):
    search = " ".join(
        [
            item.get("title", ""),
            item.get("summary", ""),
            " ".join(item.get("merits", [])),
            " ".join(item.get("demerits", [])),
            " ".join(
                " ".join(
                    [
                        ref.get("title", ""),
                        ref.get("url", ""),
                        ref.get("note", ""),
                    ]
                )
                for ref in item.get("references", [])
                if isinstance(ref, dict)
            ),
            item.get("notes", ""),
        ]
    )
    return f"""
      <article class="technique-card" data-search="{h(search)}">
        <div class="card-head">
          <h2>{h(item.get("title", "TODO"))}</h2>
        </div>
        <section class="block overview">
          <h3>概要</h3>
          <p>{h(item.get("summary", "TODO"))}</p>
        </section>
        <div class="two-grid">
          <section class="block merits">
            <h3>メリット</h3>
            <ul>{list_items(item.get("merits", []))}</ul>
          </section>
          <section class="block demerits">
            <h3>デメリット</h3>
            <ul>{list_items(item.get("demerits", []))}</ul>
          </section>
        </div>
        <section class="block references">
          <h3>参考資料</h3>
          {reference_items(item.get("references", []))}
        </section>
        <section class="block notes">
          <h3>備考</h3>
          <p>{h(item.get("notes", "TODO"))}</p>
        </section>
      </article>
    """


def main():
    news_data = yaml.safe_load(NEWS.read_text(encoding="utf-8"))
    matchup_data = yaml.safe_load(MATCHUPS.read_text(encoding="utf-8"))
    route_data = yaml.safe_load(ROUTES.read_text(encoding="utf-8"))
    technique_data = yaml.safe_load(TECHNIQUES.read_text(encoding="utf-8"))
    reference_data = yaml.safe_load(REFERENCE_TABLES.read_text(encoding="utf-8"))

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
    technique_items = technique_data.get("items", [])
    technique_html = "\n".join(technique_card(item) for item in technique_items)
    if not technique_html:
        technique_html = """
      <article class="empty-state">
        <h2>テクニックはまだ登録されていません</h2>
        <p>件名、概要、メリット、デメリット、参考資料、備考をそろえて追加していきます。</p>
      </article>
        """
    reference_items_data = reference_data.get("items", [])
    reference_tabs = "\n".join(
        f'<button class="{"" if index else "active"}" type="button" data-reference-tab="{index}">{h(item.get("theme", "テーマ"))}</button>'
        for index, item in enumerate(reference_items_data)
    )
    reference_html = "\n".join(
        reference_theme(item, index) for index, item in enumerate(reference_items_data)
    )
    if not reference_html:
        reference_html = """
      <article class="empty-state">
        <h2>参考資料はまだ登録されていません</h2>
        <p>テーマごとに確認したい表を追加していきます。</p>
      </article>
        """

    html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A.K.I. Knowledge Base</title>
  <style>
    :root {{
      --bg: #0f1319;
      --panel: #19212c;
      --soft: #222b38;
      --ink: #eef4f8;
      --muted: #a8b4c2;
      --line: #3a4658;
      --accent: #b56dff;
      --accent-soft: #35234d;
      --poison: #8bdc5c;
      --venom: #d957b8;
      --gold: #e7bf62;
      --danger: #ef6b7a;
      --good: #72d988;
      --warn: #e4b65b;
      --merit: #77a8ff;
      --glow-purple: rgba(181, 109, 255, 0.22);
      --glow-green: rgba(139, 220, 92, 0.16);
      --glow-rose: rgba(217, 87, 184, 0.16);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: system-ui, "Meiryo", sans-serif;
      background:
        radial-gradient(circle at 16% 8%, var(--glow-purple), transparent 34%),
        radial-gradient(circle at 82% 16%, var(--glow-green), transparent 30%),
        radial-gradient(circle at 48% 100%, var(--glow-rose), transparent 36%),
        linear-gradient(180deg, #10141b 0%, #121722 44%, #0d1218 100%);
      background-attachment: fixed;
      color: var(--ink);
      line-height: 1.5;
    }}

    body::before {{
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: -1;
      background:
        linear-gradient(120deg, transparent 0 28%, rgba(139, 220, 92, 0.055) 34%, transparent 45%),
        linear-gradient(30deg, transparent 0 58%, rgba(181, 109, 255, 0.07) 64%, transparent 76%);
      opacity: 0.9;
    }}

    header {{
      position: sticky;
      top: 0;
      z-index: 10;
      padding: 16px 20px;
      background: rgba(15, 19, 25, 0.9);
      border-bottom: 1px solid var(--line);
      box-shadow: 0 2px 22px rgba(0, 0, 0, 0.34), 0 0 30px rgba(181, 109, 255, 0.08);
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
      background: linear-gradient(135deg, rgba(181, 109, 255, 0.28), rgba(139, 220, 92, 0.16));
      color: #f5edff;
    }}

    main {{
      padding: 22px 20px 42px;
    }}

    .view[hidden],
    .news-item[hidden],
    .route-card[hidden],
    .matchup-card[hidden],
    .technique-card[hidden],
    .reference-card[hidden] {{
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

    .tool-box.simple-tools {{
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
      background: #10151d;
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
    .matchup-card,
    .empty-state,
    .technique-card,
    .reference-card {{
      position: relative;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: linear-gradient(180deg, rgba(31, 40, 53, 0.96), rgba(22, 29, 39, 0.98));
      overflow: hidden;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.035);
    }}

    .news-item::before,
    .route-card::before,
    .matchup-card::before,
    .empty-state::before,
    .technique-card::before,
    .reference-card::before {{
      content: "";
      display: block;
      height: 3px;
      background: linear-gradient(90deg, var(--accent), var(--poison), var(--gold), var(--venom));
    }}

    .news-item::before {{ background: linear-gradient(90deg, var(--gold), var(--venom)); }}
    .technique-card::before {{ background: linear-gradient(90deg, var(--poison), var(--accent)); }}
    .reference-card::before {{ background: linear-gradient(90deg, #58c7ff, var(--gold)); }}
    .route-card::before {{ background: linear-gradient(90deg, var(--venom), var(--poison)); }}
    .matchup-card::before {{ background: linear-gradient(90deg, var(--accent), var(--danger), var(--gold)); }}
    }}

    .news-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(90deg, rgba(231, 191, 98, 0.12), rgba(217, 87, 184, 0.08));
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    .news-meta strong,
    .tags span,
    .character-tags span {{
      padding: 3px 7px;
      border-radius: 999px;
      background: rgba(181, 109, 255, 0.18);
      color: #f1e8ff;
      font-size: 12px;
      font-weight: 800;
    }}

    .tags span:nth-child(4n + 1),
    .character-tags span:nth-child(4n + 1) {{
      background: rgba(181, 109, 255, 0.22);
      color: #f4e9ff;
    }}

    .tags span:nth-child(4n + 2),
    .character-tags span:nth-child(4n + 2) {{
      background: rgba(139, 220, 92, 0.18);
      color: #eaffdd;
    }}

    .tags span:nth-child(4n + 3),
    .character-tags span:nth-child(4n + 3) {{
      background: rgba(217, 87, 184, 0.18);
      color: #ffe5f7;
    }}

    .tags span:nth-child(4n),
    .character-tags span:nth-child(4n) {{
      background: rgba(231, 191, 98, 0.18);
      color: #fff1c7;
    }}

    .news-item h2,
    .empty-state h2,
    .card-head h2 {{
      margin: 0;
      padding: 12px 14px 4px;
      color: var(--ink);
      font-size: 17px;
      line-height: 1.35;
    }}

    .news-item p,
    .empty-state p,
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
      background: linear-gradient(135deg, rgba(34, 43, 56, 0.96), rgba(53, 35, 77, 0.72));
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
      background: rgba(16, 21, 29, 0.72);
    }}

    .block {{
      margin: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(18, 25, 34, 0.88);
      overflow: hidden;
    }}

    .block h3 {{
      margin: 0;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(90deg, rgba(34, 43, 56, 0.94), rgba(34, 43, 56, 0.55));
      font-size: 14px;
    }}

    .view[data-view="news"] .summary,
    .news-item h2 {{ color: var(--gold); }}
    .view[data-view="techniques"] .summary,
    .technique-card .card-head h2 {{ color: var(--poison); }}
    .view[data-view="references"] .summary,
    .reference-card .card-head h2 {{ color: #7ed9ff; }}
    .view[data-view="routes"] .summary,
    .route-card .card-head h2 {{ color: var(--venom); }}
    .view[data-view="matchups"] .summary,
    .matchup-card .card-head h2 {{ color: #d9c1ff; }}

    .overview h3 {{ color: var(--accent); }}
    .danger h3 {{ color: var(--danger); }}
    .punish h3 {{ color: var(--warn); }}
    .options h3,
    .merits h3 {{ color: var(--good); }}
    .demerits h3 {{ color: var(--warn); }}
    .supers h3 {{ color: #cfa9ff; }}

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
      background: linear-gradient(180deg, #202a38, #17212c);
      color: var(--muted);
      font-size: 12px;
      white-space: nowrap;
    }}

    tbody th {{
      width: 54px;
      color: #f2e7ff;
      white-space: nowrap;
    }}

    .sa-level {{
      border-left: 3px solid var(--accent);
      font-weight: 900;
    }}

    .sa-level.sa1 {{
      color: #f4e9ff;
      background: rgba(181, 109, 255, 0.16);
      border-left-color: var(--accent);
    }}

    .sa-level.sa2 {{
      color: #eaffdd;
      background: rgba(139, 220, 92, 0.14);
      border-left-color: var(--poison);
    }}

    .sa-level.sa3 {{
      color: #fff0c4;
      background: rgba(231, 191, 98, 0.15);
      border-left-color: var(--gold);
    }}

    tbody tr:last-child th,
    tbody tr:last-child td {{
      border-bottom: 0;
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

    .todo-text {{
      margin: 0;
      padding: 12px 14px 14px;
      color: var(--muted);
      font-size: 14px;
    }}

    .reference-item {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
    }}

    .reference-item:last-child {{
      border-bottom: 0;
    }}

    .reference-item a,
    .reference-item span {{
      color: #d7f7ff;
      font-size: 14px;
      font-weight: 800;
    }}

    .reference-item p {{
      margin: 5px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }}

    .video-frame {{
      margin-top: 10px;
      aspect-ratio: 16 / 9;
      width: 100%;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #080c10;
    }}

    .video-frame iframe {{
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
    }}

    .reference-nav {{
      display: flex;
      gap: 8px;
      margin-bottom: 14px;
      flex-wrap: wrap;
    }}

    .reference-nav button {{
      min-height: 34px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--soft);
      color: var(--ink);
      font: inherit;
      font-size: 14px;
      font-weight: 800;
      cursor: pointer;
    }}

    .reference-nav button.active {{
      border-color: var(--accent);
      background: var(--accent-soft);
      color: #d7f7ff;
    }}

    .reference-table {{
      border-bottom: 1px solid var(--line);
    }}

    .reference-table:last-child {{
      border-bottom: 0;
    }}

    .reference-table-head {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      padding: 12px 14px 4px;
    }}

    .reference-table-head h3 {{
      margin: 0;
      padding: 0;
      border: 0;
      background: transparent;
      color: var(--ink);
    }}

    .reference-links {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      font-size: 13px;
      font-weight: 800;
    }}

    .reference-links a {{
      color: #d7f7ff;
    }}

    .sheet-name {{
      padding: 3px 7px;
      border-radius: 999px;
      background: var(--accent-soft);
      color: #d7f7ff;
    }}

    .sheet-frame {{
      height: min(72vh, 720px);
      min-height: 420px;
      margin: 10px 14px 14px;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #080c10;
    }}

    .sheet-frame iframe {{
      width: 100%;
      height: 100%;
      border: 0;
      display: block;
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
      .tool-box.simple-tools,
      .two-grid,
      .premise-grid {{
        grid-template-columns: 1fr;
      }}

      .summary {{
        align-items: flex-start;
        flex-direction: column;
      }}

      .reference-table-head {{
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
      <p class="meta">お知らせ / テクニック / 参考資料 / 通常技組み合わせ / キャラ対</p>
      <p class="site-notice">時間を見つけて開発しながら随時更新しています。AIと共同開発しているため、表記ゆれや整理途中の内容が含まれる可能性があります。</p>
      <nav class="page-tabs" aria-label="ページ切替">
        <button class="active" type="button" data-view-button="news">お知らせ</button>
        <button type="button" data-view-button="techniques">テクニック</button>
        <button type="button" data-view-button="references">参考資料</button>
        <button type="button" data-view-button="routes">通常技組み合わせ</button>
        <button type="button" data-view-button="matchups">キャラ対</button>
      </nav>
    </div>
  </header>

  <main>
    <section class="view" data-view="news">
      <div class="summary">
        <span id="newsCount"></span>
        <span>10件ごとに表示</span>
      </div>
      <section class="news-list" aria-label="お知らせ一覧">
        {news_html}
      </section>
      <nav class="pager" id="newsPager" aria-label="お知らせページ"></nav>
    </section>

    <section class="view" data-view="techniques" hidden>
      <div class="tool-box simple-tools">
        <div>
          <label for="techniqueSearch">検索</label>
          <input id="techniqueSearch" type="search" placeholder="例: 詐欺飛び セットプレイ">
        </div>
        <button class="clear-button" id="clearTechniques" type="button">クリア</button>
      </div>
      <div class="summary"><span id="techniqueCount"></span></div>
      <section class="card-list" aria-label="テクニック一覧">
        {technique_html}
      </section>
    </section>

    <section class="view" data-view="references" hidden>
      <nav class="reference-nav" aria-label="参考資料テーマ">
        {reference_tabs}
      </nav>
      <div class="summary"><span id="referenceCount"></span></div>
      <section class="card-list" aria-label="参考資料一覧">
        {reference_html}
      </section>
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

    const newsItems = Array.from(document.querySelectorAll(".news-item"));
    const newsPager = document.getElementById("newsPager");
    const newsCount = document.getElementById("newsCount");
    let newsPage = 1;

    function filteredNews() {{
      return newsItems;
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

    const techniqueInput = document.getElementById("techniqueSearch");
    const techniqueCards = Array.from(document.querySelectorAll(".technique-card"));
    const techniqueCount = document.getElementById("techniqueCount");

    function applyTechniques() {{
      const terms = termsFrom(techniqueInput);
      let visible = 0;
      for (const card of techniqueCards) {{
        const haystack = normalize(card.dataset.search || card.textContent);
        const matched = terms.every((term) => haystack.includes(term));
        card.hidden = !matched;
        if (matched) visible += 1;
      }}
      techniqueCount.textContent = `${{visible}} / ${{techniqueCards.length}}件`;
    }}

    techniqueInput.addEventListener("input", applyTechniques);
    document.getElementById("clearTechniques").addEventListener("click", () => {{
      techniqueInput.value = "";
      techniqueInput.focus();
      applyTechniques();
    }});

    const referenceTabs = Array.from(document.querySelectorAll("[data-reference-tab]"));
    const referenceCards = Array.from(document.querySelectorAll(".reference-card"));
    const referenceCount = document.getElementById("referenceCount");

    function setReferencePanel(index) {{
      for (const card of referenceCards) {{
        card.hidden = card.dataset.referencePanel !== String(index);
      }}
      for (const button of referenceTabs) {{
        button.classList.toggle("active", button.dataset.referenceTab === String(index));
      }}
      referenceCount.textContent = `${{referenceCards.length ? 1 : 0}} / ${{referenceCards.length}}件`;
    }}

    for (const button of referenceTabs) {{
      button.addEventListener("click", () => setReferencePanel(button.dataset.referenceTab));
    }}

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
    applyTechniques();
    setReferencePanel(0);
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
