"""`codemixed` form: words switched between the language and English within a
sentence (Tenglish, Tanglish, Hinglish).

Drafts are generated from `human` rows (status `draft`), then edited and
signed off by a native speaker through the tracker (status `final`).

STUB. How drafts are generated is an open decision
(configs/languages.yaml: translated_forms.codemixed.drafting_method).
"""

import pandas as pd

from src import config
from src.data.schema import make_version_id


def draft_codemix(human_texts: list[str], english_texts: list[str], language: str) -> list[str]:
    method = config.load("languages")["translated_forms"]["codemixed"]["drafting_method"]
    if not method:
        raise NotImplementedError(
            "code-mix drafting method is not chosen yet: set "
            "translated_forms.codemixed.drafting_method in configs/languages.yaml"
        )
    # TODO: implement the chosen drafting method.
    raise NotImplementedError(f"code-mix drafting with {method!r} is not implemented yet")


def draft_rows(versions: pd.DataFrame, english: pd.DataFrame, language: str) -> pd.DataFrame:
    """Draft `codemixed` rows from final `human` rows in one language.

    `english` is the source-prompt table, used to look up each prompt's English text.
    """
    human = versions[(versions["language"] == language) & (versions["form"] == "human")
                     & (versions["status"] == "final")]
    en_text = english.set_index(["source", "source_id"])["english_text"]
    english_texts = [en_text[(s, i)] for s, i in zip(human["source"], human["source_id"])]

    drafts = human.copy()
    drafts["form"] = "codemixed"
    drafts["version_id"] = [make_version_id(s, i, language, "codemixed")
                            for s, i in zip(drafts["source"], drafts["source_id"])]
    drafts["text"] = draft_codemix(human["text"].tolist(), english_texts, language)
    drafts["translator"] = f"codemix:{config.load('languages')['translated_forms']['codemixed']['drafting_method']}"
    drafts["status"] = "draft"
    drafts["notes"] = ""
    return drafts.reset_index(drop=True)
