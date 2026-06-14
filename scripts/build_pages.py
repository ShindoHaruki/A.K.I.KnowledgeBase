"""Build the Cloudflare Pages output directory."""

from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def main():
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_index_viewer.py")],
        check=True,
    )

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copy2(ROOT / "index.html", DIST / "index.html")
    print(f"built: {DIST}")


if __name__ == "__main__":
    main()
