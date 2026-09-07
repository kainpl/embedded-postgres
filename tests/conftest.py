"""Test-suite plumbing.

Windows: every temporary directory the tests hand to PostgreSQL must stay
readable after PostgreSQL drops Administrator rights. Since CPython 3.12.4
``tempfile.mkdtemp()`` creates directories with a protected ACL for SYSTEM,
Administrators and the owner only (CVE-2024-4030 mitigation); for an
administrator the owner *is* the Administrators group, which PostgreSQL's
restricted token marks deny-only — initdb then fails inside such a directory
with "Permission denied". Granting the current user an explicit ACE keeps the
directory reachable. ``TemporaryDirectory`` goes through ``mkdtemp`` too, so
patching the module attribute covers both.
"""

import os
import platform
import subprocess
import tempfile

if platform.system() == "Windows":
    _original_mkdtemp = tempfile.mkdtemp

    def _mkdtemp_reachable_without_admin(*args, **kwargs):
        path = _original_mkdtemp(*args, **kwargs)
        user = os.environ.get("USERNAME")
        if user:
            subprocess.run(
                ["icacls", path, "/grant", f"{user}:(OI)(CI)F", "/Q"],
                check=False,
                capture_output=True,
            )
        return path

    tempfile.mkdtemp = _mkdtemp_reachable_without_admin
