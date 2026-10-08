import time
from pathlib import Path

def _a(skill='numerik.ratio', correct=False, error='wrong', bab='banding', elapsed=50000, target=45000, confidence=''):
    return {'skill':skill,'correct':correct,'skipped':False,'level':2,'elapsed_ms':elapsed,'target_ms':target,
            'ts':time.time(),'session_id':'s','track':'tpa','bab':bab,'error_type':error,'confidence':confidence}

def test_teacher_plan_prioritizes_misconception():
    from upkp import learning
    rows=[_a(False) for _ in range(3)]
    rows=[
        _a(correct=False,error='high_confidence_wrong',confidence='yakin'),
        _a(correct=False,error='wrong'),
        _a(correct=True,error='slow_correct',elapsed=65000),
        _a(correct=True,error='clean_correct',elapsed=30000),
    ]
    plan=learning.teacher_plan(rows,'tpa')
    assert plan['focus'] is not None
    assert plan['focus']['chapter']=='banding'
    assert plan['focus']['mode'] in ('relearn','concept')
    assert plan['success_criteria']

def test_chapter_coaching_distinguishes_unseen_and_speed():
    from upkp import learning
    unseen=learning.chapter_coaching([],'banding','tpa')
    assert unseen['recommended']=='warmup'
    rows=[_a(correct=True,error='slow_correct',elapsed=70000) for _ in range(6)]
    coached=learning.chapter_coaching(rows,'banding','tpa')
    assert coached['recommended']=='speed'

def test_teacher_ui_contract():
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    css=Path('app/globals.css').read_text(encoding='utf-8')
    runner=Path('components/QuestionRunner.tsx').read_text(encoding='utf-8')
    for marker in ['TEACHER MODE','DIAGNOSIS COACH','MISTAKE CLINIC','ACTIVE RECALL','5 soal pemanasan','Uji pemahaman']:
        assert marker in page
    assert 'teacherBoard' in css and 'recallCheck' in css
    assert 'COACH NOTE' in runner
