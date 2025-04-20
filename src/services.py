import logging
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно было бы накопить в инвесткопилку.

    :param month: Месяц вида "YYYY-MM"
    :param transactions: Список транзакций
    :param limit: Шаг округления (например, 50)
    :return: Общая сумма округлений
    """
    result = 0.0
    for tx in transactions:
        try:
            tx_date = datetime.strptime(tx["Дата операции"], "%Y-%m-%d")
            if tx_date.strftime("%Y-%m") != month:
                continue
            amount = float(tx["Сумма операции"])
            if amount > 0:
                remainder = limit - (amount % limit)
                if remainder != limit:
                    result += remainder
        except Exception as e:
            logger.warning(f"Ошибка в транзакции: {e}")
    return round(result, 2)


def simple_search(query: str, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Выполняет поиск по описанию и категории транзакции.

    :param query: Поисковый запрос
    :param transactions: Список транзакций
    :return: Подходящие транзакции
    """
    result = []
    query = query.lower()
    for tx in transactions:
        if query in str(tx.get("Описание", "")).lower() or query in str(tx.get("Категория", "")).lower():
            result.append(tx)
    return result
