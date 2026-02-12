import argparse

from . import __version__


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check and normalize PEP 440 version strings"
    )
    parser.add_argument(
        "path", nargs="?", default="pyproject.toml", help="path to pyproject.toml"
    )
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        help="write normalized version back to file",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s v{__version__}"
    )

    return parser.parse_args()
