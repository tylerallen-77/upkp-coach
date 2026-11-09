import time


def test_learner_profile_persists_study_pattern_and_unbounded_daily_minutes(tmp_path, monkeypatch):
    from upkp import multi_store as store

    monkeypatch.setattr(store, "LOCAL_DB", tmp_path / "study-preferences.sqlite3")
    user = store.create_user("studyplan", "hash", "user")
    store.create_learner_profile(user["id"])

    profile = store.update_learner_profile(
        user["id"],
        "2026-12-01",
        {"tpa": "basic", "substansi": "intermediate"},
        360,
        "V",
        {},
        "standalone",
    )

    assert profile["daily_minutes"] == 360
    assert profile["study_pattern"] == "standalone"
