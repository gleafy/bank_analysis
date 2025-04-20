import pytest
from typing import Any, Dict, List
from src.services import investment_bank, simple_search


@pytest.fixture
def example_transactions() -> List[Dict[str, Any]]:
    return [
        {"Дата операции": "2023-12-01", "Сумма операции": 123},
        {"Дата операции": "2023-12-15", "Сумма операции": 200},
        {"Дата операции": "2023-11-01", "Сумма операции": 50}
    ]


def test_investment_bank(example_transactions: List[Dict[str, Any]]) -> None:
    result = investment_bank("2023-12", example_transactions, 100)
    # 123 -> 77, 200 -> 0 => всего 77
    assert result == 77.0


def test_simple_search_found() -> None:
    transactions = [
        {"Описание": "Покупка в магазине", "Категория": "Продукты"},
        {"Описание": "Перевод", "Категория": "Переводы"},
    ]
    result = simple_search("магазин", transactions)
    assert len(result) == 1
    assert result[0]["Категория"] == "Продукты"


def test_simple_search_not_found() -> None:
    transactions = [
        {"Описание": "Оплата", "Категория": "Услуги"}
    ]
    result = simple_search("такси", transactions)
    assert result == []
