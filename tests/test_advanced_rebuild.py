import random
from upkp.advanced_tpa import ADVANCED_SKILLS, generate
from upkp.content_qa import validate_question, audit_advanced
from upkp.final_core import build_mastery_challenge


def test_all_advanced_skills_generate_clean():
    rng=random.Random(42)
    for skill in ADVANCED_SKILLS:
        for lv in (4,5):
            q=generate(skill,lv,rng)
            assert q is not None, skill
            assert q.lv==lv
            assert not validate_question(q), (skill, validate_question(q))


def test_data_interpretation_is_table_based():
    q=generate('numerik.data_interpretation',4,random.Random(2))
    assert '| Unit | Tahun 1 | Tahun 2 |' in q.stem
    assert q.skill=='numerik.data_interpretation'


def test_figural_matrix_has_rich_visual_payload():
    q=generate('figural.matrix_transform',4,random.Random(3))
    assert '<svg' in q.svg
    assert len(q.opt_svgs)==5
    assert all('<svg' in x for x in q.opt_svgs)
    assert q.skill=='figural.matrix_transform'


def test_each_mastery_challenge_has_hard_transfer():
    for section in ('verbal','numerical','logical','figural'):
        qs=build_mastery_challenge(section,seed=11)
        assert len(qs)==15
        assert all(q['lv']>=3 for q in qs)
        assert sum(q['lv']>=4 for q in qs)>=4


def test_advanced_audit_gate():
    r=audit_advanced(samples_per_skill=8,seed=99)
    assert r['ok'], r['issues'][:5]
    assert r['sampled']>=len(ADVANCED_SKILLS)*8


def test_first_diagnostic_spans_foundation_standard_exam():
    from upkp.final_core import build_prescription
    rx,qs=build_prescription('tpa',[],seed=123)
    levels={q['lv'] for q in qs}
    assert {1,2,3}.issubset(levels), levels


def test_targeted_advanced_skill_does_not_fallback_to_legacy_skill():
    from upkp.final_core import build_for_skill
    qs=build_for_skill('verbal.critical_inference',5,[],level=1,seed=5)
    assert len(qs)==5
    assert all(q.skill=='verbal.critical_inference' for q in qs)
    assert all(q.lv>=4 for q in qs)
