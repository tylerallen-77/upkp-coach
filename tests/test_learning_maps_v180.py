from pathlib import Path

def test_learning_map_ui_contract():
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    css=Path('app/globals.css').read_text(encoding='utf-8')
    for marker in ['function LearningMap','function MapDetail','Peta TSKKWK','Formula & Strategy Map','JEMBATAN INGATAN','RUMUS UTAMA','Buka lesson lengkap','Drill node ini']:
        assert marker in page
    assert 'learningMap' in css and 'mapBranches' in css and 'mapDetail' in css

def test_map_data_is_available_from_catalog_layers():
    from upkp import study_tools, lesson_cards
    assert study_tools.formulas('persamaan')
    assert study_tools.formulas('peluang')
    assert study_tools.mnemonics('kepegawaian')
    assert study_tools.mnemonics('keuangan')
    assert lesson_cards.cards('struktur')

def test_mobile_map_layout_exists():
    css=Path('app/globals.css').read_text(encoding='utf-8')
    assert '@media(max-width:640px)' in css
    assert '.tskChildren{grid-template-columns:1fr}' in css