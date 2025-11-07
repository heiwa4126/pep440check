import pytest
from pep440check.pep440check import check_version


def test_valid_versions():
    """有効なバージョンのテスト"""
    valid_cases = [
        ("1.0.0", "1.0.0"),
        ("1.0.0a1", "1.0.0a1"),
        ("1.0.0b1", "1.0.0b1"),
        ("1.0.0rc1", "1.0.0rc1"),
        ("1.0.0.dev1", "1.0.0.dev1"),
        ("1.0.0+local", "1.0.0+local"),
        ("2.0", "2.0"),  # packagingは2.0のまま
        ("v1.0.0", "1.0.0"),  # vプレフィックスは除去される
    ]
    
    for version_str, expected in valid_cases:
        is_valid, normalized = check_version(version_str)
        assert is_valid, f"バージョン {version_str} は有効であるべき"
        assert normalized == expected, f"正規化結果が期待値と異なる: {normalized} != {expected}"


def test_invalid_versions():
    """無効なバージョンのテスト"""
    invalid_cases = [
        "invalid",
        "",
        "1.0.0-",
    ]
    
    for version_str in invalid_cases:
        is_valid, _ = check_version(version_str)
        assert not is_valid, f"バージョン {version_str} は無効であるべき"