#!/usr/bin/env python3
"""migrate_mysql_to_postgres.py

Simple data copy utility that transfers rows from a MySQL source to a
Postgres target. This script assumes the destination schema/tables
already exist (run your migrations or `flask db upgrade` / `db.create_all()`
before importing data).

Usage examples:
  export SOURCE_DB_URI='mysql+mysqlconnector://user:pass@localhost:3306/mysgym'
  export TARGET_DB_URI='postgresql+psycopg://user:pass@host:5432/dbname'
  python scripts/migrate_mysql_to_postgres.py --batch 500

The script copies rows table-by-table using SQLAlchemy Core. It will skip
tables that are present in the source but missing on the destination.
"""
from __future__ import annotations

import os
import argparse
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.engine import Engine
from sqlalchemy import inspect
from typing import Iterable


def get_engine(uri: str) -> Engine:
    return create_engine(uri, future=True)


def chunked(iterable: Iterable, size: int):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def copy_table_data(src_engine: Engine, dst_engine: Engine, table_name: str, batch_size: int = 500):
    src_meta = MetaData()
    dst_meta = MetaData()
    src_table = Table(table_name, src_meta, autoload_with=src_engine)

    try:
        dst_table = Table(table_name, dst_meta, autoload_with=dst_engine)
    except Exception:
        print(f"Destination table '{table_name}' not found — skipping")
        return

    with src_engine.connect() as src_conn, dst_engine.begin() as dst_conn:
        sel = select(src_table)
        result = src_conn.execute(sel)

        rows_iter = (dict(row) for row in result)
        total = 0
        for batch in chunked(rows_iter, batch_size):
            dst_conn.execute(dst_table.insert(), batch)
            total += len(batch)
        print(f"Copied {total} rows into '{table_name}'")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", help="Source MySQL URI", default=os.getenv("SOURCE_DB_URI"))
    p.add_argument("--target", help="Target Postgres URI", default=os.getenv("TARGET_DB_URI") or os.getenv("DATABASE_URL"))
    p.add_argument("--batch", type=int, default=500, help="Insert batch size")
    args = p.parse_args()

    if not args.source:
        raise SystemExit("Provide source DB URI via --source or SOURCE_DB_URI envvar")
    if not args.target:
        raise SystemExit("Provide target DB URI via --target or TARGET_DB_URI/DATABASE_URL envvar")

    src_engine = get_engine(args.source)
    dst_engine = get_engine(args.target)

    inspector = inspect(src_engine)
    tables = inspector.get_table_names()
    if not tables:
        print("No tables found in source database. Exiting.")
        return

    print(f"Found {len(tables)} tables in source. Starting copy...")
    for t in tables:
        print(f"Processing table: {t}")
        try:
            copy_table_data(src_engine, dst_engine, t, batch_size=args.batch)
        except Exception as e:
            print(f"Error copying table {t}: {e}")


if __name__ == "__main__":
    main()
