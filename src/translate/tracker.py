"""Translator tracker sheets: export work for native speakers, import it back.

One CSV per (language, form) for the forms done or checked by people:
`human`, `romanized` and `codemixed`.

    python -m src.translate.tracker export --language te --form human
    python -m src.translate.tracker import outputs/trackers/te_human.csv --by "translator"

Sheet columns:
    version_id, source, source_id, harmful, harm_category   (don't edit)
    english_text      the English source prompt
    reference_text    the final human translation (romanized/codemixed only)
    draft             generated draft to edit (romanized/codemixed only)
    final_text        FILL IN: the finished text
    skip              FILL IN: "y" to skip this prompt (no reason needed)
    notes             optional comments

`human` sheets never include a machine draft: human translations must be done
without AI or machine-translation tools (docs/TRANSLATOR_BRIEF.md).
"""

import argparse
from pathlib import Path

import pandas as pd

from src import config
from src.data.loaders import load_all
from src.data.schema import VERSION_COLUMNS, make_version_id
from src.data.versions import load_versions, save_versions, upsert
from src.translate.common import english_prompts

HUMAN_FORMS = ("human", "romanized", "codemixed")
SHEET_COLUMNS = [
    "version_id", "source", "source_id", "harmful", "harm_category",
    "english_text", "reference_text", "draft", "final_text", "skip", "notes",
]
SKIP_VALUES = {"y", "yes", "x", "1", "true"}


def tracker_path(language: str, form: str) -> Path:
    return config.TRACKER_DIR / f"{language}_{form}.csv"


def export_tracker(language: str, form: str) -> Path:
    """Write the tracker sheet for one language and form, keeping any finished work."""
    versions = load_versions().set_index("version_id")
    prompts = english_prompts(load_all())

    if form != "human":
        # Only prompts with a finished human translation can be romanized/code-mixed.
        human_ids = [make_version_id(s, i, language, "human")
                     for s, i in zip(prompts["source"], prompts["source_id"])]
        done = [vid in versions.index and versions.at[vid, "status"] == "final" for vid in human_ids]
        prompts = prompts[done].reset_index(drop=True)

    rows = []
    for p in prompts.itertuples(index=False):
        vid = make_version_id(p.source, p.source_id, language, form)
        existing = versions.loc[vid] if vid in versions.index else None
        reference = draft = ""
        if form != "human":
            reference = versions.at[make_version_id(p.source, p.source_id, language, "human"), "text"]
            if existing is not None and existing["status"] == "draft":
                draft = existing["text"]
        final = existing["text"] if existing is not None and existing["status"] == "final" else ""
        skip = "y" if existing is not None and existing["status"] == "skipped" else ""
        notes = existing["notes"] if existing is not None else ""
        rows.append([vid, p.source, p.source_id, p.harmful, p.harm_category,
                     p.english_text, reference, draft, final, skip, notes])

    path = tracker_path(language, form)
    path.parent.mkdir(parents=True, exist_ok=True)
    # utf-8-sig so Excel and Google Sheets show Indic scripts correctly.
    pd.DataFrame(rows, columns=SHEET_COLUMNS).to_csv(path, index=False, encoding="utf-8-sig")
    return path


def import_tracker(path: Path, language: str, form: str, by: str) -> int:
    """Read a filled sheet back into the prompt-version table. Returns rows updated."""
    sheet = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = set(SHEET_COLUMNS) - set(sheet.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")

    updates = []
    for r in sheet.itertuples(index=False):
        if r.version_id != make_version_id(r.source, r.source_id, language, form):
            raise ValueError(f"{r.version_id} does not belong in a {language}/{form} sheet")
        if r.skip.strip().lower() in SKIP_VALUES:
            text, status = "", "skipped"
        elif r.final_text.strip():
            text, status = r.final_text.strip(), "final"
        else:
            continue   # not done yet
        updates.append([r.version_id, r.source, r.source_id, r.harmful == "True", r.harm_category,
                        language, form, text, by, status, r.notes])

    if updates:
        save_versions(upsert(load_versions(), pd.DataFrame(updates, columns=VERSION_COLUMNS)))
    return len(updates)


def _parse_name(path: Path) -> tuple[str, str]:
    language, form = path.stem.split("_", 1)
    return language, form


if __name__ == "__main__":
    langs = config.load("languages")
    parser = argparse.ArgumentParser(description="Export or import translator tracker sheets.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ex = sub.add_parser("export")
    ex.add_argument("--language", required=True, choices=langs["target_languages"])
    ex.add_argument("--form", required=True, choices=HUMAN_FORMS)

    im = sub.add_parser("import")
    im.add_argument("path", type=Path, help="a sheet named <language>_<form>.csv")
    im.add_argument("--by", help="who translated/checked it (default for `human`: the language's translator)")

    args = parser.parse_args()
    if args.cmd == "export":
        print(f"wrote {export_tracker(args.language, args.form)}")
    else:
        language, form = _parse_name(args.path)
        by = args.by or (langs["languages"][language]["human_translator"] if form == "human" else None)
        if not by:
            parser.error("--by is required for romanized and codemixed sheets")
        print(f"imported {import_tracker(args.path, language, form, by)} rows from {args.path}")
