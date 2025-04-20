import pandas as pd
import json
from src.reports import spending_by_category
from typing import Any


def test_spending_by_category_creates_file(tmp_path: Any) -> None:
    df = pd.DataFrame({
        "Дата операции": pd.to_datetime([
            "2023-12-01", "2023-11-01", "2023-10-01"
        ]),
        "Категория": ["Еда", "Еда", "Кафе"],
        "Сумма платежа": [100, 200, 300]
    })

    result = spending_by_category(df, "Еда", "2023-12-31")
    assert result == {"category": "Еда", "total_spent": 300.0}

    report_file = tmp_path / "category_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
