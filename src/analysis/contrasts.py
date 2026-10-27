"""Analysis 2-3 (Q2, Q3): paired contrasts and their confidence intervals.

STUB. See docs/ANALYSIS_PLAN.md.

Paired contrasts on the same source prompts, per model and language:
  - mt_google / mt_llm vs human    -> translation artifact
  - romanized / codemixed vs human -> script and mixing effect
  - human vs en_original           -> remaining language effect
for harmful compliance, over-refusal and garbled rates. The translation-artifact
contrast is reported on all prompts and on intent-preserved prompts only.

Confidence intervals come from a mixed-effects logistic regression, one row
per response, with the majority label of the three judges as the outcome.
Fixed effects: model, plus a form term coded within each language (English has
no forms). Random effect: prompt only; three judges are too few to treat judge
as a random effect, so refitting on each judge's labels on their own is the
sensitivity check. Results are reported per model; origin is described, not
estimated.
"""


def majority_label(judgments):
    # TODO: one label per response from the three judges; record ties.
    raise NotImplementedError


def paired_contrasts(labels, intent_preserved_only: bool = False):
    # TODO
    raise NotImplementedError


def fit_mixed_model(labels, outcome: str, judge: str | None = None):
    # TODO: judge=None uses the majority label; a judge name refits on that judge's labels.
    raise NotImplementedError
