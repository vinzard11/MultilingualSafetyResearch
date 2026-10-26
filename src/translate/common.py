"""Helpers shared by the translation modules."""

import pandas as pd

from src.data.schema import VERSION_COLUMNS, make_version_id


def english_prompts(sources: pd.DataFrame) -> pd.DataFrame:
    """English source prompts that get translated (JBB and XSTest, not IndicSafe)."""
    return sources[sources["language"] == "en"].reset_index(drop=True)


def versions_from_texts(
    prompts: pd.DataFrame,
    language: str,
    form: str,
    texts: list[str],
    translator: str,
    status: str,
) -> pd.DataFrame:
    """Build prompt-version rows for one language and form from translated texts."""
    if len(texts) != len(prompts):
        raise ValueError(f"got {len(texts)} texts for {len(prompts)} prompts")
    return pd.DataFrame({
        "version_id": [make_version_id(s, i, language, form)
                       for s, i in zip(prompts["source"], prompts["source_id"])],
        "source": prompts["source"],
        "source_id": prompts["source_id"],
        "harmful": prompts["harmful"],
        "harm_category": prompts["harm_category"],
        "language": language,
        "form": form,
        "text": texts,
        "translator": translator,
        "status": status,
        "notes": "",
    })[VERSION_COLUMNS]
