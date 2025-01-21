import os
import json
import hashlib

USERS_FILE = "users.json"
PASSWORDS_FILE = "passwords.json"
TEXTS_FILE = "TEXTS.txt"  # Файл с немецкими текстами

def load_users() -> list:
    """
    Загружает список пользователей из файла USERS_FILE (JSON).
    Возвращает пустой список, если файл отсутствует или некорректен.
    """
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def save_users(users: list) -> None:
    """
    Сохраняет список пользователей в файл USERS_FILE (JSON).
    """
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_passwords() -> dict:
    """
    Загружает словарь {username: password_hash} из файла PASSWORDS_FILE (JSON).
    Возвращает пустой словарь, если файл отсутствует или некорректен.
    """
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    try:
        with open(PASSWORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {}

def save_passwords(passwords: dict) -> None:
    """
    Сохраняет словарь {username: password_hash} в файл PASSWORDS_FILE (JSON).
    """
    with open(PASSWORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(passwords, f, ensure_ascii=False, indent=4)

def load_texts() -> list:
    """
    Загружает список текстов (dict) из файла TEXTS_FILE (JSON).
    Каждый элемент списка должен иметь поля: level, title, content.
    Возвращает пустой список, если файл отсутствует или некорректен.
    """
    if not os.path.exists(TEXTS_FILE):
        return []
    try:
        with open(TEXTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

class User:
    """
    Класс, представляющий пользователя.
    Хранит имя пользователя и методы класса, позволяющие захешировать пароль
    и проверить пароль при входе.
    """
    def __init__(self, username: str):
        self.username = username

    def set_password(self, password: str) -> None:
        """
        Хэширует пароль и сохраняет его в PASSWORDS_FILE (JSON).
        """
        passwords_data = load_passwords()
        hash_pw = hashlib.sha256(password.encode()).hexdigest()
        passwords_data[self.username] = hash_pw
        save_passwords(passwords_data)

    def check_password(self, password: str) -> bool:
        """
        Сравнивает хэш введённого пароля с хэшем, хранящимся в PASSWORDS_FILE.
        Возвращает True, если совпадают, иначе False.
        """
        passwords_data = load_passwords()
        stored_hash = passwords_data.get(self.username)
        if not stored_hash:
            return False
        # Хэшируем пароль, который ввёл пользователь, и сравниваем со значением в файле
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash

def main_menu():
    """
    Отображает главное меню и обрабатывает выбор пользователя.
    """
    print("Добро пожаловать в программу 'Изучай немецкий'!")
    while True:
        print("\nВыберите действие:")
        print("1 - Регистрация нового пользователя")
        print("2 - Вход существующего пользователя")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        else:
            print("Некорректный выбор. Попробуйте снова.")

def register_user():
    """
    Регистрация нового пользователя:
    - Считывает имя пользователя.
    - Проверяет, не существует ли уже пользователь с таким именем.
    - Если не существует, добавляет в список пользователей и запрашивает пароль для этого пользователя.
    """
    print("\n=== Регистрация нового пользователя ===")
    users = load_users()
    username = input("Введите имя пользователя: ").strip()

    if username in users:
        print(f"Пользователь '{username}' уже существует. Попробуйте другое имя.")
        return

    # Добавляет нового пользователя в список
    users.append(username)
    save_users(users)

    # Запрашивает пароль и сохраняем хэш
    password = input("Введите пароль: ").strip()
    user = User(username)
    user.set_password(password)

    print(f"Пользователь '{username}' успешно зарегистрирован!")

def login_user():
    """
    Вход пользователя:
    - Загружаем список пользователей и выводим их нумерованный список.
    - Просим выбрать номер пользователя из списка.
    - Запрашиваем пароль и сверяем с хранимым хэшем.
    """
    print("\n=== Вход существующего пользователя ===")

    users = load_users()
    if not users:
        print("Нет зарегистрированных пользователей. Сначала зарегистрируйтесь.")
        return

    # Выводим нумерованный список пользователей
    print("Список пользователей:")
    for i, u in enumerate(users, start=1):
        print(f"{i}. {u}")

    # Просим выбрать номер
    selected_username = None
    while True:
        choice_str = input("Введите номер пользователя из списка: ").strip()
        if not choice_str.isdigit():
            print("Ошибка: введите корректный номер.")
            continue

        choice_int = int(choice_str)
        if 1 <= choice_int <= len(users):
            selected_username = users[choice_int - 1]
            break
        else:
            print("Ошибка: номер вне диапазона, попробуйте ещё раз.")

    # Просим ввести пароль
    password = input("Введите пароль: ").strip()

    # Создаём объект User и проверяем пароль
    user = User(selected_username)
    if user.check_password(password):
        print(f"Добро пожаловать, {selected_username}!")
        user_dashboard(selected_username)
    else:
        print("Неправильный пароль.")

def user_dashboard(username: str):
    """
    После успешного входа отображает меню действий для пользователя.
    """
    while True:
        print("\nВыберите дальнейшее действие:")
        print("1 - Работа с текстом")
        print("2 - Тесты")
        print("3 - Перевод слов")
        print("4 - 10 слов для повторения")
        print("0 - Выход в главное меню")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            text_work(username)
        elif choice == "2":
            tests(username)
        elif choice == "3":
            translate_words(username)
        elif choice == "4":
            repeat_10_words(username)
        elif choice == "0":
            print("Выход в главное меню.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

# ====== Работа с текстами ======

AVAILABLE_LEVELS = ["A1", "A2", "B1", "B2", "C1"]

def text_work(username: str):
    """
    Предоставляет пользователю выбор уровня текста (A1, A2, B1, B2, C1),
    затем показывает доступные тексты этого уровня.
    После выбора текста по номеру выводит его содержимое.
    """

    def load_texts() -> list:
        """
        Читает файл TEXTS_FILE (texts.txt), парсит строки и формирует список словарей.
        Формат каждой строки в texts.txt:
        Уровень||Заголовок||Содержание
        Пример:
        A1||Titel A1-1||Hallo! Ich heiße ...
        Возвращает список вида:
        [
            {
              "level": "A1",
              "title": "Titel A1-1",
              "content": "Hallo! Ich heiße ..."
            },
            ...
        ]
        """
        if not os.path.exists(TEXTS_FILE):
            return []

        texts = []
        with open(TEXTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # пропускаем пустые строки
                parts = line.split("||")
                if len(parts) == 3:
                    level, title, content = parts
                    texts.append({
                        "level": level.strip(),
                        "title": title.strip(),
                        "content": content.strip()
                    })
                # Если формат строки не соответствует, можно либо пропустить, либо вызвать ошибку
        return texts

    print(f"\n[{username}] Работа с текстом")
    texts = load_texts()
    if not texts:
        print("Файл с текстами пуст или не найден. Обратитесь к администратору.")
        return

    print("\nВыберите уровень текста, который хотите прочитать:")
    for i, lvl in enumerate(AVAILABLE_LEVELS, start=1):
        print(f"{i}. {lvl}")

    chosen_level = None
    while True:
        choice_str = input("Введите номер уровня: ").strip()
        if not choice_str.isdigit():
            print("Ошибка: введите корректный номер.")
            continue

        choice_int = int(choice_str)
        if 1 <= choice_int <= len(AVAILABLE_LEVELS):
            chosen_level = AVAILABLE_LEVELS[choice_int - 1]
            break
        else:
            print("Ошибка: номер вне диапазона, попробуйте снова.")

    # Фильтруем тексты по выбранному уровню
    level_texts = [t for t in texts if t.get("level") == chosen_level]
    if not level_texts:
        print(f"Нет доступных текстов для уровня {chosen_level}.")
        return

    # Выводим список текстов данного уровня
    print(f"\nДоступные тексты уровня {chosen_level}:")
    for i, t in enumerate(level_texts, start=1):
        print(f"{i}. {t.get('title', 'Без названия')}")

    # Выбираем конкретный текст
    selected_text = None
    while True:
        choice_str = input("Введите номер текста: ").strip()
        if not choice_str.isdigit():
            print("Ошибка: введите корректный номер.")
            continue

        choice_int = int(choice_str)
        if 1 <= choice_int <= len(level_texts):
            selected_text = level_texts[choice_int - 1]
            break
        else:
            print("Ошибка: номер вне диапазона, попробуйте снова.")

    # Выводим содержимое выбранного текста
    print("\n=== ВЫБРАННЫЙ ТЕКСТ ===")
    # print(f"Уровень: {selected_text.get("level")}")
    # print(f"Название: {selected_text.title}")
    print(f"{selected_text.get("content")}")


# ====== Заглушки для остальных пунктов меню ======

def tests(username: str):
    """
    Заглушка для тестов.
    """
    print(f"\n[{username}] Тесты — пока не реализовано.")

def translate_words(username: str):
    """
    Заглушка для перевода слов.
    """
    print(f"\n[{username}] Перевод слов — пока не реализовано.")

def repeat_10_words(username: str):
    """
    Заглушка для повторения 10 слов.
    """
    print(f"\n[{username}] 10 слов для повторения — пока не реализовано.")

if __name__ == "__main__":
    main_menu()