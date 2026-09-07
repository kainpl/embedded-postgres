# Third-party notices

## pgserver

The build system, packaging layout and the Python server-management layer of
this project are derived from **pgserver** by Oscar Moll,
<https://github.com/orm011/pgserver>, licensed under the Apache License,
Version 2.0 (see `LICENSE`). The files inherited from pgserver have been
modified in this project, as required by Section 4(b) of that license.

## PostgreSQL

The wheels produced by this project contain binaries of the PostgreSQL
Database Management System, built from the official source tarballs published
at <https://www.postgresql.org/ftp/source/>.

```
PostgreSQL Database Management System
(formerly known as Postgres, then as Postgres95)

Portions Copyright (c) 1996-2026, PostgreSQL Global Development Group

Portions Copyright (c) 1994, The Regents of the University of California

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose, without fee, and without a written agreement
is hereby granted, provided that the above copyright notice and this
paragraph and the following two paragraphs appear in all copies.

IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR
DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON
AN "AS IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO
PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
```

## pgvector

The wheels contain the **pgvector** extension, <https://github.com/pgvector/pgvector>,
Copyright (c) 2021-2026 Andrew Kane, distributed under the PostgreSQL License
(same terms as above).

## System libraries

Linux wheels may carry copies of shared libraries the PostgreSQL binaries link
against (for example zlib, <https://zlib.net/>, zlib License), placed there by
the manylinux wheel repair step. Each such library keeps its own license.

## MinGW-w64 runtime (Windows wheel)

The Windows wheel carries the runtime libraries of the MinGW-w64 toolchain
that built PostgreSQL, placed next to the executables in `bin/`:
`libwinpthread-1.dll` (MIT / BSD-style licence of the winpthreads project),
and, when the toolchain links them, `libgcc_s_seh-1.dll` and `libstdc++-6.dll`
(GNU GPL v3 with the GCC Runtime Library Exception, which permits this
redistribution) and `zlib1.dll` (zlib License). They are unmodified copies from
<https://www.mingw-w64.org/>.
