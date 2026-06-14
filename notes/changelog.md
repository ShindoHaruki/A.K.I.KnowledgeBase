# Changelog

## 2026-06-14 / news page and navigation cleanup

### Added
- `data/news.yml` を追加
- `scripts/generate_index_viewer.py` を追加
- `scripts/build_pages.py` を追加
- `index.html` を追加
- `scripts/generate_news_viewer.py` を追加
- `news_viewer.html` を追加
- `requirements.txt` を追加

### Updated
- ナビゲーションから `通常技カード` と `投稿` を一旦削除
- `お知らせ`, `通常技組み合わせ`, `キャラ対` を1つのHTML内で切り替える構成に整理
- 閲覧者向けの自然文を `data/news.yml` で管理し、10件ごとにページネーションできるようにした
- お知らせページを基準に、3ページの文字サイズ・余白・カード見出し・スマートフォン表示を調整
- 旧来の分割HTMLである `news_viewer.html`, `situation_viewer.html`, `matchup_viewer.html` を削除
- Cloudflare Pages向けに `dist/index.html` だけを公開するビルド手順を追加

### Notes
- 通常技カードと投稿フォームは復活可能なように生成スクリプトを残す
- `notes/changelog.md` は開発履歴として残し、閲覧者向けのお知らせ本文とは分けて管理する
- 現在の閲覧入口は `index.html`
- Cloudflare PagesのBuild output directoryは `dist`

## 2026-06-14 / A.K.I. matchup notes

### Updated
- `data/aki_matchups.yml` に対A.K.I.戦の対策メモを追加・整理
- `data/aki_matchups.yml` に対リリー戦の対策メモを追加
- `data/aki_matchups.yml` に対ルーク戦の対策メモを追加
- `matchup_viewer.html` にA.K.I.戦カードを反映
- キャラ対カード見出しの状態表示を非表示にし、タグをキャラ名下に並べる表示へ整理

### Notes
- 紫煙砲ジャストパリィ後の具体的な意識配分は未確定のためTODOとして保持
- Dリバ詐欺、10F詐欺、弱蛇頭鞭、OD凶襲突、BO中の弱凶襲突、近距離の5強P/6強Pと弱蛇頭鞭/紫煙砲への咎めをユーザーメモとして整理
- リリー戦は風利用スパイア、9F詐欺、Dリバ拒否、風溜め阻止、SA発生フレームをユーザーメモとして整理
- ルーク戦は中距離方針、サンドブラスト対策、強ナックル対応、サプレッサー注意、SA発生フレームをユーザーメモとして整理

## 2026-06-12 / matchup viewer

### Added
- `data/aki_matchups.yml` を追加
- `scripts/generate_matchup_viewer.py` を追加
- `matchup_viewer.html` を追加

### Updated
- 共通ヘッダーに `キャラ対` タブを追加
- キャラ別に `方針`, `注意する行動`, `確反・咎め`, `有効な選択肢`, `備考` を表示できるページを追加
- キャラ対ページにキーワード検索とキャラフィルタを追加

### Notes
- キャラ一覧は `data/aki_situation_routes.yml` の `characters` を再利用
- リュウ、ケンのみサンプル入力し、他キャラはTODOカードとして表示

## 2026-06-11 / evaluation fields

### Updated
- 通常技組み合わせの評価欄を `メリット`, `デメリット` の2項目に整理
- `有効な場面`, `無効な場面` をデータ、一覧、投稿フォームから削除

### Notes
- 既存サンプルデータからも `effective_when`, `ineffective_when` を削除

## 2026-06-11 / premise fields

### Updated
- 通常技組み合わせの前提から `有利` 欄を削除
- `距離` を `密着`, `中間`, `先端`, `etc` の固定選択に変更
- `相手状態` を `相手姿勢` に変更し、`立ち`, `しゃがみ`, `どちらでも` の固定選択に変更
- `毒状態` を追加し、`毒無し`, `毒あり`, `どちらでも` の固定選択に変更
- 投稿ページの前提入力も同じ選択形式に変更

### Notes
- 既存サンプルデータは新しい前提項目へ移行

## 2026-06-11 / dark theme

### Updated
- `viewer.html`, `situation_viewer.html`, `submit_viewer.html` を暗色テーマに変更
- カード、入力欄、検索欄、タグ、ヘッダー、パネルの白背景を暗色パレットへ変更
- 3ページの生成スクリプト側に暗色テーマを反映

### Notes
- 生成HTMLを直接ではなく `scripts/generate_*.py` 側を更新したため、再生成後も暗色テーマを維持する

