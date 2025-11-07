# pep440check Project Rules

## Project Overview

- This is a Python package that checks and normalizes PEP 440 version strings in pyproject.toml files
- Package name: pep440check
- Target Python version: >=3.9
- Build system: uv_build
- License: MIT

## Code Style

- Use dataclasses for structured data
- Keep functions minimal and focused
- Follow Python naming conventions
- Use type hints where appropriate

## Testing

- Test files should be named `*_test.py`
- Use pytest for testing
- Test both functionality and data structure validation

## Dependencies

- Runtime dependencies: packaging (for PEP 440 version handling)
- Minimal dependencies - use standard library when possible
- Development dependencies include: mypy, pytest, ruff, poethepoet, validate-pyproject

## File Structure

- Source code in `src/pep440check/`
- Tests alongside source files with `_test.py` suffix
- Exclude test files from wheel distribution
