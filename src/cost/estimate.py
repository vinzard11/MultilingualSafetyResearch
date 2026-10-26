"""Cost estimator: API cost computed from the configs.

    python -m src.cost.estimate                           # enabled models only
    python -m src.cost.estimate --include gemini-4-argon  # also cost a disabled model

Counts come from the configs (sources' expected counts, languages, forms,
templates, repeat fraction, enabled models), so changing the model list
changes every number. Judges score every response, so judge cost scales
with the number of models too.
"""

import argparse

from src import config


def planned_counts(n_models: int) -> dict[str, int]:
    """Prompt versions, responses and judgments implied by the configs."""
    sources = config.load("sources")
    langs = config.load("languages")
    run = config.load("run")

    n_english = sources["jbb"]["expected_count"] + sources["xstest"]["expected_count"]
    per_english = 1 + len(langs["target_languages"]) * len(langs["translated_forms"])
    versions = n_english * per_english + sources["indicsafe"]["expected_count"]
    with_templates = versions * len(run["templates"])
    per_model = with_templates + round(with_templates * run["repeat_fraction"])
    responses = per_model * n_models
    return {
        "english_prompts": n_english,
        "prompt_versions": versions,
        "with_templates": with_templates,
        "responses_per_model": per_model,
        "responses": responses,
        "judgments_per_judge": responses,
        "judgments": responses * len(config.load("judges")["judges"]),
    }


def call_cost(model: dict, n_calls: int, input_tokens: int, output_tokens: int) -> float:
    """USD for n_calls to one model, with the batch discount if it has a batch variant."""
    usd = n_calls * (input_tokens * model["price_input_per_m"]
                     + output_tokens * model["price_output_per_m"]) / 1e6
    if model["batch_available"]:
        usd *= 1 - config.load("models")["batch_discount"]
    return usd


def estimate(include: tuple[str, ...] = ()) -> dict:
    all_models = config.load("models")["models"]
    models = {k: m for k, m in all_models.items() if m["enabled"] or k in include}
    a = config.load("run")["cost_assumptions"]
    counts = planned_counts(len(models))

    generation = {
        k: call_cost(m, counts["responses_per_model"], a["response_input_tokens"],
                     a["response_output_tokens"] + a["response_reasoning_tokens"])
        for k, m in models.items()
    }
    judges = {
        j["model"]: call_cost(all_models[j["model"]], counts["judgments_per_judge"],
                              a["judge_input_tokens"], a["judge_output_tokens"])
        for j in config.load("judges")["judges"]
    }
    subtotal = sum(generation.values()) + sum(judges.values())
    with_buffer = subtotal * (1 + a["dev_rerun_buffer"])
    total = with_buffer * (1 + a["openrouter_fee"])
    return {"models": list(models), "counts": counts, "generation": generation, "judges": judges,
            "subtotal": subtotal, "with_buffer": with_buffer, "total": total}


def _print(est: dict) -> None:
    a = config.load("run")["cost_assumptions"]
    c = est["counts"]
    print(f"Models: {len(est['models'])} ({', '.join(est['models'])})")
    print(f"Prompt versions {c['prompt_versions']:,} x templates = {c['with_templates']:,}"
          f" + repeats = {c['responses_per_model']:,} responses per model")
    print(f"Responses {c['responses']:,}  |  judgments {c['judgments']:,}\n")

    print("Generation")
    for k, usd in est["generation"].items():
        print(f"  {k:<18} ${usd:>9,.2f}")
    print(f"  {'subtotal':<18} ${sum(est['generation'].values()):>9,.2f}\n")
    print("Judges")
    for k, usd in est["judges"].items():
        print(f"  {k:<18} ${usd:>9,.2f}")
    print(f"  {'subtotal':<18} ${sum(est['judges'].values()):>9,.2f}\n")

    for label, usd in [("Subtotal", est["subtotal"]),
                       (f"+{a['dev_rerun_buffer']:.0%} dev and reruns", est["with_buffer"]),
                       (f"+{a['openrouter_fee']:.1%} OpenRouter fee", est["total"])]:
        print(f"{label:<25}${usd:>9,.2f}")
    print(f"\n{'TOTAL':<25}${est['total']:>9,.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate API cost from the configs.")
    parser.add_argument("--include", nargs="*", default=[], metavar="MODEL",
                        help="also cost these disabled models")
    _print(estimate(tuple(parser.parse_args().include)))
