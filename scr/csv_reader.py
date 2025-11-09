import csv
import sys
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path

REQUIRED_FIELDS = {"name", "brand", "price", "rating"}


def _parse_float(value: str) -> float:
    v = value.strip().replace(",", ".")
    return float(v)


def _normalize_header(fieldnames: Iterable[str]) -> list[str]:
    return [f.strip().lower() for f in fieldnames]


def read_products(paths: Iterable[Path]) -> Iterator[Mapping[str, object]]:
    for path in paths:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                msg = f"Пустой CSV или отсутствует строка заголовка: {path}"
                print(f"[warn] {msg}", file=sys.stderr)
                continue

            normalized = _normalize_header(reader.fieldnames)
            header_map: dict[str, str] = dict(zip(normalized, reader.fieldnames, strict=True))

            missing = REQUIRED_FIELDS - set(normalized)
            if missing:
                raise ValueError(
                    f"В файле {path} отсутствуют обязательные колонки: {', '.join(sorted(missing))}"
                )

            for i, row in enumerate(reader, start=2):
                try:
                    name = (row.get(header_map["name"], "") or "").strip()
                    brand = (row.get(header_map["brand"], "") or "").strip()
                    price = _parse_float(row.get(header_map["price"], ""))
                    rating = _parse_float(row.get(header_map["rating"], ""))
                    if not brand:
                        raise ValueError("Пустое поле brand")
                except Exception as exc:
                    msg = f"{path}:{i}: пропуск строки из-за ошибки: {exc}"
                    print(f"[warn] {msg}", file=sys.stderr)
                    continue

                yield {"name": name, "brand": brand, "price": price, "rating": rating}
