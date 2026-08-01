import json
import os
from pathlib import Path

from psycopg import connect

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://challenge:challenge@postgres:15432/challenge?sslmode=disable",
)


def load_json(filename: str) -> list[dict]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def main() -> None:
    customers = load_json("customers.json")
    projects = load_json("projects.json")

    print(f"Loaded {len(customers)} customers and {len(projects)} projects")

    with connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            for c in customers:
                cursor.execute(
                    'INSERT INTO customers (id, name, street, postal_code, municipality) VALUES (%s, %s, %s, %s, %s)', (c['id'], c['name'], c['street'], c["postal_code"], c['municipality'])
                )
            for p in projects:
                cursor.execute(
                    'INSERT INTO projects (id, customer_id, date, task, location, description, status) VALUES (%s, %s, %s, %s, %s, %s, %s)', (p['id'], p['customer_id'], p['date'], p['task'], p['location'], p['description'], p['status'])
                )

        connection.commit()

    print("Import script finished")


if __name__ == "__main__":
    main()
