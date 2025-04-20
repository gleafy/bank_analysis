import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
import json
from typing import Any

from src.utils import (
    filter_by_date,
    get_greeting,
    get_user_settings,
    fetch_currency_rates,
    fetch_stock_prices,
)


def test_filter_by_date() -> None:
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime(["2021-05-01", "2021-05-15", "2021-06-01"])
    })
    result = filter_by_date(df, "2021-05-20 00:00:00")
    assert len(result) == 2


@pytest.mark.parametrize("hour,expected", [
    (8, "Доброе утро"),
    (14, "Добрый день"),
    (19, "Добрый вечер"),
    (2, "Доброй ночи"),
])
def test_get_greeting(hour: int, expected: str) -> None:
    dt = datetime(2021, 1, 1, hour)
    assert get_greeting(dt) == expected


def test_get_user_settings(tmp_path: Any) -> None:
    settings_path = tmp_path / "user_settings.json"
    settings_path.write_text(json.dumps({
        "user_currencies": ["USD"],
        "user_stocks": ["AAPL"]
    }), encoding="utf-8")

    result = get_user_settings(str(settings_path))
    assert result["user_currencies"] == ["USD"]
    assert result["user_stocks"] == ["AAPL"]


@patch("src.utils.requests.get")
@patch("src.utils.os.getenv", return_value="dummy_key")
def test_fetch_currency_rates(mock_env: Any, mock_get: Any) -> None:
    mock_get.return_value.json.return_value = {
        "rates": {"USD": 0.02, "EUR": 0.01}
    }

    result = fetch_currency_rates(["USD", "EUR"])
    assert result == [
        {"currency": "USD", "rate": 50.0},
        {"currency": "EUR", "rate": 100.0}
    ]


@patch("src.utils.requests.get")
@patch("src.utils.os.getenv", return_value="dummy_key")
def test_fetch_stock_prices(mock_env: Any, mock_get: Any) -> None:
    mock_get.return_value.json.return_value = {
        "Global Quote": {"05. price": "123.45"}
    }

    result = fetch_stock_prices(["AAPL"])
    assert result == [{"stock": "AAPL", "price": 123.45}]
