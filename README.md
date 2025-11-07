# pep440check

[![PyPI - Version](https://img.shields.io/pypi/v/pep440check.svg)](https://pypi.org/project/pep440check)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pep440check.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/pep440check)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

pyproject.toml の project.version のバージョン文字列が PEP 440 準拠であるか判定し、準拠していなければ正規形を提案するユーティリティ。
またオプションで正規形に書き換えることもできる。

## 使い方

pep440check [<pyproject.toml のパス>] [-w]

パスを省略した場合はcwdのpyproject.tomlが対象
オプション無しの場合は、元のバージョン文字列と正規化後のバージョン文字列をstdout
-wオプションで正規化して元のpyproject.toml を書き換え

## インストールと実行

```sh
uv add pep440check --dev
uv run pep440check [args]
```

または

```sh
uvx pep440check [args]
```

または

```sh
uv tool install pep440check
pep440check [args]
```

など
