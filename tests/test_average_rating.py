from pytest import approx

from scr.reports.average_rating import _average_rating


def test_average_and_sorting():
    rows = [
        {"name": "A", "brand": "apple", "price": 10.0, "rating": 4.5},
        {"name": "B", "brand": "apple", "price": 12.0, "rating": 5.0},
        {"name": "C", "brand": "samsung", "price": 8.0, "rating": 4.5},
    ]
    out = _average_rating(rows)
    assert [r["label"] for r in out] == ["apple", "samsung"]
    assert out[0]["context"] == 2
    assert out[0]["metric"] == approx((4.5 + 5.0) / 2, rel=1e-12)


def test_same_average_sorted_by_brand():
    rows = [
        {"name": "A", "brand": "banana", "price": 10.0, "rating": 4.0},
        {"name": "B", "brand": "apple", "price": 9.0, "rating": 4.0},
    ]
    out = _average_rating(rows)
    assert [r["label"] for r in out] == ["apple", "banana"]
