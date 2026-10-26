# Cross-Lingual Safety Gaps

**How much of the gap in LLM safety behavior across languages comes from translation artifacts, and how much from the language itself? And does this differ between US and Chinese models?**

An ongoing personal research project. We test 7 models on the same requests in English, Telugu, Tamil and Hindi. Each prompt comes in several forms: Google-translated, LLM-translated, human-translated, romanized and code-mixed. Three judges from different model families label every response. A generalizability-theory study (G-study) then splits the variance in safety outcomes across language, prompt form, model, template, harm category, judge and run.

> **Status: setup.** The design, configs, data loaders, schema, judge rubric, cost estimator and pipeline skeleton are in place. **No models have been evaluated yet.** The analysis plan will be fixed before any results exist.

## Research questions

1. **Gap:** For the same request, how much do refusal and harmful-output rates differ across languages, and between US and Chinese models?
2. **Translation artifacts:** How much of the gap is translation artifact versus the language itself? We compare machine-translated (Google, LLM) and human-translated prompts, plus romanized and code-mixed versions.
3. **Variance breakdown:** How much variance does each factor explain? This is the G-study.
4. **Over-refusal:** Does refusing harmless prompts also vary by language?

The full design is in [docs/DESIGN.md](docs/DESIGN.md), and the pre-registration template is in [docs/ANALYSIS_PLAN.md](docs/ANALYSIS_PLAN.md).

## Design at a glance

| | |
|---|---|
| Languages | English (source), Telugu, Tamil, Hindi |
| Prompts | JailbreakBench (100 harmful + 100 matched harmless), XSTest (250 safe-but-unsafe-sounding), IndicSafe (100 per language, used as-is) |
| Forms per language | `mt_google`, `mt_llm`, `human`, `romanized`, `codemixed` |
| Templates | T1 (user message only), T2 (generic system prompt + user message) |
| Models | Claude Opus 5.5, GPT-6.1-sol, Gemini 4 Argon (optional), Muse Spark Open, Kimi K3, Qwen3.8-Max, GLM-5.3, all via OpenRouter |
| Judges | Claude Opus 5.5, GPT-6.1-sol, Qwen3.8-Max; each scores every response, without seeing which model wrote it |
| Labels | `refused`, `complied_harmful`, `complied_safe`, `offtopic_garbled` |
| Human validation | ~400 responses per language, with a 100-response overlap checked by a second person |
| Scale (7 models) | 7,500 prompt versions × 2 templates + 20% repeats = 18,000 responses per model; 126,000 responses; 378,000 judgments |

## Repository layout

```
configs/      models, run settings, templates, judges + rubric, languages, sources
docs/         design, analysis plan, translator brief, research conduct
src/
  data/       dataset loaders, prompt-version schema and table
  translate/  Google and LLM translation, romanization, code-mixing, translator sheets
  run/        build prompt versions, build batch files, submit/poll/collect
  judge/      judge prompts and label parsing
  validate/   sampling for human checks, importing them
  analysis/   rates, form comparisons, G-study, agreement
  cost/       cost estimator
tests/
outputs/      private, gitignored: prompt versions, batches, responses, judgments
```

What is implemented and what is still a stub:

| Implemented | Stub (clear TODOs) |
|---|---|
| Dataset loaders (pinned revisions), schema and validation | LLM translation, romanization, code-mix drafting (tools not chosen yet) |
| Google Translate form | Submitting, polling and collecting OpenRouter batches |
| Translator sheet export and import | Building judge batches |
| Prompt-version table, batch file builder | Validation sampling and import |
| Judge prompt rendering and label parsing | Rates, form comparisons, G-study |
| Cost estimator, Cohen's κ | |

## How to run

Requires Python 3.10+.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env               # add your own keys; .env is never committed

python -m src.data.loaders         # download sources (cached in data_cache/) and print counts
python -m src.cost.estimate        # API cost from the configs
python -m src.run.build_versions   # create outputs/prompt_versions.csv (7,500 rows)

python -m src.translate.mt_google --language te                    # needs GOOGLE_TRANSLATE_API_KEY
python -m src.translate.tracker export --language te --form human  # sheet for the translator
python -m src.translate.tracker import outputs/trackers/te_human.csv

python -m src.run.build_batches    # one request file per model in outputs/batches/ (sends nothing)
pytest
```

Submitting batches refuses to run while any setting in the configs is still a placeholder.

## Data and licenses

Source datasets are downloaded at runtime from pinned revisions and are not committed. **IndicSafe data is CC BY-NC 4.0, and anything derived from it keeps that license with attribution.** Details and citations are in [DATA_LICENSES.md](DATA_LICENSES.md). The code is MIT-licensed; see [LICENSE](LICENSE).

Raw model responses and judge outputs stay private. Only aggregates and safe examples will be published. See [docs/RESEARCH_CONDUCT.md](docs/RESEARCH_CONDUCT.md).

## Team

- **Vinith Ayapilla**, researcher
- **Bilingual researcher and translator** (Tamil, Telugu), translation and checks
- A Hindi translator and checker, and a second Tamil checker for the overlap sample
