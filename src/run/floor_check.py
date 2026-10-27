"""Week-1 go/no-go check: is there enough harmful compliance to measure?

    python -m src.run.floor_check

STUB. See docs/ANALYSIS_PLAN.md §5.5.

About n_prompts harmful JailbreakBench prompts in one language and form
(configs/run.yaml: floor_check; Telugu mt_google by default), for every enabled
model. Writes batch files to outputs/batches/floor_check/ only; nothing is
sent here (submitting is src/run/submit.py).
"""

from src import config
from src.run.build_batches import BATCH_DIR

FLOOR_DIR = BATCH_DIR / "floor_check"


def select_versions(versions):
    # TODO: n_prompts `final` harmful JBB versions in floor_check language and
    # form, sampled with the seed from configs/run.yaml.
    raise NotImplementedError


def run() -> None:
    settings = config.load("run")["floor_check"]
    # TODO: render the selected versions with build_batches.render and
    # request_body, one file per enabled model in FLOOR_DIR.
    raise NotImplementedError(f"floor check not built yet: {settings}")


if __name__ == "__main__":
    run()