## 2026-06-11 / submit viewer

### Added
- `scripts/generate_submit_viewer.py` を追加
- `submit_viewer.html` を追加

### Updated
- 通常技組み合わせの投稿フォームを追加
- 投稿フォームからYAML形式のルートデータを生成できるようにした
- 生成結果のコピー、YAMLダウンロード、ブラウザ内保存に対応
- `viewer.html` と `situation_viewer.html` の共通タブに `投稿` を追加

### Notes
- 静的HTMLのため、投稿ページ単体では `data/aki_situation_routes.yml` へ直接追記しない
- 生成されたYAMLを確認してから取り込む運用

## 2026-06-11 / unified header

### Updated
- `viewer.html` と `situation_viewer.html` のヘッダーを `A.K.I. Knowledge Base` で統一
- ページ切替を共通のタブUIとして表示
- 現在表示中のページに `active` 表示を追加
- ブラウザタブのタイトルを共通フォーマットに変更

### Notes
- 通常技カード側のみ、弱技・中技・強技のカテゴリナビをサブナビとして維持

## 2026-06-11 / combination title

### Updated
- `situation_viewer.html` の表示タイトルを `A.K.I. 通常技組み合わせ整理` に変更
- 通常技カード側のナビ文言を `通常技組み合わせ` に変更

### Notes
- ファイル名とデータ構造は既存のまま維持

## 2026-06-11 / search test route

### Added
- `data/aki_situation_routes.yml` に検索テスト用の2件目ルートを追加

### Notes
- 追加ルートは `画面端`, `投げ抜け`, `ケン` などの検索・有効キャラフィルタ確認用
- 実戦用データとしては未検証のため `TODO` と備考を残している

## 2026-06-11 / character filter

### Updated
- `situation_viewer.html` の検索欄に `有効キャラ` セレクトを追加
- キーワード検索と有効キャラフィルタのAND検索に対応
- クリアボタンでキーワードとキャラ選択を同時にリセット

### Notes
- キャラ候補は `data/aki_situation_routes.yml` の `characters` から生成

## 2026-06-11 / situation search

### Updated
- `situation_viewer.html` の最上部に検索フォームを追加
- タイトル、タグ、前提、内容、有効キャラ、有効/無効な場面、メリット/デメリット、備考を検索対象に追加
- 検索結果件数とクリアボタンを追加

### Notes
- 静的HTML内のJavaScriptで絞り込みを行う

## 2026-06-11 / situation remarks

### Updated
- 状況別ルートの `後続` 欄を削除
- `data/aki_situation_routes.yml` の `followups` を自由記述の `remarks` に変更
- `situation_viewer.html` に `備考` 欄を追加

### Notes
- 備考欄は考案者が詳細、注意点、検証ログなどを自由に書く用途

## 2026-06-11 / effective characters

### Updated
- `data/aki_situation_routes.yml` にキャラ一覧を追加
- 状況別ルートごとに `effective_characters` を持てるように更新
- `situation_viewer.html` の `前提` と `内容` の間に `有効キャラ` タグ欄を追加

### Notes
- サンプルルートは全30キャラを有効キャラとして初期入力
- ルートごとに有効キャラを絞る場合は `effective_characters` を編集する

## 2026-06-11 / situation route viewer

### Added
- `data/aki_situation_routes.yml` を追加
- `scripts/generate_situation_viewer.py` を追加
- `situation_viewer.html` を追加

### Updated
- 状況別に `前提`, `内容`, `有効な場面`, `無効な場面`, `メリット`, `デメリット`, `後続` を整理できるページを作成
- `viewer.html` のナビゲーションに `状況別ルート` へのリンクを追加

### Notes
- 入力例はサンプル/TODOとして追加し、未検証のフレームやリターンは推測で埋めていない
- 具体的なルートは `data/aki_situation_routes.yml` に追記して管理する

## 2026-06-09 / frame display format

### Updated
- `viewer.html` のフレーム表示に単位 `F` を追加
- ヒット時・ガード時のプラスフレームに `+` 記号を追加
- 表示用の整形処理を `scripts/generate_viewer.py` に追加

### Notes
- `data/aki_normals.yml` の元データは変更せず、表示側のみ整形

## 2026-06-09 / card viewer

### Updated
- `viewer.html` をSVG埋め込み表示から技カード形式に変更
- 各通常技を `基本情報`, `空振り`, `ガードさせた場合`, `ヒットした場合` のブロックで表示
- `ガードさせた場合`, `ヒットした場合` に `密着`, `中間`, `先端` の距離別カードを追加
- `viewer.html` を `data/aki_normals.yml` と `data/rules.yml` から生成する `scripts/generate_viewer.py` を追加

