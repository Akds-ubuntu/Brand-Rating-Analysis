import importlib
import pkgutil
import types

import pytest

import scr.reports as reports
from scr.reports import get_report, list_reports, register_report


def test_registry_has_average_rating():
    assert "average-rating" in list_reports()
    fn = get_report("average-rating")
    assert callable(fn)


def test_registry_unknown_report():
    with pytest.raises(KeyError):
        get_report("nope")


def test_registry_duplicate_register(monkeypatch):
    monkeypatch.setattr(reports, "_REGISTRY", {})

    def dummy(rows):
        return rows

    register_report("dummy", dummy)
    with pytest.raises(ValueError):
        register_report("dummy", dummy)


def test_load_builtin_reports_idempotent(monkeypatch):
    monkeypatch.setattr(reports, "_DISCOVERED", False, raising=True)
    reports.load_builtin_reports()
    reports.load_builtin_reports()
    assert reports._DISCOVERED is True


def test_discovery_skips_modules_with_leading_underscore(monkeypatch):
    monkeypatch.setattr(reports, "_DISCOVERED", False, raising=True)

    class FakeMod:
        def __init__(self, name):
            self.name = name

    fake_found = [FakeMod("_hidden"), FakeMod("visible")]

    def fake_iter_modules(_path):
        return iter(fake_found)

    monkeypatch.setattr(pkgutil, "iter_modules", fake_iter_modules, raising=True)

    seen: list[str] = []

    def fake_import(fullname: str):
        seen.append(fullname)
        return types.SimpleNamespace(__name__=fullname)

    monkeypatch.setattr(importlib, "import_module", fake_import, raising=True)

    reports.load_builtin_reports()

    assert not any(name.endswith("._hidden") for name in seen)
    assert any(name.endswith(".visible") for name in seen)
