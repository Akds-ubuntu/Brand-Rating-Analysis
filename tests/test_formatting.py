import scr.formatting as fmt


def test_formatting_tabulate_default(monkeypatch):
    called = {}

    def fake_tabulate(rows, headers, tablefmt, floatfmt, showindex):
        called["rows"] = rows
        called["headers"] = headers
        called["tablefmt"] = tablefmt
        called["floatfmt"] = floatfmt
        called["showindex"] = showindex
        return "OK"

    monkeypatch.setattr(fmt, "tabulate", fake_tabulate, raising=True)

    out = fmt.format_table(["Brand", "Avg", "Count"], [("apple", "4.75", "2")])
    assert out == "OK"
    assert called["headers"] == ["Brand", "Avg", "Count"]
    assert called["rows"][0][0] == "apple"
    assert called["tablefmt"] == "github"
    assert called["floatfmt"] == ".2f"


def test_formatting_tabulate_always(monkeypatch):
    got = {}

    def fake_tabulate(rows, headers, tablefmt, floatfmt, showindex):
        got["showindex"] = list(showindex) if not isinstance(showindex, str) else showindex
        return "OK"

    monkeypatch.setattr(fmt, "tabulate", fake_tabulate, raising=True)

    out = fmt.format_table(
        ["Brand", "Avg", "Count"],
        [("apple", "4.75", "2"), ("samsung", "4.50", "1")],
        show_index="always",
    )
    assert out == "OK"
    assert got["showindex"] == [1, 2]
