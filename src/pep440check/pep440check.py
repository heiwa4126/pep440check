import tomllib
from pathlib import Path
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
