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

Current state (2026-09-07): PostgreSQL 18.6 + pgvector 0.8.6 build green on
all five targets — `manylinux_2_28` x86_64 and aarch64, `macosx_11_0` arm64
and x86_64, `win_amd64` — 12–17 MB per wheel. Until the first release is
tagged, wheels are only available as workflow artifacts from the GitHub
Actions runs.

## Windows and Administrator accounts

PostgreSQL's tools refuse to run with Administrator rights: `initdb`,
`pg_ctl` and `postgres` re-launch themselves with a *restricted token* in which
the Administrators group is deny-only. Any directory that is reachable only
through that group is then invisible to them — including the binaries
themselves. Since CPython 3.12.4, `tempfile.mkdtemp()` on Windows creates
exactly such directories (SYSTEM, Administrators and the owner; for an
administrator the owner *is* Administrators). Symptom:

```
invalid binary "...\embedded_postgres\pginstallin\initdb.exe": Permission denied
initdb: error: program "postgres" is needed by initdb but was not found in the same directory as "initdb"
```

If you run as Administrator, keep the package and the data directory out of
`mkdtemp()`-created trees, or grant your user an explicit ACE
(`icacls <dir> /grant "%USERNAME%:(OI)(CI)F" /T`). Regular user accounts and
directories created with `os.mkdir()` / `python -m venv` are unaffected.

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
