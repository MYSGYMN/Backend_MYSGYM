Migration notes — MySQL → Postgres
================================

Overview
--------
This repository uses MySQL locally but the production target on Render is
Postgres. To migrate existing data you can:

- Run migrations on the target Postgres to create schema (Alembic / Flask-Migrate).
- Use `scripts/migrate_mysql_to_postgres.py` to copy rows from MySQL to Postgres.

Quick steps
-----------

1. Ensure the target Postgres database exists and is reachable. On Render the
   `DATABASE_URL` environment variable is provided to the service.

2. Run your migrations on the target DB. Example:

```bash
export DATABASE_URL='postgresql+psycopg://user:pass@host:5432/db'
flask db upgrade
```

3. Copy data from local MySQL to target Postgres:

```bash
export SOURCE_DB_URI='mysql+mysqlconnector://localuser:pwd@127.0.0.1:3306/mysgym'
export TARGET_DB_URI="$DATABASE_URL"
python scripts/migrate_mysql_to_postgres.py --batch 500
```

Notes & caveats
---------------
- This script copies raw row data and assumes tables and types are compatible.
- If you used AUTO_INCREMENT/unsigned types in MySQL, verify identity/serial
  columns in Postgres after import.
- For large datasets consider using CSV export/import or a specialized ETL
  tool. Always test on a copy before running in production.
