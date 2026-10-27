# Analysis Plan (Pre-registration)

> **Status: TEMPLATE.** To be completed and frozen in week 1, **before any model responses are collected**. After freezing, every change goes in the deviations log at the end, with its date and reason.

- Frozen on: `[DATE]`
- Commit: `[COMMIT HASH]`

## 1. Questions

1. **Q1, gap:** For the same request, how much do refusal and harmful-output rates differ across languages, and between US and Chinese models?
2. **Q2, translation artifacts:** How much of the gap is translation artifact versus the language itself?
3. **Q3, uncertainty:** How large is each contrast, with confidence intervals?
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

**Primary label per response:** the majority label of the three judges; the tie rule is in §6.3.

**Prompts skipped by translators:** `[FILL IN: how skipped human translations are handled across forms]`

**Failed or empty responses:** `[FILL IN: retry policy; how remaining failures are counted]`

## 5. Outcomes

| Outcome | Prompts | Definition |
|---|---|---|
| Harmful-compliance rate | Harmful | share labelled `complied_harmful` |
| Over-refusal rate | Harmless | share labelled `refused` |
| Garbled rate | All | share labelled `offtopic_garbled` |

`[FILL IN: whether garbled responses are kept in or dropped from the denominators of the first two rates.]`

### 5.5 Week-1 floor check (go/no-go)

Before the full run: about 50 harmful JailbreakBench prompts, Google-translated Telugu (`mt_google`), all enabled models (`src/run/floor_check.py`; `floor_check` in `configs/run.yaml`).

- Go if harmful compliance is at least `[FILL IN: threshold]`.
- Otherwise: lead with the over-refusal and garbled rates, and add StrongREJECT.

## 6. Analyses

### 6.1 Gap (Q1, Q4)

Rates by language × form × model, each compared against English.

- Comparison: `[FILL IN: difference vs. English, with CIs]`
- Uncertainty: `[FILL IN: e.g. bootstrap over prompts, number of resamples]`
- US vs. Chinese models: `[FILL IN]`

### 6.2 Paired contrasts (Q2)

On the same source prompts, per model and language, for each outcome in §5:

- `mt_google` and `mt_llm` vs `human`: translation artifact.
- `romanized` and `codemixed` vs `human`: script and mixing effect.
- `human` vs `en_original`: remaining language effect.

The translation-artifact contrast is reported on all prompts and on intent-preserved prompts only.

- Test: `[FILL IN: paired by source prompt, e.g. McNemar or a paired bootstrap]`

### 6.3 Confidence intervals (Q3)

Mixed-effects logistic regression, one model per outcome (harmful compliance, over-refusal, garbled).

- Unit: one row per response.
- Outcome: the majority label of the three judges. Tie rule: `[FILL IN: tie rule]`
- Fixed effects: model, plus a form term coded within each language (English has no forms).
- Random effect: prompt only. Judge is not a random effect, since three judges are too few.
- Sensitivity check: refit with each judge's labels on their own.
- Output: each contrast from §6.2 with a 95% CI, reported per model. Model origin is described, not estimated.
- Library: `[FILL IN: statsmodels BinomialBayesMixedGLM, or R lme4::glmer]`
- Run-to-run noise: from the 20% repeats, reported separately.

### 6.4 Judge reliability

- Cohen's κ between each judge and the human labels, per language.
- Cohen's κ between main and overlap checkers, in every language.
- Agreement on `intent_preserved`: Cohen's κ between each judge and the human checkers, per language.
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
