from pathlib import Path

def test_official_2026_track_structure():
    from upkp import curriculum, mastery
    from upkp.skill_catalog import BADGE_SKILLS
    assert curriculum.SUBTES['Tes Potensi']==['Verbal','Numerikal','Figural']
    assert mastery.SECTION_ORDER==['verbal','numerical','figural']
    assert 'logika.silogisme_quantifier' in BADGE_SKILLS['verbal']

def test_deep_course_coverage_and_tskkwk_validation():
    from upkp import course_materials, official_sources
    expected={'padanan','kelompok','silogisme','analisis','operasi','persamaan','geometri','aritsos','sudut','banding','jarak','peluang','statistika','deret','deretfig','analogifig','etika','wawasan','nilai','kepegawaian','keuangan','struktur'}
    assert expected.issubset(set(course_materials.MODULES))
    assert official_sources.VALIDATION['validated_at']=='2026-10-08'
    assert set(official_sources.TSKKWK_SOURCES)=={'etika','wawasan','nilai','kepegawaian','keuangan','struktur'}
    assert any('PMK 117/2025' in x['name'] for x in official_sources.TSKKWK_SOURCES['struktur'])

def test_no_legacy_public_branding():
    for path in ['app/page.tsx','api/index.py','upkp/curriculum.py','upkp/materi.py','upkp/material_meta.py']:
        text=Path(path).read_text(encoding='utf-8')
        assert 'Anak UPKP' not in text
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    assert '>TPA<' not in page
    assert '>Substansi<' not in page
    assert 'Tes Potensi' in page and 'TSKKWK' in page