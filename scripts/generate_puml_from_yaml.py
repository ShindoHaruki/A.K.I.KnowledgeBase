"""Generate PlantUML files from data/aki_normals.yml.

Requires:
  pip install pyyaml

Usage:
  python scripts/generate_puml_from_yaml.py
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "aki_normals.yml"
RULES = ROOT / "data" / "rules.yml"
MAIN_OUT = ROOT / "plantuml" / "aki_normal_cases.puml"
GENERATED_OUT = ROOT / "plantuml" / "aki_generated_from_yaml.puml"
GROUPS = [
    ("light", "弱技", {"5LP", "2LP", "5LK", "2LK"}),
    ("medium", "中技", {"5MP", "2MP", "5MK", "2MK"}),
    ("heavy", "強技", {"5HP", "2HP", "5HK", "2HK"}),
    ("jump", "空中技", {"j.LP", "j.MP", "j.HP", "j.LK", "j.MK", "j.HK"}),
]


def action(lines, text, indent=""):
    if text:
        lines.append(f"{indent}:{text};")


def wbs_text(text):
    return str(text).replace("\\", "\\\\").replace("\n", " ")


def tree_node(lines, level, text):
    lines.append(f"{'+' * level} {wbs_text(text)}")


def move_summary(move):
    return (
        f"発生 {move.get('startup', 'TODO')} / "
        f"持続 {move.get('active', 'TODO')} / "
        f"硬直 {move.get('recovery', 'TODO')}"
    )


def add_range_branch(lines, outcome, move, tree, indent):
    ranges = tree["outcomes"][outcome]["ranges"]
    frame_key = "on_block" if outcome == "block" else "on_hit"
    frame_label = "ガード" if outcome == "block" else "ヒット"

    lines.append(f"{indent}switch (距離)")
    for key in ("close", "mid", "tip"):
        lines.append(f"{indent}case ({ranges[key]['label']})")
        action(lines, f"{frame_label}時 {move.get(frame_key, 'TODO')}", indent + "  ")
        action(lines, ranges[key]["action"], indent + "  ")
    lines.append(f"{indent}endswitch")


def build_tree_lines(data, rules, normals, title_suffix=""):
    tree = rules["normal_case_tree"]
    title = "Street Fighter 6 - A.K.I. 通常技別ケース整理"
    if title_suffix:
        title = f"{title} - {title_suffix}"

    lines = [
        "@startsalt",
        "{",
        "{T",
        f"+ {title}",
        "++ フレーム詳細: data/aki_normals.yml",
        f"++ 参照元: {data.get('version', 'TODO')}",
    ]

    for move in normals:
        move_id = move.get("id", "UNKNOWN")
        name = move.get("name", "")
        tree_node(lines, 2, f"{move_id} {name}")
        tree_node(lines, 3, move_summary(move))
        tree_node(lines, 3, "空振り")
        tree_node(lines, 4, tree["outcomes"]["whiff"]["action"])
        for item in move.get("cases", {}).get("whiff", []):
            tree_node(lines, 4, item)

        tree_node(lines, 3, "ガードさせた")
        block_ranges = tree["outcomes"]["block"]["ranges"]
        for key in ("close", "mid", "tip"):
            tree_node(lines, 4, block_ranges[key]["label"])
            tree_node(lines, 5, f"ガード時 {move.get('on_block', 'TODO')}")
            tree_node(lines, 5, block_ranges[key]["action"])

        tree_node(lines, 3, "ヒット")
        hit_ranges = tree["outcomes"]["hit"]["ranges"]
        for key in ("close", "mid", "tip"):
            tree_node(lines, 4, hit_ranges[key]["label"])
            tree_node(lines, 5, f"ヒット時 {move.get('on_hit', 'TODO')}")
            tree_node(lines, 5, hit_ranges[key]["action"])

    lines.extend([
        "}",
        "}",
        "",
        "@endsalt",
        "",
    ])
    return lines


def build_index_lines(data):
    lines = [
        "@startsalt",
        "{",
        "{T",
        "+ Street Fighter 6 - A.K.I. 通常技別ケース整理",
        "++ 全体版は aki_generated_from_yaml.svg を参照",
        "++ PNG閲覧用",
    ]
    for slug, label, _ in GROUPS:
        lines.append(f"+++ {label}: aki_normal_cases_{slug}.png")
    lines.extend([
        f"++ 参照元: {data.get('version', 'TODO')}",
        "}",
        "}",
        "",
        "@endsalt",
        "",
    ])
    return lines


def build_lines(data, rules):
    return build_index_lines(data)


def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    rules = yaml.safe_load(RULES.read_text(encoding="utf-8"))
    normals = data.get("normals", [])
    content = "\n".join(build_lines(data, rules))
    generated_content = "\n".join(build_tree_lines(data, rules, normals))

    MAIN_OUT.write_text(content, encoding="utf-8")
    GENERATED_OUT.write_text(generated_content, encoding="utf-8")
    print(f"generated: {MAIN_OUT}")
    print(f"generated: {GENERATED_OUT}")
    for slug, label, ids in GROUPS:
        group_normals = [move for move in normals if move.get("id") in ids]
        out = ROOT / "plantuml" / f"aki_normal_cases_{slug}.puml"
        out.write_text(
            "\n".join(build_tree_lines(data, rules, group_normals, label)),
            encoding="utf-8",
        )
        print(f"generated: {out}")

if __name__ == "__main__":
    main()
