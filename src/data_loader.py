import json
from src.config import FACTS_FILE

def load_verified_data():
    try:
        with open(FACTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # في حال عدم وجود الملف أو أخطاء قراءة، أرجع قاموس فارغ
        return {}
    except json.JSONDecodeError:
        return {}
