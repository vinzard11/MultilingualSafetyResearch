"""Prompt-version table and batch building, on fake sources."""

from src.data.versions import load_versions, save_versions, upsert
from src.run import build_batches, build_versions


def test_skeleton_counts(fake_sources):
    sk = build_versions.skeleton(fake_sources)
    # 3 English prompts x (1 original + 3 languages x 5 forms) + 1 IndicSafe x 3 languages
    assert len(sk) == 3 * 16 + 3
    assert set(sk.loc[sk["form"].isin(["en_original", "native_indicsafe"]), "status"]) == {"final"}
    assert set(sk.loc[~sk["form"].isin(["en_original", "native_indicsafe"]), "status"]) == {"pending"}


def test_rebuild_never_overwrites_work(fake_sources, tmp_outputs, monkeypatch):
    monkeypatch.setattr(build_versions, "load_all", lambda: fake_sources)
    build_versions.run()
    v = load_versions()
    v.loc[v["version_id"] == "jbb-h000-te-human", ["text", "status"]] = ["అనువాదం", "final"]
    save_versions(v)

    build_versions.run()
    after = load_versions().set_index("version_id")
    assert len(after) == 51
    assert after.at["jbb-h000-te-human", "text"] == "అనువాదం"


def test_save_load_round_trip(fake_sources, tmp_outputs):
    sk = build_versions.skeleton(fake_sources)
    save_versions(sk)
    back = load_versions()
    assert back["harmful"].tolist() == sk["harmful"].tolist()
    assert "తెలుగు" in back["text"].tolist()


def test_upsert_replaces_and_appends(fake_sources):
    sk = build_versions.skeleton(fake_sources)
    changed = sk.iloc[[0]].assign(notes="changed")
    out = upsert(sk, changed)
    assert len(out) == len(sk)
    assert out.set_index("version_id").at[changed["version_id"].iloc[0], "notes"] == "changed"


def all_final(sources):
    sk = build_versions.skeleton(sources)
    pending = sk["status"] == "pending"
    sk.loc[pending, "text"] = "fake translation"
    sk.loc[pending, "status"] = "final"
    return sk


def test_planned_requests_counts(fake_sources, monkeypatch):
    monkeypatch.setattr(build_batches, "load_all", lambda: fake_sources)
    plan = build_batches.planned_requests(all_final(fake_sources))
    pairs = 51 * 2
    assert (plan["repeat"] == 0).sum() == pairs
    assert (plan["repeat"] == 1).sum() == round(pairs * 0.2)


def test_planned_requests_skip_unfinished_and_excluded(fake_sources, monkeypatch):
    versions = build_versions.skeleton(fake_sources)          # translations still pending
    kept = fake_sources[fake_sources["source_id"] != "h000"]  # as if h000 were excluded
    monkeypatch.setattr(build_batches, "load_all", lambda: kept)
    plan = build_batches.planned_requests(versions)
    ids = set(plan["version_id"])
    assert "jbb-h000-en-en_original" not in ids
    assert "jbb-b000-te-human" not in ids
    assert ids == {"jbb-b000-en-en_original", "xstest-001-en-en_original",
                   "indicsafe-000-te-native_indicsafe", "indicsafe-000-ta-native_indicsafe",
                   "indicsafe-000-hi-native_indicsafe"}


def test_repeat_subset_is_reproducible(fake_sources, monkeypatch):
    monkeypatch.setattr(build_batches, "load_all", lambda: fake_sources)
    versions = all_final(fake_sources)
    a = build_batches.planned_requests(versions)
    b = build_batches.planned_requests(versions)
    assert a.equals(b)


def test_render_templates():
    t1 = build_batches.render({"system": None, "user": "{prompt}"}, "hello")
    assert t1 == [{"role": "user", "content": "hello"}]
    t2 = build_batches.render({"system": "Be helpful.", "user": "{prompt}"}, "hello")
    assert t2[0] == {"role": "system", "content": "Be helpful."}


def test_request_body_drops_unset_and_pins_provider():
    model = {"openrouter_id": "x/y", "reasoning": None, "provider": "SomeProvider"}
    body = build_batches.request_body(model, [{"role": "user", "content": "hi"}])
    assert "temperature" not in body and "reasoning" not in body
    assert body["provider"] == {"order": ["SomeProvider"], "allow_fallbacks": False}


def test_placeholders_are_reported():
    missing = build_batches.unset_settings({"m": {"openrouter_id": None, "provider": "p", "reasoning": None}})
    assert "run.temperature" in missing
    assert "models.m.openrouter_id" in missing and "models.m.reasoning" in missing
    assert "models.m.provider" not in missing
