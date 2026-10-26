"""`mt_google` form: translate English prompts with the Google Translate API (v2).

    python -m src.translate.mt_google --language te

Needs GOOGLE_TRANSLATE_API_KEY in .env. Results go into the prompt-version
table with status `final`.
"""

import argparse

import requests

from src import config
from src.data.loaders import load_all
from src.data.versions import load_versions, save_versions, upsert
from src.translate.common import english_prompts, versions_from_texts

API_URL = "https://translation.googleapis.com/language/translate/v2"
BATCH_SIZE = 100   # the API accepts up to 128 segments per request


def translate(texts: list[str], target: str, source: str = "en") -> list[str]:
    key = config.api_key("GOOGLE_TRANSLATE_API_KEY")
    out = []
    for i in range(0, len(texts), BATCH_SIZE):
        resp = requests.post(
            API_URL,
            params={"key": key},
            data={"q": texts[i : i + BATCH_SIZE], "source": source, "target": target, "format": "text"},
            timeout=60,
        )
        resp.raise_for_status()
        out += [t["translatedText"] for t in resp.json()["data"]["translations"]]
    return out


def run(language: str) -> None:
    prompts = english_prompts(load_all())
    texts = translate(prompts["text"].tolist(), target=language)
    rows = versions_from_texts(prompts, language, "mt_google", texts, translator="google", status="final")
    save_versions(upsert(load_versions(), rows))
    print(f"mt_google {language}: {len(rows)} versions written")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--language", required=True, choices=config.load("languages")["target_languages"])
    run(parser.parse_args().language)
