from datetime import datetime
from .utils import (
    load_data, filter_by_date, get_user_settings,
    fetch_currency_rates, fetch_stock_prices, get_greeting
)


def main_page_view(date_str: str) -> dict:
    """
    Формирует JSON-ответ для главной страницы на основе даты.

    :param date_str: Дата в формате "YYYY-MM-DD HH:MM:SS"
    :return: Словарь с итогами: приветствие, карты, топ транзакции, курсы, акции
    """
    df = load_data("data/operations.xlsx")
    df_filtered = filter_by_date(df, date_str)
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    cards_info = []
    for card, group in df_filtered.groupby("Номер карты"):
        total = abs(group["Сумма платежа"].sum())
        cashback = round(total * 0.01, 2)
        cards_info.append({
            "last_digits": str(card)[-4:],
            "total_spent": round(total, 2),
            "cashback": cashback
        })

    top_tx = df_filtered.sort_values("Сумма платежа", ascending=False).head(5)

    top_transactions = []
    for _, row in top_tx.iterrows():
        top_transactions.append({
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"]
        })

    settings = get_user_settings()
    currency_rates = fetch_currency_rates(settings.get("user_currencies", []))
    stock_prices = fetch_stock_prices(settings.get("user_stocks", []))

    return {
        "greeting": get_greeting(dt),
        "cards": cards_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
