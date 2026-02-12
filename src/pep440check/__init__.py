from importlib.metadata import version

from pep440check.pep440check import (
    check_version,
    load_pyproject_toml,
    save_pyproject_toml,
)

__version__ = version(__package__ or __name__)  # Python 3.9+ only
__all__ = [
    "check_version",
    "load_pyproject_toml",
    "save_pyproject_toml",
    "__version__",
]
