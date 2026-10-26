"""Paths, YAML config loading and API keys."""

import os
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "configs"
CACHE_DIR = ROOT / "data_cache"   # downloaded datasets (gitignored)
OUTPUT_DIR = ROOT / "outputs"     # private working data (gitignored)
VERSIONS_PATH = OUTPUT_DIR / "prompt_versions.csv"
TRACKER_DIR = OUTPUT_DIR / "trackers"


def api_key(name: str) -> str:
    """Read an API key from the environment or .env (never from the repo)."""
    load_dotenv(ROOT / ".env")
    key = os.environ.get(name)
    if not key:
        raise RuntimeError(f"{name} is not set. Copy .env.example to .env and fill it in.")
    return key


@lru_cache
def load(name: str) -> dict:
    """Load configs/<name>.yaml."""
    with open(CONFIG_DIR / f"{name}.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def enabled_models() -> dict:
    """Models under test with `enabled: true`, keyed by model key."""
    return {k: m for k, m in load("models")["models"].items() if m["enabled"]}