### Notes
- 空中技と全体表示はビューアから除外し、地上通常技のみ表示
- フレーム値と分岐内容はYAML/rulesを参照して生成

## 2026-06-09 / viewer design

### Updated
- `viewer.html` から空中技と全体表示を削除
- `viewer.html` を弱技・中技・強技の地上通常技ビューに整理
- ナビゲーション、色分け、固定見出し、余白、カード風の表示を追加
- セクション見出しが本文に重ならないよう固定表示を解除

### Notes
- 画像ビューアではなくHTML内のSVG表示で閲覧する

## 2026-06-09 / compact split view

### Updated
- `plantuml/aki_normal_cases.puml` をPNG閲覧用の索引に変更
- 全体ツリーを `plantuml/aki_generated_from_yaml.puml` とSVG出力で保持
- PNGが縦横に切れないよう、通常技ケースを `弱技`, `中技`, `強技`, `空中技` に分割
- `scripts/generate_puml_from_yaml.py` にカテゴリ別PlantUML生成を追加

### Added
- `plantuml/aki_normal_cases_light.puml`
- `plantuml/aki_normal_cases_medium.puml`
- `plantuml/aki_normal_cases_heavy.puml`
- `plantuml/aki_normal_cases_jump.puml`

### Notes
- 分割PNGはすべて高さ4096px未満に収まることを確認
- 全体を一枚で見る場合はSVGを使う

## 2026-06-09 / switch case tree

### Updated
- `plantuml/aki_normal_cases.puml` の分岐を `if/else yes/no` 連鎖から `switch/case` 形式へ変更
- 各通常技を `case` として並べ、技ごとの中に `空振り`, `ガードさせた`, `ヒット` の分岐を配置
- `ガードさせた`, `ヒット` の距離分岐も `密着`, `中間`, `先端` の `case` として配置
- `scripts/generate_puml_from_yaml.py` の生成ロジックを同形式に更新

### Notes
- 技ごとの分岐構造を見やすくするための表示形式変更
- フレーム値やTODO判断内容の追加推測は行っていない

## 2026-06-09 / normal case tree

### Updated
- `plantuml/aki_normal_cases.puml` を通常技ごとの第一階層ツリーへ変更
- 各通常技の下に `空振り`, `ガードさせた`, `ヒット` の分岐を追加
- `ガードさせた`, `ヒット` の下に `密着`, `中間`, `先端` の分岐を追加
- `scripts/generate_puml_from_yaml.py` を `data/aki_normals.yml` と `data/rules.yml` から技別ツリーを生成する形に更新
- `data/rules.yml` に通常技ケースツリー用の分岐テンプレートを追加

### Notes
- 距離別の具体的な判断内容は未検証のため `TODO確認` として残した
- PlantUML画像を再生成した

## 2026-06-09 / sf6-frame.app 2026-05-28

### Updated
- `data/aki_normals.yml` の通常技フレーム値を `sf6-frame.app` の A.K.I. データで更新
- `startup`, `active`, `recovery`, `on_hit`, `on_block` を取得できた範囲で反映
- `cancel.source_code` に取得元のキャンセル表記を保存
- `plantuml/aki_normal_cases.puml` にフレーム参照元メモを追加

### Notes
- 参照元: `https://sf6-frame.app/`
- データバージョン: `2026-05-28`
- 空中通常技の `on_hit`, `on_block` は取得元が空欄のため `TODO` のまま
- `cancel.source_code` の `C` / `SA` は取得元表記をそのまま記録し、詳細なキャンセル可否への分解は行っていない

## 2026-06-09 / patch version TODO

### Updated
- `plantuml/aki_normal_cases.puml` に空中通常技の確認分岐を追加

### Added
- `data/aki_normals.yml` に不足していた空中通常技をTODO付きで追加
- 追加: `j.LP`, `j.MP`, `j.HP`, `j.LK`, `j.MK`, `j.HK`

### Notes
- フレーム値、ガード時有利不利、着地後状況は未確認のため `TODO` のまま
- 推測でフレーム値は入力していない

## TODO: YYYY-MM-DD / patch version

### Updated
- TODO

### Added
- A.K.I.通常技ケース整理ベースを作成
- `aki_normals.yml`
- `rules.yml`
- `aki_normal_cases.puml`

### Notes
- フレーム値は未入力
- 公式パッチノート、フレームデータ参照元を追記予定
