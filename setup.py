"""Packaging glue.

The wheel carries the PostgreSQL binaries under embedded_postgres/pginstall and
no compiled Python extension, so it must be tagged as a *platform* wheel
(``py3-none-<platform>``) rather than a pure-Python one — one wheel per
platform, valid for every CPython version. setuptools only does that for
distributions with extension modules, hence the two overrides below.
"""

from setuptools import Distribution, setup

try:
    from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # setuptools < 70.1
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class BinaryDistribution(Distribution):
    def has_ext_modules(self) -> bool:  # noqa: D401 — setuptools hook
        return True


class bdist_wheel(_bdist_wheel):
    def finalize_options(self) -> None:
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        _python, _abi, plat = super().get_tag()
        return "py3", "none", plat


setup(
    distclass=BinaryDistribution,
    cmdclass={"bdist_wheel": bdist_wheel},
)
