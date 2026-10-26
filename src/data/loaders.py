"""Download and normalize the source datasets.

Files are fetched at runtime from the pinned revisions in configs/sources.yaml
and cached in data_cache/ (gitignored). Each loader returns a DataFrame with
schema.SOURCE_COLUMNS.

    python -m src.data.loaders     # download all sources and print counts
"""

import io

import pandas as pd
import requests

from src import config
from src.data.schema import SOURCE_COLUMNS

HARMLESS_INDICSAFE = "Harmless Control Prompts"


def _fetch(source: str, file_key: str) -> pd.DataFrame:
    """Return one source file as a DataFrame, downloading it if not cached."""
    spec = config.load("sources")[source]
    url = spec["files"][file_key].format(revision=spec["revision"])
    path = config.CACHE_DIR / source / spec["revision"] / url.rsplit("/", 1)[-1]
    if not path.exists():
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(resp.content)
    return pd.read_csv(io.BytesIO(path.read_bytes()), encoding="utf-8-sig")


def load_jbb() -> pd.DataFrame:
    """100 harmful + 100 matched harmless JBB behaviors (matched by index)."""
    parts = []
    for file_key, harmful, prefix in [("harmful", True, "h"), ("benign", False, "b")]:
        raw = _fetch("jbb", file_key)
        parts.append(pd.DataFrame({
            "source": "jbb",
            "source_id": raw["Index"].map(lambda i: f"{prefix}{i:03d}"),
            "harmful": harmful,
            "harm_category": raw["Category"],
            "language": "en",
            "text": raw["Goal"],
            "english_text": raw["Goal"],
            "notes": "behavior: " + raw["Behavior"],
        }))
    return pd.concat(parts, ignore_index=True)[SOURCE_COLUMNS]


def load_xstest() -> pd.DataFrame:
    """The 250 safe-but-unsafe-sounding XSTest prompts."""
    raw = _fetch("xstest", "prompts")
    raw = raw[raw["label"] == config.load("sources")["xstest"]["label"]]
    return pd.DataFrame({
        "source": "xstest",
        "source_id": raw["id"].map(lambda i: f"{i:03d}"),
        "harmful": False,
        "harm_category": raw["type"],
        "language": "en",
        "text": raw["prompt"],
        "english_text": raw["prompt"],
        "notes": "focus: " + raw["focus"].astype(str) + "; note: " + raw["note"].astype(str),
    }).reset_index(drop=True)[SOURCE_COLUMNS]


def _stratified_ids(by_category: pd.Series, n: int, seed: int) -> list[str]:
    """Sample n ids, allocated across categories in proportion to their size."""
    sizes = by_category.value_counts().sort_index()
    quotas = sizes * n / sizes.sum()
    alloc = quotas.astype(int)
    # Largest-remainder rounding so the quotas sum to exactly n.
    for cat in (quotas - alloc).sort_values(ascending=False).index[: n - alloc.sum()]:
        alloc[cat] += 1
    picked = []
    for cat, k in alloc.items():
        ids = by_category[by_category == cat].index.to_series()
        picked += ids.sample(n=k, random_state=seed).tolist()
    return sorted(picked)


def load_indicsafe() -> pd.DataFrame:
    """The same n_per_language IndicSafe prompts in each target language."""
    spec = config.load("sources")["indicsafe"]
    langs = config.load("languages")
    code_by_name = {langs["languages"][c]["name"]: c for c in langs["target_languages"]}

    raw = _fetch("indicsafe", "prompts")
    raw = raw[raw["Language"].isin(code_by_name)].copy()
    # The file labels some controls "Harmless Control" and others "... Prompts".
    raw["Category"] = raw["Category"].replace({"Harmless Control": HARMLESS_INDICSAFE})
    # Prompts are parallel across languages; id each English prompt by first appearance.
    ids = {p: f"{i:03d}" for i, p in enumerate(dict.fromkeys(raw["Prompt"]))}
    raw["source_id"] = raw["Prompt"].map(ids)

    by_category = raw.drop_duplicates("source_id").set_index("source_id")["Category"]
    keep = _stratified_ids(by_category, spec["n_per_language"], config.load("run")["seed"])
    raw = raw[raw["source_id"].isin(keep)]

    return pd.DataFrame({
        "source": "indicsafe",
        "source_id": raw["source_id"],
        "harmful": raw["Category"] != HARMLESS_INDICSAFE,
        "harm_category": raw["Category"],
        "language": raw["Language"].map(code_by_name),
        "text": raw["Translated_Prompt"],
        "english_text": raw["Prompt"],
        "notes": "",
    }).sort_values(["language", "source_id"]).reset_index(drop=True)[SOURCE_COLUMNS]


def apply_exclusions(df: pd.DataFrame) -> pd.DataFrame:
    """Drop excluded harm categories and individual prompts (configs/run.yaml)."""
    run = config.load("run")
    excluded_ids = set(run["excluded_prompt_ids"])
    keyed = df["source"] + ":" + df["source_id"]
    return df[~df["harm_category"].isin(run["excluded_harm_categories"]) & ~keyed.isin(excluded_ids)]


def load_all() -> pd.DataFrame:
    """All source prompts from every source, with exclusions applied."""
    df = pd.concat([load_jbb(), load_xstest(), load_indicsafe()], ignore_index=True)
    return apply_exclusions(df).reset_index(drop=True)


if __name__ == "__main__":
    df = load_all()
    print(df.groupby(["source", "language", "harmful"]).size().to_string())
    print(f"\ntotal source prompts: {len(df)}")
