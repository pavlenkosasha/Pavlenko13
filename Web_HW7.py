import requests
from bs4 import BeautifulSoup
import sqlite3

# URL пошуку iPhone на OLX
URL = "https://www.olx.ua/uk/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/q-iphone/"

# Заголовки браузера
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

# Запит до сайту
response = requests.get(URL, headers=headers)

# Перевірка статусу
if response.status_code != 200:
    print("Помилка при отриманні сторінки")
    exit()

# Парсинг HTML
soup = BeautifulSoup(response.text, "html.parser")

# Підключення до SQLite
conn = sqlite3.connect("olx_phones.db")
cursor = conn.cursor()

# Створення таблиці
cursor.execute("""
CREATE TABLE IF NOT EXISTS phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price TEXT,
    location TEXT,
    link TEXT
)
""")

# Пошук товарів
items = soup.find_all("div", {"data-cy": "l-card"})

print(f"Знайдено товарів: {len(items)}")

# Обробка кожного товару
for item in items:

    # Назва
    title_tag = item.find("h6")
    title = title_tag.text.strip() if title_tag else "Немає назви"

    # Ціна
    price_tag = item.find("p", {"data-testid": "ad-price"})
    price = price_tag.text.strip() if price_tag else "Немає ціни"

    # Посилання
    link_tag = item.find("a")
    link = link_tag["href"] if link_tag else ""

    # Локація
    location_tag = item.find("p", {"data-testid": "location-date"})
    location = location_tag.text.strip() if location_tag else "Немає локації"

    # Вивід у консоль
    print(title)
    print(price)
    print(location)
    print(link)
    print("-" * 50)

    # Запис у базу даних
    cursor.execute("""
    INSERT INTO phones (title, price, location, link)
    VALUES (?, ?, ?, ?)
    """, (title, price, location, link))

# Збереження даних
conn.commit()

print("\nДані успішно збережені в SQLite")

# Читання даних із бази
cursor.execute("SELECT * FROM phones")

rows = cursor.fetchall()

print("\nДані з бази:\n")

# Вивід даних
for row in rows:
    print(row)

# Закриття бази даних
conn.close()