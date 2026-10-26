"""Build the prompt-version table skeleton.

    python -m src.run.build_versions

Adds a row for every (source prompt, language, form) not yet in
outputs/prompt_versions.csv. Existing rows (translations in progress) are
never overwritten.

    en_original, native_indicsafe   text from the source, status `final`
    translated forms                status `pending`, filled by src/translate/
"""

import pandas as pd

from src import config
from src.data.loaders import load_all
from src.data.versions import load_versions, save_versions, upsert
from src.translate.common import english_prompts, versions_from_texts


def skeleton(sources: pd.DataFrame) -> pd.DataFrame:
    """Every prompt version the design calls for."""
    langs = config.load("languages")
    english = english_prompts(sources)
    parts = [versions_from_texts(english, "en", "en_original", english["text"].tolist(),
                                 translator="source", status="final")]
    for lang in langs["target_languages"]:
        for form in langs["translated_forms"]:
            parts.append(versions_from_texts(english, lang, form, [""] * len(english),
                                             translator="", status="pending"))
        native = sources[(sources["source"] == "indicsafe") & (sources["language"] == lang)]
        parts.append(versions_from_texts(native, lang, "native_indicsafe", native["text"].tolist(),
                                         translator="source", status="final"))
    return pd.concat(parts, ignore_index=True)


def run() -> pd.DataFrame:
    existing = load_versions()
    rows = skeleton(load_all())
    new = rows[~rows["version_id"].isin(existing["version_id"])]
    table = upsert(existing, new)
    save_versions(table)
    print(f"added {len(new):,} new rows; table has {len(table):,}")
    print(table.groupby(["language", "form", "status"]).size().to_string())
    return table


if __name__ == "__main__":
    run()
