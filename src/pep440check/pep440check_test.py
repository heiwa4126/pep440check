from pep440check.pep440check import check_version


def test_valid_versions():
    """Test valid version strings"""
    valid_cases = [
        ("1.0.0", "1.0.0"),
        ("1.0.0a1", "1.0.0a1"),
        ("1.0.0b1", "1.0.0b1"),
        ("1.0.0rc1", "1.0.0rc1"),
        ("1.0.0.dev1", "1.0.0.dev1"),
        ("1.0.0+local", "1.0.0+local"),
        ("2.0", "2.0"),  # packaging keeps 2.0 as is
        ("v1.0.0", "1.0.0"),  # v prefix is removed
    ]

    for version_str, expected in valid_cases:
        is_valid, normalized = check_version(version_str)
        assert is_valid, f"Version {version_str} should be valid"
        assert normalized == expected, (
            f"Normalized result differs from expected: {normalized} != {expected}"
        )


def test_invalid_versions():
    """Test invalid version strings"""
    invalid_cases = [
        "invalid",
        "",
        "1.0.0-",
    ]

    for version_str in invalid_cases:
        is_valid, _ = check_version(version_str)
        assert not is_valid, f"Version {version_str} should be invalid"
