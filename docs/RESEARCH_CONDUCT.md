# Research Conduct

These rules apply to everyone working on this project. Where possible they are enforced in code; the right-hand column says how.

| Rule | How it's enforced |
|---|---|
| API and OpenRouter accounts are in Vinith Ayapilla's own name, never IEA's. | Manual |
| API keys live only in `.env`, which is never committed. | `.env` is gitignored; keys are read only via `src/config.py:api_key` |
| Public benchmark prompts only. | Prompts come only from the pinned public sources in `configs/sources.yaml` |
| The most severe weapons-related harm categories are excluded for every model. | `excluded_harm_categories` and `excluded_prompt_ids` in `configs/run.yaml`, applied by the loaders before anything is built |
| No iterating on jailbreaks. | Prompts are fixed benchmark items and their translations; nothing in the pipeline rewrites prompts based on model responses |
| Raw model responses and judge outputs are stored privately. Only aggregates and safe examples are published. | `outputs/` is gitignored |
| No personal data in prompts. OpenRouter batch requests can't use zero data retention. | Manual; translator brief tells translators not to add personal information |
| Translators and checkers get a content warning and can skip any prompt. | [TRANSLATOR_BRIEF.md](TRANSLATOR_BRIEF.md); every tracker sheet has a `skip` column |
| Human translations are done without AI or machine-translation tools. | Brief; `human` tracker sheets never include a machine draft |
| Runs use only finalized settings. | Submitting refuses while any setting in the configs is still a placeholder |
| The IEA work (non-public data) is completely separate. Nothing from it enters this repo. | Manual |
