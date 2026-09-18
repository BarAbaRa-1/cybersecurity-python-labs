"Головний модуль запуску Лабораторної роботи №1."

from labs.lab01.task1 import run_task1
from labs.lab01.task2 import run_task2
from labs.lab01.task3 import run_task3


def main() -> None:
    """Послідовний запуск усім завдань."""
    print("=" * 15 + " ЗАВДАННЯ 1 " + "=" * 15)
    run_task1()

    print("\n" + "=" * 15 + " ЗАВДАННЯ 2 " + "=" * 15)
    run_task2()

    print("\n" + "=" * 15 + " ЗАВДАННЯ 3 " + "=" * 15)
    run_task3()


if __name__ == "__main__":
    main()