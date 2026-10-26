"""Submit batch files to OpenRouter, poll them, and collect responses.

STUB. Nothing here calls an API yet.

Collected responses go to outputs/responses/<model>.csv with columns
RESPONSE_COLUMNS, one row per request in the batch file.
"""

from src import config
from src.run.build_batches import BATCH_DIR, unset_settings

RESPONSE_DIR = config.OUTPUT_DIR / "responses"
RESPONSE_COLUMNS = [
    "custom_id", "model", "version_id", "template", "repeat",
    "response_text", "finish_reason", "input_tokens", "output_tokens", "reasoning_tokens",
]


def check_ready() -> None:
    """Refuse to submit while any run setting is still a placeholder."""
    missing = unset_settings(config.enabled_models())
    if missing:
        raise RuntimeError("settings still placeholders: " + ", ".join(missing))


def submit(model: str) -> str:
    """Upload outputs/batches/<model>.jsonl and start a batch. Returns the batch id."""
    check_ready()
    # TODO: OpenRouter batch API for models with batch_available; otherwise
    # rate-limited direct calls. Key from config.api_key("OPENROUTER_API_KEY").
    raise NotImplementedError(f"submit is not implemented yet ({BATCH_DIR / f'{model}.jsonl'})")


def poll(batch_id: str) -> str:
    """Return the batch status."""
    # TODO
    raise NotImplementedError


def collect(model: str, batch_id: str) -> None:
    """Download results and write RESPONSE_DIR/<model>.csv."""
    # TODO: parse each result line into RESPONSE_COLUMNS; keep failed requests
    # (finish_reason) so they can be retried, not silently dropped.
    raise NotImplementedError
