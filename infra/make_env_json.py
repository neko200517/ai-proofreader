# infra/make_env_json.py
import json
import pathlib
import sys

# 設定：関数の論理名（template.yaml の Resources 名）
FUNCTION_NAME = "ProofreadFunction"

# backend/.env へのパス（infra からの相対）
ENV_PATH = pathlib.Path(__file__).resolve().parent.parent / "backend" / ".env"
OUT_PATH = pathlib.Path(__file__).resolve().parent / "env.json"

if not ENV_PATH.exists():
    print(f"[ERROR] .env not found: {ENV_PATH}", file=sys.stderr)
    sys.exit(1)

env_map = {}

with ENV_PATH.open(encoding="utf-8") as f:
    for raw in f:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # 例: KEY=VALUE / KEY="VALUE" / export KEY=VALUE に対応
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        env_map[k] = v

obj = {FUNCTION_NAME: env_map}

OUT_PATH.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"[OK] Wrote {OUT_PATH} with {len(env_map)} keys.")
