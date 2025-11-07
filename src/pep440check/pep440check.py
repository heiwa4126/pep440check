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

    parser = argparse.ArgumentParser(description="PEP 440バージョンチェック・正規化")
    parser.add_argument(
        "path", nargs="?", default="pyproject.toml", help="pyproject.tomlのパス"
    )
    parser.add_argument("-w", "--write", action="store_true", help="正規化して書き換え")

    args = parser.parse_args()

    toml_path = Path(args.path).resolve()
    print(f"対象: {toml_path}")

    if not toml_path.exists():
        print(f"エラー: {toml_path} が見つかりません", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_pyproject_toml(toml_path)
        version_str = data["project"]["version"]
    except (KeyError, tomllib.TOMLDecodeError) as e:
        print(f"エラー: pyproject.tomlの読み込みに失敗: {e}", file=sys.stderr)
        sys.exit(1)

    is_valid, normalized = check_version(version_str)

    if not is_valid:
        print(
            f"エラー: バージョン '{version_str}' はPEP 440準拠ではありません",
            file=sys.stderr,
        )
        sys.exit(1)

    if version_str == normalized:
        print("OK")
        sys.exit(0)

    if args.write:
        save_pyproject_toml(toml_path, data, normalized)
        print(f"バージョンを正規化しました: {version_str} -> {normalized}")
    else:
        print(f"元のバージョン: {version_str}")
        print(f"正規化後(提案): {normalized}")

    sys.exit(1)
