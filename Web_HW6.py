import mysql.connector

# 🔌 Підключення до сервера (без бази)
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=""
)

cursor = conn.cursor()

# 🗄 Створення бази
cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
cursor.execute("USE test_db")

# 🧱 Таблиці
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100),
    email VARCHAR(100) UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(100),
    login VARCHAR(100),
    password VARCHAR(100),
    auth_type VARCHAR(50),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()


# 👤 Клас користувача
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def register(self):
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (self.username, self.password, self.email)
            )
            conn.commit()
            print("✅ Реєстрація успішна!")
        except:
            print("❌ Користувач або email вже існує!")

    @staticmethod
    def login(username, password):
        cursor.execute(
            "SELECT id FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        return cursor.fetchone()


# 🌐 Акаунти сайтів
class Account:
    def __init__(self, site_name, login, password, auth_type, user_id):
        self.site_name = site_name
        self.login = login
        self.password = password
        self.auth_type = auth_type
        self.user_id = user_id

    def save(self):
        cursor.execute(
            "INSERT INTO accounts (site_name, login, password, auth_type, user_id) VALUES (%s, %s, %s, %s, %s)",
            (self.site_name, self.login, self.password, self.auth_type, self.user_id)
        )
        conn.commit()
        print("✅ Дані збережені!")

    @staticmethod
    def show(user_id):
        cursor.execute(
            "SELECT site_name, login, auth_type FROM accounts WHERE user_id=%s",
            (user_id,)
        )

        data = cursor.fetchall()

        print("\n📄 Твої сайти:")
        for row in data:
            print(f"Сайт: {row[0]}, Логін: {row[1]}, Тип входу: {row[2]}")


# 🔍 перевірка
def user_exists(username, email):
    cursor.execute(
        "SELECT * FROM users WHERE username=%s OR email=%s",
        (username, email)
    )
    return cursor.fetchone()


# 💻 меню
while True:
    print("\n1 - Реєстрація")
    print("2 - Вхід")
    print("3 - Вийти")

    choice = input("👉 Обери: ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        email = input("Email: ")

        if user_exists(username, email):
            print("❌ Такий користувач вже існує!")
        else:
            User(username, password, email).register()

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")

        user = User.login(username, password)

        if user:
            user_id = user[0]
            print("✅ Успішний вхід!")

            while True:
                print("\n1 - Додати сайт")
                print("2 - Показати сайти")
                print("3 - Назад")

                sub = input("👉 Обери: ")

                if sub == "1":
                    site = input("Сайт: ")
                    auth_type = input("Тип входу: ")

                    if auth_type.lower() == "password":
                        login = input("Логін: ")
                        password = input("Пароль: ")
                    else:
                        login = "-"
                        password = "-"

                    Account(site, login, password, auth_type, user_id).save()

                elif sub == "2":
                    Account.show(user_id)

                elif sub == "3":
                    break
        else:
            print("❌ Невірні дані!")

    elif choice == "3":
        print("👋 Вихід")
        break
#Username: Alex
#Password: 000
#Email: sashap@gmail.com