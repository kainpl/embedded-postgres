#! /bin/bash
# Run the package tests against the wheel cibuildwheel just built and installed
# into its test venv. A per-test timeout guards against hangs (a failed child
# process once left the parent waiting forever on Windows).
PROJECT=$1

echo "Running on OSTYPE=$OSTYPE with UID=$UID"

case "$OSTYPE" in
    msys* | cygwin*)
        # cibuildwheel creates its run directory with tempfile.mkdtemp(), which
        # on Windows (CPython >= 3.12.4, CVE-2024-4030) gets a protected ACL for
        # SYSTEM, Administrators and the *owner* only. PostgreSQL's tools drop
        # Administrator rights before doing anything (restricted token), and for
        # an administrator the owner IS the Administrators group — so initdb
        # cannot even stat its own binary inside the venv. Grant the user itself.
        # MSYS_NO_PATHCONV: Git Bash would otherwise rewrite "/grant" into
        # "C:/Program Files/Git/grant" before icacls ever sees it.
        venv=$(python -c "import sys; print(sys.prefix)")
        echo "granting $USERNAME explicit access on $venv"
        MSYS_NO_PATHCONV=1 icacls "$venv" /grant "$USERNAME:(OI)(CI)F" /T /Q
        ;;
esac

pytest -s -v --log-cli-level=INFO --timeout=600 "$PROJECT/tests"
