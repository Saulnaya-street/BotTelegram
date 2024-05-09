import requests
import json
from config import keys

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")
        
        try:
            base_key = keys[base]
            quote_key = keys[quote]
            amount = float(amount)
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {base} или {quote}.")
        except ValueError:
            raise APIException("Не удалось обработать количество.")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
        price = json.loads(r.content)[quote_key]
        return price * amount