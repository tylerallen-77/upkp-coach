def test_learner_profile_persists_study_pattern(tmp_path, monkeypatch):
    from upkp import multi_store as store

    monkeypatch.setattr(store, "LOCAL_DB", tmp_path / "study-preferences.sqlite3")
    user = store.create_user("studyplan", "hash", "user")
    store.create_learner_profile(user["id"])

    profile = store.update_learner_profile(
        user["id"],
        "2026-12-01",
        {"tpa": "basic", "substansi": "intermediate"},
        60,
        "V",
        {},
        "standalone",
    )

    assert profile["study_pattern"] == "standalone"
