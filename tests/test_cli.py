from pathlib import Path

import pytest

from scr import cli
from scr.cli import _validate_input_paths, main


def test_cli_happy_path(write, capsys):
    csv = write("p.csv", "name,brand,price,rating\nA,apple,10,4.5\nB,apple,12,5.0\n")
    rc = main(["--files", str(csv), "--report", "average-rating"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "apple" in out and "4.75" in out


def test_validate_input_paths_missing_file(tmp_path: Path):
    missing = tmp_path / "nope.csv"
    with pytest.raises(FileNotFoundError) as exc:
        _validate_input_paths([str(missing)])
    assert "Файл не найден" in str(exc.value)


def test_validate_input_paths_not_a_file(tmp_path: Path):
    d = tmp_path / "is_dir"
    d.mkdir()
    with pytest.raises(FileNotFoundError) as exc:
        _validate_input_paths([str(d)])
    assert "Не является файлом" in str(exc.value)


def test_invalid_header(write, capsys):
    csv = write("p.csv", "name,brand,rating\nA,apple,10,4.5\nB,apple,12,5.0\n")
    rc = main(["--files", str(csv), "--report", "average-rating"])
    err = capsys.readouterr().err.lower()
    assert rc == 2
    assert "[error]" in err and "отсутствуют обязательные колонки" in err


def test_invalid_report(write, capsys):
    csv = write("p.csv", "name,brand,price,rating\nA,apple,10,4.5\n")
    rc = main(["--files", str(csv), "--report", "average-sum-rating"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "[error]" in err and "Неизвестный отчёт:" in err


def test_cli_missing_file(capsys, tmp_path: Path):
    rc = main(["--files", str(tmp_path / "no.csv"), "--report", "average-rating"])
    err = capsys.readouterr().err
    assert rc == 2 and "Файл не найден" in err


def test_cli_unknown_report(write, capsys):
    csv = write("p.csv", "name,brand,price,rating\nA,apple,10,4.5\n")
    rc = main(["--files", str(csv), "--report", "nope"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "Неизвестный отчёт" in err


def test_cli_no_valid_rows(write, capsys):
    csv = write("empty.csv", "name,brand,price,rating\nA,,10,4.5\n")
    rc = main(["--files", str(csv), "--report", "average-rating"])
    err = capsys.readouterr().err
    assert rc == 2
    assert "Нет валидных данных" in err


def test_cli_parsing_error_non_numeric(write, capsys):
    csv = write("bad.csv", "name,brand,price,rating\nA,apple,10,not_a_number\n")
    rc = main(["--files", str(csv), "--report", "average-rating"])
    err = capsys.readouterr().err.lower()
    assert rc == 2
    assert "[error]" in err


def test_cli_report_execution_error(write, monkeypatch, capsys):
    csv = write("ok.csv", "name,brand,price,rating\nA,apple,10,4.5\n")

    def boom(_rows):
        raise RuntimeError("crash!")

    monkeypatch.setattr(cli.reports, "get_report", lambda name: boom, raising=True)
    rc = main(["--files", str(csv), "--report", "average-rating"])
    err = capsys.readouterr().err.lower()
    assert rc == 2
    assert "ошибка при построении отчёта" in err
