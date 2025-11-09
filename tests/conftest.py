from collections.abc import Callable
from pathlib import Path

import pytest


@pytest.fixture
def write(tmp_path: Path) -> Callable[[str, str], Path]:

    def _write(name: str, content: str) -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p

    return _write


@pytest.fixture
def csv_ok(write) -> Path:
    return write("ok.csv", "name,brand,price,rating\n" "A,apple,10,4.5\n" "B,samsung,20,4.8\n")
