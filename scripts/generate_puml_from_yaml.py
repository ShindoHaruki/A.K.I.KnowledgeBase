"""Generate a simple PlantUML file from data/aki_normals.yml.

Requires:
  pip install pyyaml

Usage:
  python scripts/generate_puml_from_yaml.py
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "aki_normals.yml"
OUT = ROOT / "plantuml" / "aki_generated_from_yaml.puml"

def main():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    normals = data.get("normals", [])

    lines = [
        "@startuml",
        "title A.K.I. 通常技別ケース - YAML自動生成",
        "",
        "start",
        ":通常技を選ぶ;",
        "",
    ]

    for move in normals:
        move_id = move.get("id", "UNKNOWN")
        name = move.get("name", "")
        lines.extend([
            f"if ({move_id} {name}?) then (yes)",
            "  :技を振る;",
            "  if (ヒット?) then (yes)",
        ])
        for action in move.get("cases", {}).get("hit", []):
            lines.append(f"    :{action};")
        lines.extend([
            "  elseif (ガード?) then (yes)",
        ])
        for action in move.get("cases", {}).get("block", []):
            lines.append(f"    :{action};")
        lines.extend([
            "  else (空振り)",
        ])
        for action in move.get("cases", {}).get("whiff", []):
            lines.append(f"    :{action};")
        lines.extend([
            "  endif",
            "else (no)",
        ])

    lines.append("  :未選択;")
    for _ in normals:
        lines.append("endif")

    lines.extend([
        "",
        "stop",
        "@enduml",
        "",
    ])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"generated: {OUT}")

if __name__ == "__main__":
    main()
