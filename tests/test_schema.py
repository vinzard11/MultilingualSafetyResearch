from dataclasses import asdict

import pandas as pd
import pytest

from src.data.schema import (
    VERSION_COLUMNS, PromptVersion, allowed_forms, make_version_id, validate_versions,
)


def row(**changes):
    base = dict(
        version_id="jbb-h000-te-human", source="jbb", source_id="h000", harmful=True,
        harm_category="Privacy", language="te", form="human", text="అనువాదం",
        translator="Tamil/Telugu translator", status="final", notes="",
    )
    base.update(changes)
    return asdict(PromptVersion(**base))


def table(*rows):
    return pd.DataFrame(list(rows), columns=VERSION_COLUMNS)


def test_version_id_format():
    assert make_version_id("jbb", "h000", "te", "human") == "jbb-h000-te-human"


def test_valid_rows_pass():
    validate_versions(table(row(), row(version_id="jbb-h000-te-mt_google", form="mt_google")))


@pytest.mark.parametrize("changes, message", [
    (dict(version_id="wrong"), "version_id should be"),
    (dict(form="nonsense", version_id="jbb-h000-te-nonsense"), "unknown form"),
    (dict(language="en", version_id="jbb-h000-en-human"), "not allowed for language"),
    (dict(status="checked"), "unknown status"),
    (dict(text=""), "requires text"),
    (dict(harmful="yes"), "harmful must be bool"),
])
def test_invalid_rows_caught(changes, message):
    with pytest.raises(ValueError, match=message):
        validate_versions(table(row(**changes)))


def test_duplicate_ids_caught():
    with pytest.raises(ValueError, match="duplicate version_id"):
        validate_versions(table(row(), row()))


def test_pending_and_skipped_need_no_text():
    validate_versions(table(row(status="pending", text=""), row(
        version_id="jbb-b000-te-human", source_id="b000", status="skipped", text="")))


def test_wrong_columns_rejected():
    with pytest.raises(ValueError, match="columns must be"):
        validate_versions(table(row()).drop(columns="notes"))


def test_allowed_forms():
    forms = allowed_forms()
    assert forms["en_original"] == {"en"}
    assert forms["native_indicsafe"] == {"te", "ta", "hi"}
    for form in ("mt_google", "mt_llm", "human", "romanized", "codemixed"):
        assert forms[form] == {"te", "ta", "hi"}
