import sqlite3

#==============Підключення до БД і створення таблиці====================================================================
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


#===============Клас користувача========================================================================================
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def register(self):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (self.username, self.password, self.email)
            )

            conn.commit()
            conn.close()

            print("Реєстрація успішна!")

        except sqlite3.IntegrityError:
            print("Користувач з таким username або email вже існує!")

    @staticmethod
    def login(username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        return user is not None


#===============Основна програма============================================================================================
def main():
    init_db()

    while True:
        print("\n1 - Зареєструватися")
        print("2 - Увійти")
        print("3 - Вийти")

        choice = input("Виберіть опцію: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            email = input("Email: ")

            user = User(username, password, email)
            user.register()

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")

            if User.login(username, password):
                print("Успішний вхід!")
            else:
                print("Неправильні дані!")

        elif choice == "3":
            print("Вихід з програми...")
            break

        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    main()