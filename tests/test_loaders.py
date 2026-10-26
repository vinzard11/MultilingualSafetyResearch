import pandas as pd

from src.data.loaders import _stratified_ids, apply_exclusions


def test_stratified_sample_is_proportional_and_exact():
    cats = pd.Series(["a"] * 60 + ["b"] * 30 + ["c"] * 10,
                     index=[f"{i:03d}" for i in range(100)])
    picked = _stratified_ids(cats, n=10, seed=0)
    assert len(picked) == len(set(picked)) == 10
    assert cats[picked].value_counts().to_dict() == {"a": 6, "b": 3, "c": 1}


def test_stratified_sample_rounds_to_exact_total():
    cats = pd.Series(["a"] * 34 + ["b"] * 33 + ["c"] * 33, index=range(100))
    assert len(_stratified_ids(cats, n=10, seed=0)) == 10


def test_stratified_sample_is_reproducible():
    cats = pd.Series(["a"] * 50 + ["b"] * 50, index=range(100))
    assert _stratified_ids(cats, 10, seed=0) == _stratified_ids(cats, 10, seed=0)


def test_exclusions_by_category_and_id(fake_sources, override_config):
    override_config("run", excluded_harm_categories=["homonyms"], excluded_prompt_ids=["jbb:h000"])
    kept = apply_exclusions(fake_sources)
    assert set(kept["source_id"]) == {"b000", "000"}


def test_no_exclusions_keeps_everything(fake_sources):
    assert len(apply_exclusions(fake_sources)) == len(fake_sources)
