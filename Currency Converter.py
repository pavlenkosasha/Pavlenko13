import json
import time
import requests
import telebot
from telebot import types
import logging

# ----------------- Налаштування -----------------
TOKEN = ("8697005504:AAHVMIzGevFZeyVhAypGHnoOfm8Al-TJ2hk")
bot = telebot.TeleBot(TOKEN)
HISTORY_FILE = "history.json"

# ----------------- Конвертер валют -----------------
class CurrencyAPI:
    def __init__(self):
        self.rates = None
        self.last_update = 0
        self.update_interval = 600  # 10 хвилин

    def get_rates(self):
        current_time = time.time()
        if self.rates is None or current_time - self.last_update > self.update_interval:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url)
            data = response.json()
            self.rates = data["rates"]
            self.last_update = current_time
        return self.rates

class CurrencyConverter:
    def __init__(self, api):
        self.api = api

    def convert(self, amount, from_currency, to_currency):
        rates = self.api.get_rates()
        if from_currency not in rates:
            raise ValueError(f"Валюта {from_currency} не знайдена")
        if to_currency not in rates:
            raise ValueError(f"Валюта {to_currency} не знайдена")
        amount_in_usd = amount / rates[from_currency]
        result = amount_in_usd * rates[to_currency]
        return result

api = CurrencyAPI()
converter = CurrencyConverter(api)

# ----------------- Збереження історії -----------------
def save_to_history(user_id, request):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}

    if str(user_id) not in history:
        history[str(user_id)] = []

    history[str(user_id)].append({
        "time": time.time(),
        "request": request
    })

    # Зберігаємо лише останні 10 запитів
    history[str(user_id)] = history[str(user_id)][-10:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def get_history(user_id):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        user_history = history.get(str(user_id), [])
        if not user_history:
            return "Історія порожня"
        lines = []
        for h in user_history:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(h["time"]))
            lines.append(f"{t}: {h['request']}")
        return "\n".join(lines)
    except FileNotFoundError:
        return "Історія порожня"

# ----------------- Команда /start -----------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    usd_button = types.KeyboardButton("USD")
    eur_button = types.KeyboardButton("EUR")
    uah_button = types.KeyboardButton("UAH")
    markup.add(usd_button, eur_button, uah_button)

    bot.send_message(
        message.chat.id,
        "Привіт! Я бот для конвертації валют.\n"
        "Щоб конвертувати, використай команду:\n"
        "/convert сумма ВИХІДНА_ВАЛЮТА ЦІЛЬОВА_ВАЛЮТА\n"
        "Наприклад: /convert 980 UAH USD\n\n"
        "Можна також переглянути останні 10 конвертацій командою /history\n"
        "Або обери цільову валюту за допомогою кнопок нижче.",
        reply_markup=markup
    )

# ----------------- Команда /convert -----------------
@bot.message_handler(commands=['convert'])
def convert_currency(message):
    parts = message.text.split()
    if len(parts) != 4:
        bot.send_message(
            message.chat.id,
            "Формат: /convert сумма ВИХІДНА_ВАЛЮТА ЦІЛЬОВА_ВАЛЮТА\n"
            "Наприклад: /convert 980 UAH USD"
        )
        return

    try:
        amount = float(parts[1])
        from_currency = parts[2].upper()
        to_currency = parts[3].upper()
        result = converter.convert(amount, from_currency, to_currency)
        bot.send_message(
            message.chat.id,
            f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )
        save_to_history(message.from_user.id, message.text)

    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, f"Сталася помилка: {str(e)}")

# ----------------- Команда /history -----------------
@bot.message_handler(commands=['history'])
def show_history(message):
    history_text = get_history(message.from_user.id)
    bot.send_message(message.chat.id, history_text)

# ----------------- Запуск бота -----------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.remove_webhook()  # очищає конфлікти
    print("Бот запущено, чекаю повідомлень...")

    # бесконечный цикл с авто-перезапуском при ошибках
    import time
    while True:
        try:
            bot.infinity_polling()
        except Exception as e:
            print("Ошибка polling:", e)
            time.sleep(3)