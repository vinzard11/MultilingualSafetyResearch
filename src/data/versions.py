"""The prompt-version table: load, save and update outputs/prompt_versions.csv."""

from pathlib import Path

import pandas as pd

from src import config
from src.data.schema import VERSION_COLUMNS, validate_versions


def load_versions(path: Path | None = None) -> pd.DataFrame:
    """Load the table, or an empty one if it doesn't exist yet."""
    path = path or config.VERSIONS_PATH
    if not path.exists():
        return pd.DataFrame(columns=VERSION_COLUMNS)
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")
    df["harmful"] = df["harmful"].map({"True": True, "False": False})
    return df[VERSION_COLUMNS]


def save_versions(df: pd.DataFrame, path: Path | None = None) -> None:
    """Validate, then write the table."""
    path = path or config.VERSIONS_PATH
    df = df[VERSION_COLUMNS].fillna("")
    validate_versions(df)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")


def upsert(master: pd.DataFrame, rows: pd.DataFrame) -> pd.DataFrame:
    """Replace rows with matching version_id and append new ones."""
    rows = rows[VERSION_COLUMNS]
    if master.empty:
        return rows.sort_values("version_id").reset_index(drop=True)
    kept = master[~master["version_id"].isin(rows["version_id"])]
    return pd.concat([kept, rows], ignore_index=True).sort_values("version_id").reset_index(drop=True)
