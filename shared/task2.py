"""Завдання 2: Багаторівнева система контролю доступу (Варіант 13)."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER  # noqa: E402


users = {
    "ai_security_expert": {
        "role": "ai_security",
        "clearance": 4,
        "department": "AI Security",
        "active": True,
    },
    "ml_engineer": {
        "role": "ml_engineer",
        "clearance": 3,
        "department": "Machine Learning",
        "active": True,
    },
    "data_engineer": {
        "role": "data_engineer",
        "clearance": 2,
        "department": "Data Engineering",
        "active": True,
    },
    "research_assistant": {
        "role": "researcher",
        "clearance": 2,
        "department": "Research",
        "active": True,
    },
    "training_bot": {
        "role": "bot_account",
        "clearance": 1,
        "department": "Automation",
        "active": False,
    },
}

resources = [
    ("ai_models", 4),
    ("training_datasets", 3),
    ("data_pipelines", 2),
    ("research_notebooks", 2),
    ("model_artifacts", 4),
    ("synthetic_data", 1),
    ("adversarial_tests", 3),
    ("model_registry", 4),
    ("feature_stores", 2),
    ("public_models", 1),
]

security_levels = (
    "Open Source",
    "Internal Research",
    "Proprietary",
    "Trade Secret",
)

blocked_users = {"training_bot", "model_theft", "data_poisoning_acc"}


def check_access(username: str, resource_name: str, resource_level: int) -> tuple[str, str]:
    """Алгоритм перевірки доступу."""
    if username not in users:
        return "DENY", "User not found"

    if username in blocked_users:
        return "DENY", "User is blocked"

    user_info = users[username]

    if not user_info.get("active", False):
        return "DENY", "Account inactive"

    if user_info.get("clearance", 0) >= resource_level:
        return "ALLOW", ""

    return "DENY", "Insufficient clearance"


def run_task2() -> None:
    "Запуск системи контролю доступу."
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}\n")

    print("Список ресурсів системи ")
    for res_name, level_code in resources:
        text_level = security_levels[level_code - 1]
        print(f"Ресурс: {res_name:<20} | Рівень безпеки: {text_level}")
    print("\n Результати перевірки доступу ")

    for username in list(users.keys()) + ["non_existent_user"]:
        for res_name, level_code in resources[:2]: 
            status, reason = check_access(username, res_name, level_code)
            reason_str = f" ({reason})" if reason else ""
            print(f"user=[{username}] resource=[{res_name}] -> {status}{reason_str}")


if __name__ == "__main__":
    run_task2()