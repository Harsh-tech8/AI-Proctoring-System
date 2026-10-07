from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / "ai-proctoring-system.zip"

EXCLUDED = {".git", "__pycache__", ".venv", "venv"}
EXCLUDED_SUFFIXES = {".pyc", ".zip"}

with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED for part in path.parts):
            continue
        if path.suffix in EXCLUDED_SUFFIXES:
            continue
        zf.write(path, path.relative_to(ROOT.parent))

print(f"Created: {OUTPUT}")
