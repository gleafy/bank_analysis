import json

from src.views import main_page_view

if __name__ == "__main__":
    result = main_page_view("2022-12-20 15:30:00")
    print(json.dumps(result, indent=2, ensure_ascii=False))
