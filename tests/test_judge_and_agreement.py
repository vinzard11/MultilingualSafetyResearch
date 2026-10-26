import pytest

from src.analysis.agreement import cohen_kappa
from src.judge.judge import PLACEHOLDERS, labels, parse_judgment, render_judge_prompt
from src.run import submit


def test_labels_are_the_four():
    assert labels() == ["refused", "complied_harmful", "complied_safe", "offtopic_garbled"]


def test_render_fills_every_slot():
    prompt = render_judge_prompt("ప్రశ్న", "question", "answer")
    assert not any(slot in prompt for slot in PLACEHOLDERS)
    assert "ప్రశ్న" in prompt and '{"label"' in prompt   # rubric's JSON example survives


@pytest.mark.parametrize("raw", [
    '{"label": "refused", "short_reason": "declines"}',
    '```json\n{"label": "refused", "short_reason": "declines"}\n```',
    'Here is my answer: {"label": "refused", "short_reason": "declines"}',
])
def test_parse_judgment(raw):
    assert parse_judgment(raw) == {"label": "refused", "short_reason": "declines"}


@pytest.mark.parametrize("raw, message", [
    ('{"label": "maybe"}', "invalid label"),
    ("no json here", "no JSON"),
])
def test_parse_judgment_rejects(raw, message):
    with pytest.raises(ValueError, match=message):
        parse_judgment(raw)


def test_kappa():
    assert cohen_kappa(list("abcd"), list("abcd")) == 1.0
    # observed 0.8, expected 0.32 -> 0.48 / 0.68
    assert cohen_kappa(list("aabbc"), list("aabcc")) == pytest.approx(0.48 / 0.68)
    with pytest.raises(ValueError):
        cohen_kappa(["a"], ["a", "b"])


def test_submit_refuses_while_settings_are_placeholders():
    with pytest.raises(RuntimeError, match="placeholders"):
        submit.submit("opus-5.5")
