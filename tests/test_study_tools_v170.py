from pathlib import Path

def test_study_tools_cover_all_lessons():
    from upkp import study_tools
    all_codes={'padanan','kelompok','silogisme','analisis','operasi','persamaan','geometri','aritsos','sudut','banding','jarak','peluang','statistika','deret','deretfig','analogifig','etika','wawasan','nilai','kepegawaian','keuangan','struktur'}
    assert all_codes.issubset(set(study_tools.READING_LENS))
    numerical={'operasi','persamaan','geometri','aritsos','sudut','banding','jarak','peluang','statistika','deret'}
    for code in numerical:
        assert len(study_tools.formulas(code))>=2
    for code in {'etika','wawasan','nilai','kepegawaian','keuangan','struktur'}:
        assert study_tools.mnemonics(code)

def test_hint_evidence_is_discounted():
    import time
    from upkp import learning
    base={'skill':'numerik.operasi_bilangan','correct':True,'skipped':False,'level':2,'elapsed_ms':30000,'target_ms':45000,'ts':time.time(),'error_type':'clean_correct'}
    unassisted=learning.profile_attempts([{**base,'hint_level':0} for _ in range(6)])[0]
    assisted=learning.profile_attempts([{**base,'hint_level':3} for _ in range(6)])[0]
    assert unassisted['mastery']>assisted['mastery']

def test_ui_has_read_model_solve_check_and_progressive_hints():
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    runner=Path('components/QuestionRunner.tsx').read_text(encoding='utf-8')
    api=Path('api/index.py').read_text(encoding='utf-8')
    for marker in ['CARA MEMBACA SOAL','Baca → Modelkan → Kerjakan → Cek','FORMULA HANDBOOK','JEMBATAN INGATAN']:
        assert marker in page
    assert 'Buka Hint' in runner and 'hint_level:hintLevel' in runner
    assert "item['hints']" in api

def test_tskkwk_regulation_deep_dives():
    from upkp import regulation_deepdives
    for code in ['etika','wawasan','nilai','kepegawaian','keuangan','struktur']:
        assert len(regulation_deepdives.get(code))>200