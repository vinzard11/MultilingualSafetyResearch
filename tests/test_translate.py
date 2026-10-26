"""Translator sheets, Google Translate batching, and the stubbed forms. No network."""

from unittest import mock

import pandas as pd
import pytest

from src import config
from src.data.versions import load_versions
from src.translate import codemix, mt_google, mt_llm, romanize, tracker


@pytest.fixture
def offline_tracker(fake_sources, tmp_outputs, monkeypatch):
    monkeypatch.setattr(tracker, "load_all", lambda: fake_sources)


def read_sheet(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")


def test_human_sheet_round_trip(offline_tracker):
    path = tracker.export_tracker("te", "human")
    sheet = read_sheet(path)
    assert len(sheet) == 3
    assert (sheet["draft"] == "").all()   # no machine drafts for human translators

    sheet.loc[0, "final_text"] = "అనువాదం"
    sheet.loc[1, "skip"] = "y"
    sheet.to_csv(path, index=False, encoding="utf-8-sig")
    assert tracker.import_tracker(path, "te", "human", "Tamil/Telugu translator") == 2

    v = load_versions().set_index("version_id")
    assert v.at["jbb-h000-te-human", "text"] == "అనువాదం"
    assert v.at["jbb-h000-te-human", "status"] == "final"
    assert v.at["jbb-h000-te-human", "translator"] == "Tamil/Telugu translator"
    assert v.at["jbb-b000-te-human", "status"] == "skipped"

    again = read_sheet(tracker.export_tracker("te", "human"))
    assert again.loc[0, "final_text"] == "అనువాదం" and again.loc[1, "skip"] == "y"


def test_romanized_sheet_only_has_finished_human_rows(offline_tracker):
    path = tracker.export_tracker("te", "human")
    sheet = read_sheet(path)
    sheet.loc[0, "final_text"] = "అనువాదం"
    sheet.to_csv(path, index=False, encoding="utf-8-sig")
    tracker.import_tracker(path, "te", "human", "Tamil/Telugu translator")

    rom = read_sheet(tracker.export_tracker("te", "romanized"))
    assert len(rom) == 1
    assert rom.loc[0, "reference_text"] == "అనువాదం"


def test_import_rejects_rows_from_another_sheet(offline_tracker):
    path = tracker.export_tracker("te", "human")
    with pytest.raises(ValueError, match="does not belong"):
        tracker.import_tracker(path, "ta", "human", "someone")


def test_mt_google_batches_and_keeps_order():
    class Resp:
        def __init__(self, texts):
            self.texts = texts
        def raise_for_status(self):
            pass
        def json(self):
            return {"data": {"translations": [{"translatedText": t.upper()} for t in self.texts]}}

    texts = [f"s{i}" for i in range(250)]
    with mock.patch.object(config, "api_key", return_value="k"), \
         mock.patch("requests.post", side_effect=lambda *a, **k: Resp(k["data"]["q"])) as post:
        out = mt_google.translate(texts, "te")
    assert post.call_count == 3
    assert out == [t.upper() for t in texts]


@pytest.mark.parametrize("call", [
    lambda: mt_llm.translate(["x"], "te"),
    lambda: romanize.romanize(["x"], "te"),
    lambda: codemix.draft_codemix(["x"], ["x"], "te"),
])
def test_undecided_tools_raise(call):
    with pytest.raises(NotImplementedError, match="not chosen yet"):
        call()
