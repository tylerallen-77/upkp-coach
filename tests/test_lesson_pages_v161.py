from pathlib import Path

def test_lesson_page_contract():
    page=Path('app/page.tsx').read_text(encoding='utf-8')
    css=Path('app/globals.css').read_text(encoding='utf-8')
    api=Path('api/index.py').read_text(encoding='utf-8')
    rich=Path('components/RichContent.tsx').read_text(encoding='utf-8')
    assert 'function LessonPage' in page
    assert '← Kembali ke daftar materi' in page
    assert 'LESSON MAP' in page
    assert 'Sumber & validasi materi' in page
    assert 'sourceDisclosure' in css
    assert 'lessonCardGrid' in css
    assert "'lesson_cards':lesson_cards.cards" in api
    assert '<em key={i}>' in rich

def test_formula_and_concept_cards_exist():
    from upkp import lesson_cards
    for code in ['operasi','persamaan','geometri','aritsos','banding','jarak','peluang','statistika','etika','kepegawaian','keuangan','struktur']:
        cards=lesson_cards.cards(code)
        assert cards
        assert all(c.get('title') and c.get('body') for c in cards)
    assert any(c.get('formula') for c in lesson_cards.cards('persamaan'))