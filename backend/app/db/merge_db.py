import sqlite3
from pathlib import Path

# Шляхи до баз даних
USERS_DB = Path("backend/app/db/users.db")
MEAS_DB = Path("backend/app/db/measurement.sqlite")

def main():
    # Перевіряємо, чи існують файли баз даних
    if not USERS_DB.exists():
        print(f"Помилка: Файл {USERS_DB} не знайдено!")
        return
    if not MEAS_DB.exists():
        print(f"Помилка: Файл {MEAS_DB} не знайдено!")
        return

    conn = sqlite3.connect(USERS_DB)
    cur = conn.cursor()

    try:
        # Приєднуємо базу measurement як 'meas'
        cur.execute("ATTACH DATABASE ? AS meas", (str(MEAS_DB),))
        print(f"Успішно приєднано {MEAS_DB} як 'meas'")

        # Отримуємо список всіх таблиць з measurement.sqlite (окрім системних)
        tables = cur.execute("""
            SELECT name, sql 
            FROM meas.sqlite_master 
            WHERE type = 'table' 
              AND name NOT LIKE 'sqlite_%';
        """).fetchall()

        if not tables:
            print("У базі measurement.sqlite не знайдено користувацьких таблиць.")
            return

        for name, create_sql in tables:
            print(f"Обробляю таблицю: {name!r}")

            # Перевіряємо, чи таблиця вже існує в users.db
            exists = cur.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?;",
                (name,)
            ).fetchone()

            if not exists:
                if create_sql:
                    print(f"  Створюю таблицю {name!r} в users.db")
                    cur.execute(create_sql)
                else:
                    print(f"  Увага: Для таблиці {name!r} немає CREATE SQL, пропускаю створення")
                    continue
            else:
                print(f"  Таблиця {name!r} вже існує в users.db — пропускаю створення")

            # Копіюємо дані
            try:
                print(f"  Копіюю дані з meas.{name} → {name}")
                cur.execute(f"INSERT INTO {name} SELECT * FROM meas.{name}")
                row_count = cur.rowcount
                print(f"  Успішно скопійовано {row_count} рядків")
            except sqlite3.Error as e:
                print(f"  ПОМИЛКА при копіюванні даних таблиці {name}: {e}")

        # Зберігаємо зміни
        conn.commit()
        print("Усі зміни успішно збережено в users.db")

    except sqlite3.Error as e:
        print(f"Помилка SQLite: {e}")
        conn.rollback()
    finally:
        # Від'єднуємо базу та закриваємо з'єднання
        try:
            cur.execute("DETACH DATABASE meas")
            print("Базу 'meas' від'єднано")
        except:
            pass
        conn.close()

if __name__ == "__main__":
    main()