import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scr import reports
from scr.csv_reader import read_products
from scr.formatting import format_table


def _build_parser() -> argparse.ArgumentParser:
    reports.load_builtin_reports()
    available_reports = sorted(reports.list_reports())

    parser = argparse.ArgumentParser(
        prog="brand-reports",
        description=(
            "Агрегирует CSV-файлы товаров и строит отчёты. "
            f"Поддерживаемые отчёты: {', '.join(available_reports)}."
        ),
    )

    parser.add_argument(
        "--files",
        metavar="PATH",
        nargs="+",
        required=True,
        help="Пути к CSV-файлам (один или несколько)",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Имя отчёта для построения",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="brand-reports 1.0.0",
    )
    return parser


def _validate_input_paths(paths: Sequence[str]) -> list[Path]:
    resolved: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if not p.exists():
            raise FileNotFoundError(f"Файл не найден: {raw}")
        if not p.is_file():
            raise FileNotFoundError(f"Не является файлом: {raw}")
        resolved.append(p)
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        file_paths = _validate_input_paths(args.files)
    except FileNotFoundError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2

    try:
        rows = list(read_products(file_paths))
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2

    if not rows:
        print(
            "[error] Нет валидных данных для отчёта (все строки некорректны или файлы пусты)",
            file=sys.stderr,
        )
        return 2

    try:
        reports.load_builtin_reports()
        report_fn = reports.get_report(args.report)
    except KeyError:
        print(f"[error] Неизвестный отчёт: {args.report}", file=sys.stderr)
        return 2

    try:
        aggregates = list(report_fn(rows))
    except Exception as e:
        print(f"[error] Ошибка при построении отчёта '{args.report}': {e}", file=sys.stderr)
        return 2

    headers = getattr(report_fn, "HEADERS", ["brand", "avg rating", "count"])
    table_rows: list[tuple[str, str, str]] = [
        (str(a["label"]), f"{float(a["metric"]):.2f}", str(a["context"])) for a in aggregates
    ]

    print(format_table(headers, table_rows))
    return 0


def run() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    raise SystemExit(main())
