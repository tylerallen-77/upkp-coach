from pathlib import Path

def test_v141_mastery_and_material_contract():
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    css=Path('app/globals.css').read_text(encoding='utf-8')
    rich=Path('components/RichContent.tsx').read_text(encoding='utf-8')
    api=Path('api/index.py').read_text(encoding='utf-8')
    assert "['materials','Materi']" in page
    assert 'function Materials' in page
    assert 'function BadgeGlyph' in page
    assert "const code:any" not in page
    assert 'sealProgress' in page and '--progress' in page
    for icon_case in ['verbal','numerical','logical','figural','substansi_etika','substansi_wawasan','substansi_nilai','substansi_kepegawaian','substansi_keuangan']:
        assert icon_case in page
    assert 'richH3' in rich and 'richCallout' in rich and 'richList' in rich
    assert 'source_status_label' in api and 'verified_at' in api
    assert 'materialGrid' in css and 'lessonToolbar' in css

def test_material_metadata_exists_for_all_substansi():
    from upkp.material_meta import metadata
    for code in ['etika','wawasan','nilai','kepegawaian','keuangan','struktur']:
        m=metadata(code,'umum')
        assert m['status']
        assert m['status_label']
        assert m['note']
