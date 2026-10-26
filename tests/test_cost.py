"""Run counts and the cost estimator against hand-computed check figures."""

import pytest

from src.cost.estimate import estimate, planned_counts


def test_counts_with_seven_models():
    c = planned_counts(7)
    assert c["english_prompts"] == 450
    assert c["prompt_versions"] == 7_500        # 450 x 16 + 300
    assert c["with_templates"] == 15_000
    assert c["responses_per_model"] == 18_000
    assert c["responses"] == 126_000
    assert c["judgments"] == 378_000


def test_counts_follow_model_count():
    assert planned_counts(5)["responses"] == 90_000
    assert planned_counts(5)["judgments"] == 270_000


def test_default_excludes_disabled_argon():
    est = estimate()
    assert "gemini-4-argon" not in est["models"]
    assert len(est["models"]) == 6
    assert est["total"] == pytest.approx(3_091.93, abs=0.01)


def test_with_argon_matches_check_figures():
    est = estimate(include=("gemini-4-argon",))
    assert len(est["models"]) == 7
    # Hand-computed check figures, rounded to the dollar.
    expected_generation = {"opus-5.5": 263, "gemini-4-argon": 263, "gpt-6.1-sol": 132,
                           "muse-spark-open": 114, "kimi-k3": 368, "qwen3.8-max": 162, "glm-5.3": 36}
    for key, usd in expected_generation.items():
        assert est["generation"][key] == pytest.approx(usd, abs=1)
    for key, usd in {"opus-5.5": 441, "gpt-6.1-sol": 220, "qwen3.8-max": 365}.items():
        assert est["judges"][key] == pytest.approx(usd, abs=1)
    assert est["total"] == pytest.approx(3_750, abs=25)


def test_batch_discount_applies_only_to_batch_models(override_config):
    base = estimate()
    override_config("models", batch_discount=0.0)
    no_discount = estimate()
    assert no_discount["generation"]["opus-5.5"] == pytest.approx(2 * base["generation"]["opus-5.5"])
    assert no_discount["generation"]["kimi-k3"] == pytest.approx(base["generation"]["kimi-k3"])
