import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pep440check.main import main


def create_test_pyproject(content: str) -> Path:
    """Create a temporary pyproject.toml file with given content."""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False)
    temp_file.write(content)
    temp_file.close()
    return Path(temp_file.name)


def test_main_ok_case():
    """Test main function with already normalized version."""
    pyproject_content = '''[project]
name = "test"
version = "1.0.0"
'''
    temp_file = create_test_pyproject(pyproject_content)
    
    try:
        with patch('sys.argv', ['pep440check', str(temp_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    finally:
        temp_file.unlink()


def test_main_normalization_needed():
    """Test main function with version that needs normalization."""
    pyproject_content = '''[project]
name = "test"
version = "1.0.0-rc1"
'''
    temp_file = create_test_pyproject(pyproject_content)
    
    try:
        with patch('sys.argv', ['pep440check', str(temp_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        temp_file.unlink()


def test_main_write_option():
    """Test main function with write option."""
    pyproject_content = '''[project]
name = "test"
version = "1.0.0-rc1"
'''
    temp_file = create_test_pyproject(pyproject_content)
    
    try:
        with patch('sys.argv', ['pep440check', str(temp_file), '-w']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            
        # Check that file was modified
        with open(temp_file, 'r') as f:
            content = f.read()
            assert 'version = "1.0.0rc1"' in content
    finally:
        temp_file.unlink()


def test_main_file_not_found():
    """Test main function with non-existent file."""
    with patch('sys.argv', ['pep440check', 'nonexistent.toml']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1


def test_main_invalid_version():
    """Test main function with invalid version."""
    pyproject_content = '''[project]
name = "test"
version = "invalid"
'''
    temp_file = create_test_pyproject(pyproject_content)
    
    try:
        with patch('sys.argv', ['pep440check', str(temp_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        temp_file.unlink()


def test_main_missing_version():
    """Test main function with missing version field."""
    pyproject_content = '''[project]
name = "test"
'''
    temp_file = create_test_pyproject(pyproject_content)
    
    try:
        with patch('sys.argv', ['pep440check', str(temp_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        temp_file.unlink()