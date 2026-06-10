#!/usr/bin/env python3
"""Check pipeline infrastructure and latest ingestion run."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ingestion.config import CITIES
from ingestion.db import get_connection, table_exists


def healthcheck() -> int:
    issues: list[str] = []

    try:
        conn = get_connection()
    except RuntimeError as exc:
        print(f"FAIL: database unreachable - {exc}")
        return 1

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")

        print("OK: database connected")

        if not table_exists(conn, "raw_weather"):
            issues.append("raw_weather table does not exist (run make ingest)")
        else:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM raw_weather")
                total_rows = cur.fetchone()[0]
                print(f"OK: raw_weather has {total_rows} rows")

                cur.execute(
                    """
                    SELECT city, COUNT(*)
                    FROM raw_weather
                    GROUP BY city
                    ORDER BY city
                    """
                )
                city_counts = dict(cur.fetchall())

            for city in CITIES:
                count = city_counts.get(city, 0)
                if count == 0:
                    issues.append(f"no data for {city}")
                else:
                    print(f"OK: {city} has {count} rows")

        if not table_exists(conn, "pipeline_runs"):
            issues.append("pipeline_runs table does not exist (run make ingest)")
        else:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT status, records_loaded, finished_at
                    FROM pipeline_runs
                    ORDER BY started_at DESC
                    LIMIT 1
                    """
                )
                last_run = cur.fetchone()

            if last_run:
                status, loaded, finished_at = last_run
                print(
                    f"OK: last run status={status}, loaded={loaded}, finished={finished_at}"
                )
                if status != "success":
                    issues.append(f"last pipeline run status is {status}")
            else:
                issues.append("no pipeline runs recorded")

    finally:
        conn.close()

    if issues:
        for issue in issues:
            print(f"WARN: {issue}")
        return 1

    print("Health check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(healthcheck())
