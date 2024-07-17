import numpy as np
import pytest

from transformer import HtmlTransformer


class TestTransformer:
    @staticmethod
    @pytest.fixture
    def input_html() -> str:
        with open('tests/input.html') as f:
            return f.read()

    def test_run_expect_dict(self, input_html: str) -> None:
        # arrange
        transformer = HtmlTransformer(input_html)
        # act
        result = transformer.run()
        # assert
        assert result == {
            'Взыскатель': 'АО "Тинькофф Банк"',
            'Вступило в силу': '18.05.2024',
            'Дата документа': '29.03.2024',
            'Дата размещения': '29.03.2024',
            'Должник': 'Миндрина И.Ю.',
            'Зарегистрировано': '29.03.2024',
            'Категория дела': 'О выдаче дубликата судебного приказа',
            'Судебный участок': '1',
            'Судопроизводство': 'Гражданское',
            'Судья': 'Стась Л.В.',
            'Текущее состояние': 'Вступило в силу (18.05.2024)',
            'Третье лицо': 'ОСП по Абанскому району',
            'УИД': '24MS0001-01-2022-001127-18',
            'Удовлетворено': '22.04.2024',
            '№ дела': '13-0247/1/2024',
            '№ заявления': np.nan,
        }
