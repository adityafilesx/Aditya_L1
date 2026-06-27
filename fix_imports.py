from pathlib import Path
import re

ROOT = Path("backend")

REPLACEMENTS = {
    r"\bfrom api\.": "from backend.api.",
    r"\bimport api\.": "import backend.api.",

    r"\bfrom events\.": "from backend.events.",
    r"\bimport events\.": "import backend.events.",

    r"\bfrom features\.": "from backend.features.",
    r"\bimport features\.": "import backend.features.",

    r"\bfrom physics\.": "from backend.physics.",
    r"\bimport physics\.": "import backend.physics.",

    r"\bfrom forecasting\.": "from backend.forecasting.",
    r"\bimport forecasting\.": "import backend.forecasting.",

    r"\bfrom observation_engine\.": "from backend.observation_engine.",
    r"\bimport observation_engine\.": "import backend.observation_engine.",

    r"\bfrom nowcasting\.": "from backend.nowcasting.",
    r"\bimport nowcasting\.": "import backend.nowcasting.",

    r"\bfrom ml\.": "from backend.ml.",
    r"\bimport ml\.": "import backend.ml.",

    r"\bfrom xai\.": "from backend.xai.",
    r"\bimport xai\.": "import backend.xai.",

    r"\bfrom reasoning\.": "from backend.reasoning.",
    r"\bimport reasoning\.": "import backend.reasoning.",

    r"\bfrom platform\.": "from backend.platform.",
    r"\bimport platform\.": "import backend.platform.",

    r"\bfrom aditya_flare\.": "from backend.aditya_flare.",
    r"\bimport aditya_flare\.": "import backend.aditya_flare.",

    r"\bfrom physics_engine\.": "from backend.physics_engine.",
    r"\bimport physics_engine\.": "import backend.physics_engine.",
}

count = 0

for file in ROOT.rglob("*.py"):
    text = file.read_text(encoding="utf-8")

    original = text

    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)

    if text != original:
        file.write_text(text, encoding="utf-8")
        count += 1
        print(f"Updated: {file}")

print(f"\nFinished! Updated {count} files.")