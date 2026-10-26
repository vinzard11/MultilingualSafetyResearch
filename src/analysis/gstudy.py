"""Analysis 3 (Q3): variance breakdown (G-study), using statsmodels.

STUB. See docs/ANALYSIS_PLAN.md.

Variance components for prompt item, language, form, model and model origin,
template, harm category, judge and repeat run, plus key interactions
(language x model origin, form x model, judge x language). Outcomes are
binary, so a mixed-effects logistic model is fitted alongside as a check.
A decision study then estimates how many prompts and judges phase 2 needs.
"""


def g_study(labels):
    # TODO
    raise NotImplementedError


def d_study(components, n_prompts, n_judges):
    # TODO
    raise NotImplementedError
