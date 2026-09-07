#! /bin/bash
# Run the package tests against the wheel cibuildwheel just built and installed
# into its test venv. A per-test timeout guards against the hang seen on
# Windows, where a failed child process left the parent waiting forever.
PROJECT=$1

echo "Running on OSTYPE=$OSTYPE with UID=$UID"

pytest -s -v --log-cli-level=INFO --timeout=600 "$PROJECT/tests"
