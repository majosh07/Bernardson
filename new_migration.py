import re
import sys
from pathlib import Path

MIGRATION_DIR = Path("db/migrations")

def main():
    if len(sys.argv) < 2:
        raise SystemExit('usage: python3 new_migration.py "add media url"')

    name = re.sub(r"[^a-z0-9]+", "_", " ".join(sys.argv[1:]).lower()).strip("_")
    if not name:
        raise SystemExit("Give the migration a name with letters or numbers in it.")
    
    MIGRATION_DIR.mkdir(parents=True, exist_ok=True)

    numbers = [
        int(p.name.split("_", 1)[0])
        for p in MIGRATION_DIR.glob("*.sql")
        if p.name.split("_", 1)[0].isdigit()
    ]
    next_number = max(numbers, default=0) + 1

    path = MIGRATION_DIR / f"{next_number:04d}_{name}.sql"
    path.write_text(f"-- {path.name}\n\n", encoding="utf-8")
    print(f"created {path}")

if __name__ == "__main__":
    main()
