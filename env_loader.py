import os
from pathlib import Path

_LOADED = False

def load_env(search_start: Path | None = None):
    global _LOADED
    if _LOADED:
        return
    search_start = search_start or Path.cwd()
    # Walk upward looking for .env up to repo root depth (8 levels safety)
    for _ in range(8):
        candidate = search_start / '.env'
        if candidate.exists():
            _parse_env_file(candidate)
            _LOADED = True
            return
        if search_start.parent == search_start:
            break
        search_start = search_start.parent
    # Fallback: if python-dotenv installed, try load_dotenv (will search default locations)
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass


def _parse_env_file(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
