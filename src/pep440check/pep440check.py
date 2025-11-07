import sys
from pathlib import Path

import tomllib
from packaging.version import InvalidVersion, Version


def check_version(version_str: str) -> tuple[bool, str]:
    """PEP 440準拠チェックと正規化"""
    try:
        version = Version(version_str)
        return True, str(version)
    except InvalidVersion:
        return False, version_str


def load_pyproject_toml(path: Path) -> dict:
    """pyproject.tomlを読み込み"""
    with open(path, "rb") as f:
        return tomllib.load(f)


def save_pyproject_toml(path: Path, data: dict, normalized_version: str) -> None:
    """pyproject.tomlにバージョンを書き戻し"""
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("version = "):
                lines.append(f'version = "{normalized_version}"\n')
            else:
                lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main() -> None:
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(description="Check and normalize PEP 440 version strings")
    parser.add_argument(
        "path", nargs="?", default="pyproject.toml", help="Path to pyproject.toml"
    )
    parser.add_argument("-w", "--write", action="store_true", help="Write normalized version back to file")

    args = parser.parse_args()

    toml_path = Path(args.path).resolve()
    print(f"Target: {toml_path}")

    if not toml_path.exists():
        print(f"Error: {toml_path} not found", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_pyproject_toml(toml_path)
        version_str = data["project"]["version"]
    except (KeyError, tomllib.TOMLDecodeError) as e:
        print(f"Error: Failed to read pyproject.toml: {e}", file=sys.stderr)
        sys.exit(1)

    is_valid, normalized = check_version(version_str)

    if not is_valid:
        print(
            f"Error: Version '{version_str}' is not PEP 440 compliant",
            file=sys.stderr,
        )
        sys.exit(1)

    if version_str == normalized:
        print("OK")
        sys.exit(0)

    if args.write:
        save_pyproject_toml(toml_path, data, normalized)
        print(f"Normalized version: {version_str} -> {normalized}")
    else:
        print(f"Original version: {version_str}")
        print(f"Suggested normalized version: {normalized}")

    sys.exit(1)
