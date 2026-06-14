"""Generate submit_viewer.html for route submissions."""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "aki_situation_routes.yml"
OUT = ROOT / "submit_viewer.html"


def h(value):
    return escape(str(value or ""))


def checkbox_list(characters):
    return "\n".join(
        f"""
        <label class="check-pill">
          <input type="checkbox" name="effective_characters" value="{h(character)}">
          <span>{h(character)}</span>
        </label>
        """
        for character in characters
    )


def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    characters = data.get("characters", [])
    html = f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>A.K.I. Knowledge Base - 投稿</title>
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
      background: var(--accent-soft);
      color: #d7f7ff;
    }}

    main {{
      padding: 22px 20px 42px;
    }}

    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
      gap: 16px;
      align-items: start;
    }}

    .panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.26);
      overflow: hidden;
    }}

    .panel h2 {{
      margin: 0;
      padding: 13px 15px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #202c38 0%, #18222d 100%);
      font-size: 17px;
    }}

    form {{
      padding: 14px 15px 16px;
    }}

    fieldset {{
      margin: 0 0 14px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #141e28;
    }}

    legend {{
      padding: 0 6px;
      color: #dbe5ec;
      font-size: 13px;
      font-weight: 800;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}

    label {{
      display: block;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
    }}

    input,
    textarea,
    select {{
      width: 100%;
      margin-top: 5px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 7px;
      color: var(--ink);
      background: #111820;
      font: inherit;
      font-size: 14px;
    }}

    textarea {{
      min-height: 82px;
      resize: vertical;
      line-height: 1.45;
    }}

    input:focus,
    textarea:focus,
    select:focus {{
      outline: 2px solid rgba(31, 122, 140, 0.22);
      border-color: var(--accent);
    }}

    .characters {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      margin-top: 8px;
    }}

    .check-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 5px 8px;
      border: 1px solid #315466;
      border-radius: 999px;
      background: #173845;
      color: #d7f7ff;
      font-size: 12px;
      font-weight: 800;
    }}

    .check-pill input {{
      width: auto;
      margin: 0;
    }}

    .actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    button {{
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

    button.primary {{
      border-color: var(--accent);
      background: var(--accent);
      color: #ffffff;
    }}

    button.danger {{
      color: var(--danger);
    }}

    .preview {{
      padding: 14px;
    }}

    pre {{
      min-height: 220px;
      max-height: 520px;
      margin: 0;
      padding: 12px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #0c1218;
      color: #e6edf3;
      font-family: Consolas, "Yu Gothic", monospace;
      font-size: 12px;
      line-height: 1.5;
      white-space: pre;
    }}

    .hint {{
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
    }}

    .saved-list {{
      display: grid;
      gap: 8px;
      padding: 0 14px 14px;
    }}

    .saved-item {{
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #141e28;
    }}

    .saved-item strong {{
      display: block;
      margin-bottom: 4px;
      font-size: 13px;
    }}

    .saved-item span {{
      color: var(--muted);
      font-size: 12px;
    }}

    @media (max-width: 920px) {{
      .layout,
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <h1>A.K.I. Knowledge Base</h1>
      <p class="meta">通常技組み合わせ / 投稿</p>
      <nav class="page-tabs" aria-label="ページ切替">
        <a href="viewer.html">通常技カード</a>
        <a href="situation_viewer.html">通常技組み合わせ</a>
        <a href="matchup_viewer.html">キャラ対</a>
        <a class="active" href="submit_viewer.html">投稿</a>
      </nav>
    </div>
  </header>

  <main>
    <div class="layout">
      <section class="panel">
        <h2>組み合わせを投稿</h2>
        <form id="submitForm">
          <fieldset>
            <legend>基本</legend>
            <div class="grid">
              <label>タイトル
                <input name="title" required placeholder="例: 画面端の投げ抜け狩り">
              </label>
              <label>状態
                <select name="status">
                  <option value="TODO">TODO</option>
                  <option value="検証中">検証中</option>
                  <option value="確認済み">確認済み</option>
                </select>
              </label>
              <label>タグ
                <input name="tags" placeholder="例: 画面端, 投げ抜け狩り, 暴れ潰し">
              </label>
              <label>ID
                <input name="id" placeholder="空欄ならタイトルから自動生成">
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>前提</legend>
            <div class="grid">
              <label>状況
                <input name="situation" placeholder="例: 画面端で+2Fを取った後">
              </label>
              <label>距離
                <select name="range">
                  <option value="密着">密着</option>
                  <option value="中間">中間</option>
                  <option value="先端">先端</option>
                  <option value="etc">etc</option>
                </select>
              </label>
              <label>相手姿勢
                <select name="opponent_stance">
                  <option value="立ち">立ち</option>
                  <option value="しゃがみ">しゃがみ</option>
                  <option value="どちらでも">どちらでも</option>
                </select>
              </label>
              <label>毒状態
                <select name="poison_state">
                  <option value="毒無し">毒無し</option>
                  <option value="毒あり">毒あり</option>
                  <option value="どちらでも">どちらでも</option>
                </select>
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>有効キャラ</legend>
            <div class="actions">
              <button type="button" id="selectAll">全選択</button>
              <button type="button" id="clearCharacters">解除</button>
            </div>
            <div class="characters">
              {checkbox_list(characters)}
            </div>
          </fieldset>

          <fieldset>
            <legend>内容</legend>
            <label>ルート
              <input name="notation" placeholder="例: 2中K > 5中P ...">
            </label>
            <label>狙い
              <input name="goal" placeholder="例: 投げ抜け狩り / 暴れ潰し">
            </label>
          </fieldset>

          <fieldset>
            <legend>評価</legend>
            <div class="grid">
              <label>メリット
                <textarea name="merits" placeholder="1行につき1項目"></textarea>
              </label>
              <label>デメリット
                <textarea name="demerits" placeholder="1行につき1項目"></textarea>
              </label>
            </div>
          </fieldset>

          <fieldset>
            <legend>備考</legend>
            <label>自由記述
              <textarea name="remarks" placeholder="考案者の詳細、検証ログ、注意点など"></textarea>
            </label>
          </fieldset>

          <div class="actions">
            <button class="primary" type="submit">YAML生成</button>
            <button type="button" id="saveLocal">投稿として保存</button>
            <button type="reset">入力リセット</button>
          </div>
        </form>
      </section>

      <aside class="panel">
        <h2>生成結果</h2>
        <div class="preview">
          <pre id="yamlPreview">フォームを入力して YAML生成 を押してください。</pre>
          <div class="actions" style="margin-top: 10px;">
            <button type="button" id="copyYaml">コピー</button>
            <button type="button" id="downloadYaml">YAMLダウンロード</button>
          </div>
          <p class="hint">静的HTMLのため、このページだけでは data/aki_situation_routes.yml へ直接追記しません。生成されたYAMLを確認してから取り込む運用です。</p>
        </div>
        <h2>ブラウザ内の投稿</h2>
        <div id="savedList" class="saved-list"></div>
      </aside>
    </div>
  </main>

  <script>
    const form = document.getElementById("submitForm");
    const preview = document.getElementById("yamlPreview");
    const savedList = document.getElementById("savedList");
    const storageKey = "aki-route-submissions";

    function lines(value) {{
      return String(value || "")
        .split(/\\r?\\n/)
        .map((line) => line.trim())
        .filter(Boolean);
    }}

    function csv(value) {{
      return String(value || "")
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
    }}

    function slug(value) {{
      return String(value || "route")
        .toLowerCase()
        .replace(/[^a-z0-9ぁ-んァ-ヶ一-龠ー]+/g, "-")
        .replace(/^-+|-+$/g, "")
        || `route-${{Date.now()}}`;
    }}

    function yamlQuote(value) {{
      return `"${{String(value || "TODO").replace(/\\\\/g, "\\\\\\\\").replace(/"/g, "\\\\\\"")}}"`;
    }}

    function yamlList(items, indent) {{
      if (!items.length) return `${{indent}}- "TODO"`;
      return items.map((item) => `${{indent}}- ${{yamlQuote(item)}}`).join("\\n");
    }}

    function selectedCharacters() {{
      return Array.from(form.querySelectorAll('input[name="effective_characters"]:checked'))
        .map((input) => input.value);
    }}

    function buildYaml() {{
      const data = new FormData(form);
      const title = data.get("title") || "TODO";
      const id = data.get("id") || slug(title);
      const characters = selectedCharacters();
      return `  - id: ${{yamlQuote(id)}}
    title: ${{yamlQuote(title)}}
    status: ${{yamlQuote(data.get("status") || "TODO")}}
    tags:
${{yamlList(csv(data.get("tags")), "      ")}}
    premise:
      situation: ${{yamlQuote(data.get("situation"))}}
      range: ${{yamlQuote(data.get("range"))}}
      opponent_stance: ${{yamlQuote(data.get("opponent_stance"))}}
      poison_state: ${{yamlQuote(data.get("poison_state"))}}
    effective_characters:
${{yamlList(characters, "      ")}}
    route:
      notation: ${{yamlQuote(data.get("notation"))}}
      goal: ${{yamlQuote(data.get("goal"))}}
    merits:
${{yamlList(lines(data.get("merits")), "      ")}}
    demerits:
${{yamlList(lines(data.get("demerits")), "      ")}}
    remarks: |
${{lines(data.get("remarks")).length ? lines(data.get("remarks")).map((line) => `      ${{line}}`).join("\\n") : "      TODO"}}
`;
    }}

    function refreshPreview() {{
      const yaml = buildYaml();
      preview.textContent = yaml;
      return yaml;
    }}

    function loadSaved() {{
      return JSON.parse(localStorage.getItem(storageKey) || "[]");
    }}

    function writeSaved(items) {{
      localStorage.setItem(storageKey, JSON.stringify(items));
    }}

    function renderSaved() {{
      const items = loadSaved();
      savedList.innerHTML = "";
      if (!items.length) {{
        savedList.innerHTML = '<div class="saved-item"><span>まだ投稿は保存されていません。</span></div>';
        return;
      }}
      for (const item of items) {{
        const div = document.createElement("div");
        div.className = "saved-item";
        div.innerHTML = `<strong>${{item.title}}</strong><span>${{item.createdAt}}</span>`;
        div.addEventListener("click", () => {{
          preview.textContent = item.yaml;
        }});
        savedList.appendChild(div);
      }}
    }}

    form.addEventListener("submit", (event) => {{
      event.preventDefault();
      refreshPreview();
    }});

    document.getElementById("saveLocal").addEventListener("click", () => {{
      const yaml = refreshPreview();
      const data = new FormData(form);
      const items = loadSaved();
      items.unshift({{
        title: String(data.get("title") || "TODO"),
        yaml,
        createdAt: new Date().toLocaleString(),
      }});
      writeSaved(items);
      renderSaved();
    }});

    document.getElementById("copyYaml").addEventListener("click", async () => {{
      await navigator.clipboard.writeText(preview.textContent);
    }});

    document.getElementById("downloadYaml").addEventListener("click", () => {{
      const blob = new Blob([preview.textContent], {{ type: "text/yaml" }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "aki_route_submission.yml";
      a.click();
      URL.revokeObjectURL(url);
    }});

    document.getElementById("selectAll").addEventListener("click", () => {{
      form.querySelectorAll('input[name="effective_characters"]').forEach((input) => input.checked = true);
    }});

    document.getElementById("clearCharacters").addEventListener("click", () => {{
      form.querySelectorAll('input[name="effective_characters"]').forEach((input) => input.checked = false);
    }});

    renderSaved();
  </script>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"generated: {OUT}")


if __name__ == "__main__":
    main()
