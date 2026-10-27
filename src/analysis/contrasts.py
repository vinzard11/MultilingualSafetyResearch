"""Analysis 2-3 (Q2, Q3): paired contrasts and their confidence intervals.

STUB. See docs/ANALYSIS_PLAN.md.

Paired contrasts on the same source prompts, per model and language:
  - mt_google / mt_llm vs human    -> translation artifact
  - romanized / codemixed vs human -> script and mixing effect
  - human vs en_original           -> remaining language effect
for harmful compliance, over-refusal and garbled rates.

Confidence intervals come from a mixed-effects logistic regression on the
binary outcome, one row per judgment: fixed effects language, form, model
(and interactions); crossed random effects for prompt and judge.
"""


def paired_contrasts(labels):
    # TODO: raw paired differences per model x language x contrast.
    raise NotImplementedError


def fit_mixed_model(labels, outcome: str):
    # TODO: fit the model for one outcome (e.g. complied_harmful) and return
    # each contrast with a 95% CI. Library is an open decision (see ANALYSIS_PLAN).
    raise NotImplementedError
