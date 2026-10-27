"""Judge prompts and label parsing.

Each judge in configs/judges.yaml scores every response. Judges see the prompt
as sent, its English source, and the response, never the model's name.

Rendering and parsing are implemented; building and submitting judge batches
is a STUB.
"""

import json
import re

from src import config

PLACEHOLDERS = ("{prompt_text}", "{english_source}", "{response}")


def labels() -> list[str]:
    return config.load("judges")["labels"]


def render_judge_prompt(prompt_text: str, english_source: str, response: str) -> str:
    """Fill the rubric's input slots. (str.format would trip on the rubric's JSON braces.)"""
    with open(config.ROOT / config.load("judges")["rubric"], encoding="utf-8") as f:
        rubric = f.read()
    for slot, value in zip(PLACEHOLDERS, (prompt_text, english_source, response)):
        rubric = rubric.replace(slot, value)
    return rubric


def parse_judgment(raw: str) -> dict:
    """Parse a judge reply into {label, intent_preserved, short_reason}. Raises ValueError if invalid."""
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"no JSON object in judge reply: {raw[:200]!r}")
    data = json.loads(match.group(0))
    if data.get("label") not in labels():
        raise ValueError(f"invalid label {data.get('label')!r}")
    if not isinstance(data.get("intent_preserved"), bool):
        raise ValueError(f"invalid intent_preserved {data.get('intent_preserved')!r}")
    return {"label": data["label"], "intent_preserved": data["intent_preserved"],
            "short_reason": str(data.get("short_reason", ""))}


def build_judge_batches() -> None:
    """One batch file per judge over all collected responses."""
    # TODO: read outputs/responses/*.csv, join prompt text and English source,
    # render with render_judge_prompt, write outputs/judge_batches/<judge>.jsonl.
    raise NotImplementedError
