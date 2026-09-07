"""Dependency-free smoke test of an installed wheel.

Used where the full pytest suite cannot run because its extras
(psycopg2-binary, SQLAlchemy, greenlet) have no wheels for the platform —
today that is manylinux armv7l inside cibuildwheel. Starts a server through
the package's own API, queries it through the bundled psql, loads pgvector,
and stops it. Exits non-zero on any failure.
"""

import sys
import tempfile

import embedded_postgres


def main() -> int:
    pgdata = tempfile.mkdtemp(prefix="embedded-postgres-smoke-")
    with embedded_postgres.get_server(pgdata) as server:
        version = server.psql("select version();")
        print(version.strip())
        if "PostgreSQL 18." not in version:
            print("unexpected server version", file=sys.stderr)
            return 1
        vector = server.psql(
            "create extension if not exists vector;"
            " select extversion from pg_extension where extname = 'vector';"
        )
        print(vector.strip())
        if "0.8" not in vector:
            print("pgvector did not load", file=sys.stderr)
            return 1
        print(server.psql("create extension if not exists pg_stat_statements;").strip())
    print("smoke OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
