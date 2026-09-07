# embedded-postgres

PostgreSQL server binaries as a pip-installable wheel, plus a small Python
layer that runs `initdb`, starts and stops the server, and hands you a
connection URI. No system PostgreSQL, no root, no Docker.

```python
import embedded_postgres

with embedded_postgres.get_server("/path/to/pgdata") as pg:
    uri = pg.get_uri()          # postgresql://postgres:@localhost:PORT/postgres
    pg.psql("create extension vector")
```

## Status

Early. This project started on 2026-09-07 as a fork of
[pgserver](https://github.com/orm011/pgserver), which had stopped at
PostgreSQL 16.2 in mid-2024. The goals that justify a separate project:

- **current PostgreSQL** (18.6 today), with minor releases picked up as they ship;
- **Linux aarch64** (and later armv7l) wheels next to x86_64, macOS and Windows;
- **one wheel per platform** (`py3-none-<platform>`) instead of one per Python version;
- **contrib** modules such as `pg_stat_statements` shipped alongside `pgvector`.

Until the first release is tagged, wheels are only available as workflow
artifacts from the GitHub Actions runs.

## Versioning

The package version mirrors the bundled PostgreSQL release: `MAJOR.MINOR` are
PostgreSQL's, the third number counts this package's own revisions for that
PostgreSQL version. `18.6.0` is the first packaging of PostgreSQL 18.6.

## How it is built

`pgbuild/Makefile` downloads the official PostgreSQL source tarball and
`pgvector`, builds `world-bin` (server, client tools and contrib, no docs)
with `configure && make`, and installs the result into
`src/embedded_postgres/pginstall/`. `cibuildwheel` runs that build once per
platform in CI and packages the tree into a wheel. Nothing is compiled on the
user's machine.

Configure flags: `--without-readline --without-icu`. No OpenSSL — the server
is meant to listen on localhost or a Unix socket.

## License

Apache License 2.0 for this project's own code. The bundled PostgreSQL and
pgvector binaries are distributed under the PostgreSQL License. See `NOTICE`
and `THIRD_PARTY_NOTICES.md`.
