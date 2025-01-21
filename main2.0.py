import os
import json
import hashlib
import random  # нужно для выбора случайного текста

USERS_FILE = "users.json"
PASSWORDS_FILE = "passwords.json"
TEXTS_FILE = "texts.txt"  # Файл, содержащий тексты

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

def load_texts_from_txt() -> list:
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

class User:
    """
    Класс, представляющий пользователя.
    Хранит имя пользователя, а методы класса позволяют установить (захешировать) пароль
    и проверить пароль при входе.
    """
    def __init__(self, username: str):
        self.username = username

    def set_password(self, password: str) -> None
