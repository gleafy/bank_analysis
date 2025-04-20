import json
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
import requests
import os

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_data(filepath: str) -> pd.DataFrame:
    """
    Загружает Excel-файл с транзакциями и преобразует даты.

    :param filepath: Путь к файлу
    :return: DataFrame с транзакциями
    """
    try:
        df = pd.read_excel(filepath)
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)
        return df
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        return pd.DataFrame()


def filter_by_date(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """
    Фильтрует транзакции с начала месяца до указанной даты.

    :param df: Все транзакции
    :param date_str: Дата в формате "YYYY-MM-DD HH:MM:SS"
    :return: Отфильтрованный DataFrame
    """
    try:
        target_date = pd.to_datetime(date_str)
        start_of_month = target_date.replace(day=1)
        filtered = df[(df['Дата операции'] >= start_of_month) & (df['Дата операции'] <= target_date)]
        return filtered
    except Exception as e:
        logger.error(f"Ошибка при фильтрации по дате: {e}")
        return pd.DataFrame()


def get_user_settings(filepath: str = "user_settings.json") -> Dict[str, List[str]]:
    """
    Загружает пользовательские настройки (валюты, акции).

    :param filepath: Путь к JSON-файлу
    :return: Словарь с настройками
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return dict(json.load(f))


def fetch_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют из внешнего API.

    :param currencies: Список валют
    :return: Курсы валют к рублю
    """
    url = f"http://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols={','.join(currencies)}"
    headers = {"apikey": os.getenv("EXCHANGE_API_KEY", "")}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return [{"currency": cur, "rate": round(1 / data["rates"][cur], 2)} for cur in currencies]
    except Exception as e:
        logger.warning(f"Не удалось получить курсы валют: {e}")
        return []


def fetch_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """
    Получает цены акций из API Alpha Vantage.

    :param stocks: Список тикеров
    :return: Список акций с ценами
    """
    result = []
    api_key = os.getenv("ALPHAVANTAGE_API_KEY", "")
    for stock in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            price = float(data["Global Quote"]["05. price"])
            result.append({"stock": stock, "price": round(price, 2)})
        except Exception as e:
            logger.warning(f"Ошибка получения данных по акции {stock}: {e}")
    return result


def get_greeting(dt: datetime) -> str:
    """
    Возвращает приветствие по времени суток.

    :param dt: Объект datetime
    :return: Строка приветствия
    """
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
