from src.views import main_page_view
import json

if __name__ == "__main__":
    result = main_page_view("2018-02-10 12:06:09")
    print(json.dumps(result, indent=2, ensure_ascii=False))
