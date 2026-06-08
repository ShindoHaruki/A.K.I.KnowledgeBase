# SF6 A.K.I. 技振りケース整理ベース

PlantUMLで「A.K.I.の通常技を振った後のケース」を整理するためのベースです。

## 使い方

1. `data/aki_normals.yml` に通常技ごとの情報を追記する
2. `data/rules.yml` に判断基準を調整する
3. `plantuml/aki_normal_cases.puml` をPlantUMLで表示する
4. パッチごとの変更は `notes/changelog.md` に記録する

## 更新の頼み方例

```text
この aki_normals.yml を元に、A.K.I.の通常技後の判断をPlantUMLに反映して。
不明点は TODO のまま残して、更新差分を changelog.md に書いて。
```

## 方針

- フレーム値・確反・キャンセル可否は更新されやすいので、YAML側で管理
- PlantUMLは判断フローを見やすくするための出力
- 不明な情報は `TODO` のまま残す
