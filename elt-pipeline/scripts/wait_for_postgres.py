#!/usr/bin/env python3
"""Wait until PostgreSQL accepts connections."""

import sys
import time

from ingestion.config import DB_CONFIG, DB_CONNECT_DELAY, DB_CONNECT_RETRIES
from ingestion.db import get_connection


def wait_for_postgres() -> None:
    for attempt in range(1, DB_CONNECT_RETRIES + 1):
        try:
            conn = get_connection()
            conn.close()
            print("PostgreSQL is ready.")
            return
        except RuntimeError:
            if attempt == DB_CONNECT_RETRIES:
                raise
            print(f"Waiting for PostgreSQL ({attempt}/{DB_CONNECT_RETRIES})...")
            time.sleep(DB_CONNECT_DELAY)


if __name__ == "__main__":
    try:
        wait_for_postgres()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
