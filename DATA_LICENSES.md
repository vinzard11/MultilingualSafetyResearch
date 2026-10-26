# Data Licenses

This repository does not contain copies of the source datasets. They are downloaded at runtime from the pinned revisions in [configs/sources.yaml](configs/sources.yaml).

| Dataset | What we use | License | Source |
|---|---|---|---|
| JailbreakBench (JBB-Behaviors) | 100 harmful + 100 matched harmless behaviors | MIT | [huggingface.co/datasets/JailbreakBench/JBB-Behaviors](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors) |
| XSTest | 250 safe prompts that sound unsafe | CC BY 4.0 | [github.com/paul-rottger/xstest](https://github.com/paul-rottger/xstest) |
| IndicSafe | 100 prompts per language in Telugu, Tamil, Hindi, used as-is | **Data CC BY-NC 4.0**; code MIT | [github.com/ppattnayak/indicsafe](https://github.com/ppattnayak/indicsafe) |

## IndicSafe: non-commercial

IndicSafe's data is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). **Anything we publish that is derived from IndicSafe prompts keeps CC BY-NC 4.0, with attribution.** That covers prompt lists, examples, and per-item results. It may not be used commercially.

## Translations

Our translations of JailbreakBench and XSTest prompts (machine, human, romanized and code-mixed) are derived works. They carry the attribution requirements of their source licenses (MIT, CC BY 4.0).

## Citations

- Chao, P., Debenedetti, E., Robey, A., et al. *JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models.* NeurIPS Datasets and Benchmarks Track, 2024.
- Röttger, P., Kirk, H. R., Vidgen, B., et al. *XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models.* NAACL, 2024.
- Pattnayak, P., and Chowdhuri, S. *IndicSafe: A Benchmark for Evaluating Multilingual LLM Safety in South Asia.* arXiv:2603.17915, 2026.

## Code

The code license for this repository will be added before it goes public.
