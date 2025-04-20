# Анализ банковских операций

Учебный проект для курсов по программированию. Приложение читает данные из Excel-файла с банковскими операциями, фильтрует их по дате и выводит сводную информацию: траты по картам, популярные транзакции, курсы валют и цены акций.

---

## Структура проекта

```
.
├── data
│   └── operations.xlsx        # Таблица с банковскими операциями
├── src                        # Основной код приложения
│   ├── main.py                # Точка входа
│   ├── views.py               # "Главная" страница
│   ├── utils.py               # Поддерживающие функции
│   ├── services.py            # Инвесткопилка и поиск
│   ├── reports.py             # Отчёты и генерация файлов
│   └── __init__.py
├── tests                      # Тесты
├── .env                       # Переменные окружения (API-ключи)
├── .env_template              # Шаблон для .env
├── pyproject.toml             # Настройки poetry, линтеров и форматтеров
├── .flake8                    # Настройки линтера
├── README.md                  # Этот файл
└── user_settings.json         # Настройки валют и акций
```

---

## Запуск проекта

1. Установите зависимости через Poetry:
   ```bash
   poetry install
   ```

2. Создайте `.env` на основе `.env_template`:
   ```env
   EXCHANGE_API_KEY=ваш_ключ_от_apilayer
   ALPHAVANTAGE_API_KEY=ваш_ключ_от_alphavantage
   ```

3. Запустите приложение:
   ```bash
   poetry run python -m src.main
   ```

4. Результат отобразится в консоли в формате JSON.

---

## Запуск тестов

```bash
poetry run pytest
```

С покрытием кода:
```bash
poetry run pytest --cov=src
```

---

## Переменные окружения

Файл `.env` должен содержать:

```env
EXCHANGE_API_KEY=ключ_для_exchange_rates_data_api
ALPHAVANTAGE_API_KEY=ключ_для_alpha_vantage
```

API-ключи можно получить бесплатно:
- [https://apilayer.com/marketplace/exchangerates_data-api](https://apilayer.com/marketplace/exchangerates_data-api)
- [https://www.alphavantage.co/](https://www.alphavantage.co/)

---

## Настройки пользователя

Файл `user_settings.json` позволяет указать интересующие валюты и акции:

```json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
```

---

## 🛠 Реализованные функции

- [x] "Главная" страница (приветствие, карты, транзакции, курсы, акции)
- [x] Инвесткопилка: расчёт накоплений
- [x] Простой поиск по операциям
- [x] Отчёт по тратам по категории за 3 месяца
- [x] Обращение к внешним API (валюты и акции)
- [x] Покрытие тестами всех функций
- [x] Настроенные линтеры: `flake8`, `isort`, `mypy`
- [x] Полная типизация, структура и документация