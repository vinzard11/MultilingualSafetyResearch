"""`romanized` form: the human translation written in Latin script.

Drafts are generated from `human` rows (status `draft`), then edited and
signed off by a native speaker through the tracker (status `final`).

STUB. The romanization tool is an open decision
(configs/languages.yaml: translated_forms.romanized.tool).
"""

import pandas as pd

from src import config
from src.data.schema import make_version_id


def romanize(texts: list[str], language: str) -> list[str]:
    tool = config.load("languages")["translated_forms"]["romanized"]["tool"]
    if not tool:
        raise NotImplementedError(
            "romanization tool is not chosen yet: set translated_forms.romanized.tool in configs/languages.yaml"
        )
    # TODO: call the chosen tool.
    raise NotImplementedError(f"romanization with {tool!r} is not implemented yet")


def draft_rows(versions: pd.DataFrame, language: str) -> pd.DataFrame:
    """Draft `romanized` rows from final `human` rows in one language."""
    human = versions[(versions["language"] == language) & (versions["form"] == "human")
                     & (versions["status"] == "final")]
    drafts = human.copy()
    drafts["form"] = "romanized"
    drafts["version_id"] = [make_version_id(s, i, language, "romanized")
                            for s, i in zip(drafts["source"], drafts["source_id"])]
    drafts["text"] = romanize(human["text"].tolist(), language)
    drafts["translator"] = f"romanize:{config.load('languages')['translated_forms']['romanized']['tool']}"
    drafts["status"] = "draft"
    drafts["notes"] = ""
    return drafts.reset_index(drop=True)
