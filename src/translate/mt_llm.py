"""`mt_llm` form: translate English prompts with an LLM via OpenRouter.

STUB. The translation model is an open decision
(configs/languages.yaml: translated_forms.mt_llm.model).
"""

from src import config


def translation_model() -> str:
    model = config.load("languages")["translated_forms"]["mt_llm"]["model"]
    if not model:
        raise NotImplementedError(
            "mt_llm model is not chosen yet: set translated_forms.mt_llm.model in configs/languages.yaml"
        )
    return model


def translate(texts: list[str], target: str) -> list[str]:
    translation_model()
    # TODO: fix the translation prompt wording, then call OpenRouter
    # (batch where available). Rows get translator=f"llm:{model}", status "final".
    raise NotImplementedError("mt_llm translation is not implemented yet")
