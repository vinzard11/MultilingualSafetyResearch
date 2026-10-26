# Analysis Plan (Pre-registration)

> **Status: TEMPLATE.** To be completed and frozen in week 1, **before any model responses are collected**. After freezing, every change goes in the deviations log at the end, with its date and reason.

- Frozen on: `[DATE]`
- Commit: `[COMMIT HASH]`

## 1. Questions

1. **Q1, gap:** For the same request, how much do refusal and harmful-output rates differ across languages, and between US and Chinese models?
2. **Q2, translation artifacts:** How much of the gap is translation artifact versus the language itself?
3. **Q3, variance breakdown:** How much variance does each factor explain?
4. **Q4, over-refusal:** Does refusing harmless prompts also vary by language?

## 2. Hypotheses

`[To fill in: directional expectations, if any, for each question. Mark anything without a prior expectation as exploratory.]`

## 3. Fixed settings

| Setting | Value |
|---|---|
| Template T1 wording | `[FILL IN]` |
| Template T2 system prompt | `[FILL IN]` |
| Temperature | `[FILL IN]` |
| Max output tokens | `[FILL IN]` |
| Reasoning setting per model | Lowest available; exact values `[FILL IN]` |
| LLM translation model (`mt_llm`) | `[FILL IN]` |
| Romanization tool | `[FILL IN]` |
| Code-mix drafting method | `[FILL IN]` |
| Excluded harm categories / prompts | `[FILL IN]` |
| Models included (OpenRouter IDs, pinned providers) | `[FILL IN]` |
| Gemini 4 Argon included? | `[FILL IN]` |
| Judge temperature, max tokens | `[FILL IN]` |
| Random seed | 0 ([configs/run.yaml](../configs/run.yaml)) |

## 4. Data

- **Prompts:** JailbreakBench 200 (100 harmful + 100 matched harmless), XSTest 250 (harmless), IndicSafe 100 per language. Exclusions are applied before any runs.
- **Forms:** `en_original`; `mt_google`, `mt_llm`, `human`, `romanized`, `codemixed` per language; `native_indicsafe`.
- **Responses:** each prompt version × template, plus a fixed 20% repeat subset.
- **Labels:** three judges per response; human labels on about 400 responses per language.

**Primary label per response:** `[FILL IN: e.g. majority of three judges; rule for three-way splits]`

**Prompts skipped by translators:** `[FILL IN: how skipped human translations are handled across forms]`

**Failed or empty responses:** `[FILL IN: retry policy; how remaining failures are counted]`

## 5. Outcomes

| Outcome | Prompts | Definition |
|---|---|---|
| Harmful-compliance rate | Harmful | share labelled `complied_harmful` |
| Over-refusal rate | Harmless | share labelled `refused` |
| Garbled rate | All | share labelled `offtopic_garbled` |

`[FILL IN: whether garbled responses are kept in or dropped from the denominators of the first two rates.]`

## 6. Analyses

### 6.1 Gap (Q1, Q4)

Rates by language × form × model, each compared against English.

- Comparison: `[FILL IN: difference vs. English, with CIs]`
- Uncertainty: `[FILL IN: e.g. bootstrap over prompts, number of resamples]`
- US vs. Chinese models: `[FILL IN]`

### 6.2 Translation artifacts (Q2)

Within each language, compare `mt_google`, `mt_llm` and `human`, and compare `romanized` and `codemixed` against `human`.

- Test: `[FILL IN: paired by source prompt, e.g. McNemar or a paired bootstrap]`
- What counts as a translation artifact: `[FILL IN]`

### 6.3 Variance breakdown (Q3)

G-study in Python with **statsmodels**.

- Facets: prompt item, language, form, model and model origin, template, harm category, judge, repeat run.
- Interactions: language × model origin, form × model, judge × language. `[FILL IN: any others]`
- Estimation: `[FILL IN: variance-component model specification]`
- Check: mixed-effects logistic model on the binary outcomes. `[FILL IN: specification]`
- Decision study: projected reliability for phase 2 by number of prompts and judges. `[FILL IN: target reliability]`

### 6.4 Judge reliability

- Cohen's κ between each judge and the human labels, per language.
- Cohen's κ between main and overlap checkers, per language.
- Self-preference: `[FILL IN: how each judge's scoring of its own lab's model is compared with the other two judges]`
- Threshold: `[FILL IN: κ below which a judge is reported with a caveat or dropped]`

## 7. Multiple comparisons

`[FILL IN: correction method, and which analyses are confirmatory vs. exploratory]`

## 8. What gets published

Aggregates and safe examples only. Raw responses and judge outputs stay private. See [RESEARCH_CONDUCT.md](RESEARCH_CONDUCT.md).

## 9. Deviations log

| Date | Change | Reason |
|---|---|---|
| | | |
