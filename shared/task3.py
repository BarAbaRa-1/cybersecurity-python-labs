"Завдання 3: Безпечне хешування, CSV-база та JSON-логування (Варіант 13)."

import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from shared.student import VARIANT_NUMBER  # noqa: E402


MIN_PASSWORD_LEN = 14
DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_FILE = DATA_DIR / "users.csv"
LOG_FILE = DATA_DIR / "log.json"


class ValidationError(Exception):
    "Кастомний виняток для помилок валідації пароля."

    pass


def generate_hash(password: str, salt: str = "00000") -> str:
    """Генерує sha3_256 хеш для пароля із сіллю."""
    if not password or not salt:
        raise ValueError("Пароль та сіль не можуть бути порожніми.")

    if len(password) < MIN_PASSWORD_LEN:
        raise ValidationError(
            f"Довжина пароля має бути не менше {MIN_PASSWORD_LEN} символів."
        )

    salted_password = password + salt
    return hashlib.sha3_256(salted_password.encode("utf-8")).hexdigest()


def get_personal_salt() -> str:
    "Формує персональну сіль на основі варіанту."
    return str(VARIANT_NUMBER).zfill(5)


def log_event(func):
    "Декоратор для логування спроб входу у JSON-файл."

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = kwargs.get("username") or (args[0] if args else "unknown")
        try:
            res = func(*args, **kwargs)
            status = "success" if res else "failure"
        except Exception:
            status = "failure"
            raise
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": status,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "args": list(args),
                "kwargs": kwargs,
            }
            try:
                DATA_DIR.mkdir(parents=True, exist_ok=True)
                logs = []
                if LOG_FILE.exists() and os.path.getsize(LOG_FILE) > 0:
                    with open(LOG_FILE, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                logs.append(log_entry)
                with open(LOG_FILE, "w", encoding="utf-8") as f:
                    json.dump(logs, f, indent=4, ensure_ascii=False)
            except (IOError, PermissionError) as e:
                print(f"Помилка запису лог-файлу: {e}")

        return res

    return wrapper


def create_user(username: str, password: str) -> tuple[str, str]:
    "Створює кортеж користувача із хешованим паролем."
    salt = get_personal_salt()
    pwd_hash = generate_hash(password, salt)
    return username, pwd_hash


def create_users(users_list: list[tuple[str, str]]) -> None:
    "Записує базу користувачів у CSV файл."
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "hash_value"])
        for user, pwd in users_list:
            try:
                u, h = create_user(user, pwd)
                writer.writerow([u, h])
            except (ValidationError, ValueError) as e:
                print(f"Не вдалося зареєструвати {user}: {e}")


def read_users_db() -> list[tuple[str, str]]:
    """Зчитує користувачів із CSV-файлу."""
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"Файл {CSV_FILE} не знайдено.")

    users_db = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Пропустити заголовок
        for row in reader:
            if row:
                users_db.append((row[0], row[1]))
    return users_db


@log_event
def login(username: str, password: str) -> bool:
    """Автентифікація користувача."""
    if not username or not password:
        raise ValueError("Логін та пароль є обов'язковими.")

    users_db = read_users_db()
    salt = get_personal_salt()

    try:
        input_hash = generate_hash(password, salt)
    except ValidationError:
        return False

    for db_user, db_hash in users_db:
        if db_user == username and db_hash == input_hash:
            return True

    return False


def run_task3() -> None:
    "Виконання основного сценарію Завдання 3."
    users_to_register = (
        ("ai_admin", "SecurePass12345!"),
        ("ml_dev01", "ComplexPassword99#"),
        ("data_user", "DataEngine2026!#"),
        ("researcher", "ResearchPass#2026"),
        ("bot_service", "BotAuthPass!2026"),
        ("analyst_01", "AnalystPass_999!"),
        ("guest_account", "GuestPassKey_123"),
        ("auditor", "AuditSystem_Pass1"),
        ("engineer", "Engineering_007!"),
        ("short_user", "12345"), 
    )

    try:
        print("1. Реєстрація користувачів та збереження у CSV...")
        create_users(users_to_register)

        print("\n2. Зчитана CSV-база користувачів:")
        db = read_users_db()
        print(f"{'Username':<15} | {'Password SHA3-256 Hash'}")
        print("-" * 60)
        for u, h in db:
            print(f"{u:<15} | {h}")

        print("\n3. Перевірка автентифікації:")
       
        res1 = login("ai_admin", "SecurePass12345!")
        print(f"Вхід ai_admin: {'Успішний' if res1 else 'Невдалий'}")

       
        res2 = login("ai_admin", "WrongPassword123")
        print(f"Вхід ai_admin (невірний пароль): {'Успішний' if res1 and res2 else 'Невдалий'}")

    except (FileNotFoundError, PermissionError, IOError, ValidationError, ValueError) as e:
        print(f"Помилка виконання: {e}")


if __name__ == "__main__":
    run_task3()