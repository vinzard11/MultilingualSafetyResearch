"""Build one OpenRouter batch request file per enabled model.

    python -m src.run.build_batches

Writes outputs/batches/<model>.jsonl. Every `final` prompt version is rendered
with each template, plus a repeat of a seeded random `repeat_fraction` of
(version, template) pairs to measure run-to-run noise. The repeat subset is
the same for every model. Versions that aren't `final` yet are left out.

Nothing is sent here: submitting is src/run/submit.py.
"""

import json

import pandas as pd

from src import config
from src.data.loaders import load_all
from src.data.versions import load_versions

BATCH_DIR = config.OUTPUT_DIR / "batches"


def custom_id(version_id: str, template: str, repeat: int) -> str:
    return f"{version_id}__{template}__r{repeat}"


def render(template: dict, text: str) -> list[dict]:
    messages = []
    if template["system"]:
        messages.append({"role": "system", "content": template["system"]})
    messages.append({"role": "user", "content": template["user"].replace("{prompt}", text)})
    return messages


def planned_requests(versions: pd.DataFrame) -> pd.DataFrame:
    """(version_id, template, repeat) for every request each model gets."""
    run = config.load("run")
    sources = load_all()   # applies exclusions
    current = set(sources["source"] + ":" + sources["source_id"])
    final = versions[(versions["status"] == "final")
                     & (versions["source"] + ":" + versions["source_id"]).isin(current)]

    pairs = final[["version_id"]].merge(pd.DataFrame({"template": run["templates"]}), how="cross")
    pairs["repeat"] = 0
    repeats = pairs.sample(n=round(len(pairs) * run["repeat_fraction"]), random_state=run["seed"])
    repeats = repeats.assign(repeat=1)
    return pd.concat([pairs, repeats], ignore_index=True)


def request_body(model: dict, messages: list[dict]) -> dict:
    run = config.load("run")
    body = {
        "model": model["openrouter_id"],
        "messages": messages,
        "temperature": run["temperature"],
        "max_tokens": run["max_output_tokens"],
        "reasoning": model["reasoning"],
        "provider": {"order": [model["provider"]], "allow_fallbacks": False} if model["provider"] else None,
    }
    return {k: v for k, v in body.items() if v is not None}


def unset_settings(models: dict) -> list[str]:
    """Settings that are still placeholders. Batches built with these are drafts."""
    run, templates = config.load("run"), config.load("templates")["templates"]
    missing = [f"run.{k}" for k in ("temperature", "max_output_tokens") if run[k] is None]
    missing += [f"templates.{t}" for t in run["templates"]
                if "TODO" in f"{templates[t]['system']}{templates[t]['user']}"]
    for key, m in models.items():
        missing += [f"models.{key}.{f}" for f in ("openrouter_id", "provider", "reasoning") if m[f] is None]
    return missing


def run() -> None:
    versions = load_versions()
    templates = config.load("templates")["templates"]
    models = config.enabled_models()
    plan = planned_requests(versions)
    text = versions.set_index("version_id")["text"]

    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    for key, model in models.items():
        path = BATCH_DIR / f"{key}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for r in plan.itertuples(index=False):
                # OpenAI-style batch line. TODO: confirm against OpenRouter's batch docs.
                line = {
                    "custom_id": custom_id(r.version_id, r.template, r.repeat),
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": request_body(model, render(templates[r.template], text[r.version_id])),
                }
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
        print(f"{key}: {len(plan):,} requests -> {path}")

    not_final = (versions["status"] != "final").sum()
    if not_final:
        print(f"\n{not_final:,} prompt versions are not final yet and were left out.")
    missing = unset_settings(models)
    if missing:
        print(f"\nDRAFT batches: {len(missing)} settings are still placeholders:")
        print("  " + "\n  ".join(missing))


if __name__ == "__main__":
    run()
