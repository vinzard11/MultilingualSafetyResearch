"""Sample responses for human checking and export one sheet per checker.

STUB.

Per language (configs/languages.yaml: validation):
  - main_sample_per_language responses, stratified by model, form and
    harmful/harmless, go to the main checker.
  - overlap_sample_per_language of those same responses also go to the
    overlap checker(s), for agreement. Where there are two overlap checkers,
    the overlap sample is split between them.

Sheets are blind: no model name, no judge labels.
"""

from src import config

SHEET_DIR = config.OUTPUT_DIR / "validation"
SHEET_COLUMNS = ["item_id", "language", "prompt_text", "english_text", "response_text", "label", "intent_preserved", "notes"]


def sample(language: str):
    # TODO: stratified sample from outputs/responses, seeded from configs/run.yaml.
    raise NotImplementedError


def export_sheets(language: str) -> None:
    # TODO: write SHEET_DIR/<language>_<checker>.csv (utf-8-sig) and a private
    # key mapping item_id -> custom_id, model.
    raise NotImplementedError
