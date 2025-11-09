from pathlib import Path

import pytest

from scr.csv_reader import read_products


def test_read_products_ok(csv_ok: Path):
    rows = list(read_products([csv_ok]))
    assert len(rows) == 2
    assert rows[0]["brand"] == "apple"


def test_missing_columns_raises(write):
    bad = write("bad.csv", "name,brand,price\nA,apple,10\n")  # нет rating
    with pytest.raises(ValueError):
        list(read_products([bad]))


def test_skips_invalid_and_warns(write, capsys):
    mix = write(
        "mix.csv",
        "name,brand,price,rating\nA,apple,10,4.5\nB,,20,4.9\n",
    )
    rows = list(read_products([mix]))
    assert len(rows) == 1
    err = capsys.readouterr().err.lower()
    assert "пропуск строки" in err and "пустое поле brand" in err


def test_header_spaces_and_case(write):
    f = write("hdr.csv", " Name , BRAND , Price , Rating \nA,apple,10,4.5\n")
    rows = list(read_products([f]))
    assert rows[0]["brand"] == "apple"


def test_headerless_file_warns(tmp_path: Path, capsys):
    f = tmp_path / "no_header.csv"
    f.write_text("", encoding="utf-8")
    rows = list(read_products([f]))
    assert rows == []
    err = capsys.readouterr().err.lower()
    assert "отсутствует строка заголовка" in err
