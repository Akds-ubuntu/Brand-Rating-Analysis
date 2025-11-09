import importlib
import pkgutil
import sys
from collections.abc import Callable, Iterable, Mapping
from typing import Any

ReportRow = Mapping[str, Any]
ReportFn = Callable[[Iterable[ReportRow]], Iterable[ReportRow]]

_REGISTRY: dict[str, ReportFn] = {}
_DISCOVERED = False


def register_report(name: str, fn: ReportFn) -> None:
    if name in _REGISTRY:
        raise ValueError(f"Отчёт уже зарегистрирован: {name}")
    _REGISTRY[name] = fn


def get_report(name: str) -> ReportFn:
    try:
        return _REGISTRY[name]
    except KeyError as exc:
        raise KeyError(f"Неизвестный отчёт: {name}") from exc


def list_reports() -> list[str]:
    return sorted(_REGISTRY.keys())


def load_builtin_reports() -> None:
    global _DISCOVERED
    if _DISCOVERED:
        return
    pkg_name = __name__
    for m in pkgutil.iter_modules(__path__):
        name = m.name
        if name.startswith("_"):
            continue
        full = f"{pkg_name}.{name}"
        if full in sys.modules:
            continue
        importlib.import_module(full)
    _DISCOVERED = True


from . import average_rating as _average_rating  # noqa: E402, F401
