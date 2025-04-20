import json
import logging
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def save_report_to_file(default_name: str = "report.json") -> Callable:
    """
    Декоратор для сохранения результата функции в JSON-файл.

    :param default_name: Имя файла по умолчанию
    :return: Обёртка
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            filename = kwargs.get("filename", default_name)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return result

        return wrapper

    return decorator


@save_report_to_file("category_report.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """
    Рассчитывает сумму трат по категории за последние 3 месяца.

    :param transactions: DataFrame с транзакциями
    :param category: Название категории
    :param date: Дата отсчёта (по умолчанию — сегодня)
    :return: Словарь с итогом
    """
    parsed_date: datetime = pd.to_datetime(date) if date else datetime.today()
    start_date = parsed_date - pd.DateOffset(months=3)
    df_filtered = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]
    total = df_filtered["Сумма платежа"].sum()
    return {"category": category, "total_spent": round(float(total), 2)}
