from collections.abc import Iterable, Sequence

from tabulate import tabulate


def format_table(
    headers: list[str],
    rows: Sequence[tuple[str, ...]],
    *,
    style: str = "github",
    floatfmt: str = ".2f",
    show_index: bool | Iterable[int] | str = "always",
) -> str:

    idx = show_index
    if show_index == "always" or show_index is True:
        idx = range(1, len(rows) + 1)

    return tabulate(rows, headers=headers, tablefmt=style, floatfmt=floatfmt, showindex=idx)
