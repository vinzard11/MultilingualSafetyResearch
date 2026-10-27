"""Schemas for source prompts and prompt versions.

A *source prompt* is one item from a benchmark (JBB, XSTest, IndicSafe), with
its English text. A *prompt version* is one row per (source prompt, language,
form): the text actually sent to models.
"""

from dataclasses import dataclass, fields

import pandas as pd

from src import config

# pending: no text yet. draft: generated, awaiting native-speaker edit/check.
# final: ready to send to models. skipped: translator chose to skip it.
STATUSES = ("pending", "draft", "final", "skipped")
TEXT_REQUIRED_STATUSES = ("draft", "final")

# Source prompts, as returned by src.data.loaders. `english_text` is what the
# judges see as the English source.
SOURCE_COLUMNS = [
    "source", "source_id", "harmful", "harm_category",
    "language", "text", "english_text", "notes",
]


@dataclass
class PromptVersion:
    version_id: str
    source: str
    source_id: str
    harmful: bool
    harm_category: str
    language: str
    form: str
    text: str | None
    translator: str | None   # "source", "google", "llm:<model>", or a role label (e.g. translator)
    status: str              # one of STATUSES
    notes: str = ""


VERSION_COLUMNS = [f.name for f in fields(PromptVersion)]


def make_version_id(source: str, source_id: str, language: str, form: str) -> str:
    return f"{source}-{source_id}-{language}-{form}"


def allowed_forms() -> dict[str, set[str]]:
    """Map each form id to the language codes it may appear with."""
    langs = config.load("languages")
    targets = set(langs["target_languages"])
    allowed = {form: targets for form in langs["translated_forms"]}
    for form, spec in langs["other_forms"].items():
        allowed[form] = set(spec["languages"])
    return allowed


def validate_versions(df: pd.DataFrame) -> None:
    """Raise ValueError listing every schema problem in a prompt-version table."""
    if list(df.columns) != VERSION_COLUMNS:
        raise ValueError(f"columns must be {VERSION_COLUMNS}, got {list(df.columns)}")

    problems = []
    forms = allowed_forms()

    dupes = df.loc[df["version_id"].duplicated(), "version_id"]
    if len(dupes):
        problems.append(f"duplicate version_id: {sorted(set(dupes))[:5]}")

    for row in df.itertuples(index=False):
        vid = row.version_id
        expected = make_version_id(row.source, row.source_id, row.language, row.form)
        if vid != expected:
            problems.append(f"{vid}: version_id should be {expected}")
        if row.form not in forms:
            problems.append(f"{vid}: unknown form {row.form!r}")
        elif row.language not in forms[row.form]:
            problems.append(f"{vid}: form {row.form!r} not allowed for language {row.language!r}")
        if row.status not in STATUSES:
            problems.append(f"{vid}: unknown status {row.status!r}")
        if row.harmful not in (True, False):
            problems.append(f"{vid}: harmful must be bool")
        if row.status in TEXT_REQUIRED_STATUSES and not (isinstance(row.text, str) and row.text.strip()):
            problems.append(f"{vid}: status {row.status!r} requires text")

    if problems:
        raise ValueError(f"{len(problems)} schema problem(s):\n" + "\n".join(problems))
