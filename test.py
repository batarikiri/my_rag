print("Скрипт запущен", flush=True)

import sys
print(f"Python version: {sys.version}", flush=True)

try:
    import psycopg2
    print("psycopg2 импортирован", flush=True)
except Exception as e:
    print(f"Ошибка импорта psycopg2: {e}", flush=True)
    sys.exit(1)

print("Введите вопрос: ", end="", flush=True)
question = sys.stdin.readline()
print(f"Вы ввели: {question}", flush=True)