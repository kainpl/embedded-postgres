from setuptools import setup

# Baseline packaging inherited from pgserver: an empty CFFI module is compiled
# only so that setuptools produces a platform-specific (non-pure) wheel that
# carries the PostgreSQL binaries under src/embedded_postgres/pginstall.
# Replacing this with a py3-none-<platform> tag is a planned change.
setup(
    cffi_modules=["src/embedded_postgres/_build.py:ffibuilder"],
)
