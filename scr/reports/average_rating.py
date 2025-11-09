from collections import defaultdict
from collections.abc import Iterable
from typing import Any

from . import ReportRow, register_report


def _average_rating(rows: Iterable[ReportRow]) -> list[ReportRow]:
    acc_sum: dict[str, float] = defaultdict(float)
    acc_cnt: dict[str, int] = defaultdict(int)

    for r in rows:
        b = str(r["brand"])
        rating = float(r["rating"])
        acc_sum[b] += rating
        acc_cnt[b] += 1

    result: list[dict[str, Any]] = [
        {"label": b, "metric": acc_sum[b] / acc_cnt[b], "context": acc_cnt[b]} for b in acc_sum
    ]

    result.sort(key=lambda x: (-x["metric"], x["label"]))
    return result


register_report("average-rating", _average_rating)
_average_rating.HEADERS = ["brand", "avg rating", "count"]
