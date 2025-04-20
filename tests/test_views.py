from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import main_page_view


@pytest.fixture
def fake_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Номер карты": ["1234", "5678", "1234"],
            "Сумма платежа": [100.0, 200.0, 300.0],
            "Дата операции": pd.to_datetime(["2022-12-01", "2022-12-15", "2022-12-20"]),
            "Категория": ["Еда", "Кафе", "Развлечения"],
            "Описание": ["Магазин", "Ресторан", "Кино"],
        }
    )


@patch("src.views.fetch_currency_rates", return_value=[{"currency": "USD", "rate": 70.0}])
@patch("src.views.fetch_stock_prices", return_value=[{"stock": "AAPL", "price": 150.0}])
@patch("src.views.get_user_settings", return_value={"user_currencies": ["USD"], "user_stocks": ["AAPL"]})
@patch("src.views.load_data")
@patch("src.views.filter_by_date")
def test_main_page_view_all(
    mock_filter: Any, mock_load: Any, mock_settings: Any, mock_stocks: Any, mock_rates: Any, fake_df: pd.DataFrame
) -> None:
    mock_load.return_value = fake_df
    mock_filter.return_value = fake_df

    result = main_page_view("2022-12-20 15:30:00")

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 2
    assert len(result["top_transactions"]) == 3
    assert result["currency_rates"][0]["rate"] == 70.0
    assert result["stock_prices"][0]["price"] == 150.0
