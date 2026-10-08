from pathlib import Path

def test_visual_v14_contract():
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    css=Path('app/globals.css').read_text(encoding='utf-8')
    icon=Path('app/icon.svg').read_text(encoding='utf-8')
    assert 'function MasterySeal' in page
    assert 'function ReadinessRing' in page
    assert 'function Account' in page
    for code in ['verbal','numerical','logical','figural','substansi_etika','substansi_wawasan','substansi_nilai','substansi_kepegawaian','substansi_keuangan','substansi_struktur']:
        assert code in page or ('seal-'+code) in css
    assert 'readinessRing' in css
    assert 'masteryGallery' in css
    assert '<svg' in icon and '#ffd23f' in icon