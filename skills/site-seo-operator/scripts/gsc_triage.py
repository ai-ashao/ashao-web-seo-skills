#!/usr/bin/env python3
"""Read-only candidate triage for two same-dimension GSC Performance CSV exports.

Does not fetch Search Console, validate date windows, diagnose a cause, or edit code.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path


DIMENSION_HEADERS = {
    "page": ("Top pages", "Pages", "Page", "URL", "Landing page"),
    "query": ("Top queries", "Queries", "Query", "Search query"),
}
METRIC_HEADERS = {
    "clicks": ("Clicks",),
    "impressions": ("Impressions",),
    "position": ("Position", "Average position", "Avg. position"),
}


class ExportError(ValueError):
    """Malformed or incompatible GSC export."""


@dataclass(frozen=True)
class Metric:
    key: str
    clicks: int
    impressions: int
    position: float

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions else 0.0


def _headers(fieldnames: list[str] | None) -> dict[str, str]:
    if not fieldnames:
        raise ExportError("CSV has no header row")
    normalized = {}
    for name in fieldnames:
        key = name.strip().casefold()
        if key in normalized:
            raise ExportError(f"Duplicate CSV column: {name}")
        normalized[key] = name
    return normalized


def _column(headers: dict[str, str], aliases: tuple[str, ...]) -> str:
    for alias in aliases:
        actual = headers.get(alias.casefold())
        if actual is not None:
            return actual
    raise ExportError(f"Missing GSC column (any of {', '.join(aliases)})")


def _integer(raw: str | None, name: str, line: int) -> int:
    value = (raw or "").strip().replace(",", "")
    try:
        n = int(value)
    except ValueError as exc:
        raise ExportError(f"Line {line}: invalid {name}: {raw!r}") from exc
    if n < 0:
        raise ExportError(f"Line {line}: negative {name}")
    return n


def _position(raw: str | None, line: int) -> float:
    try:
        value = float((raw or "").strip())
    except ValueError as exc:
        raise ExportError(f"Line {line}: invalid Position: {raw!r}") from exc
    if not math.isfinite(value) or value < 0:
        raise ExportError(f"Line {line}: invalid Position: {raw!r}")
    return value


def read_export(path: str | Path, dimension: str) -> dict[str, Metric]:
    if dimension not in DIMENSION_HEADERS:
        raise ExportError(f"Unsupported dimension {dimension!r}")
    results: dict[str, Metric] = {}
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        headers = _headers(reader.fieldnames)
        key_col = _column(headers, DIMENSION_HEADERS[dimension])
        click_col = _column(headers, METRIC_HEADERS["clicks"])
        impression_col = _column(headers, METRIC_HEADERS["impressions"])
        position_col = _column(headers, METRIC_HEADERS["position"])
        for line, row in enumerate(reader, start=2):
            key = (row.get(key_col) or "").strip()
            if not key:
                raise ExportError(f"Line {line}: empty {dimension}")
            if key in results:
                raise ExportError(f"Line {line}: duplicate {dimension} {key!r}; do not aggregate")
            results[key] = Metric(
                key=key,
                clicks=_integer(row.get(click_col), "Clicks", line),
                impressions=_integer(row.get(impression_col), "Impressions", line),
                position=_position(row.get(position_col), line),
            )
    if not results:
        raise ExportError(f"Export has no data rows: {path}")
    return results


def review_flags(
    current: Metric,
    previous: Metric | None,
    min_impressions: int = 100,
    min_prior_clicks: int = 10,
) -> list[str]:
    flags = []
    if current.impressions < min_impressions:
        return flags
    if 8 <= current.position <= 20:
        flags.append("PAGE_2_REVIEW")
    if previous is None:
        flags.append("NOT_IN_PREVIOUS_EXPORT")
        return flags
    if previous.impressions >= min_impressions:
        if previous.ctr - current.ctr >= 0.01 and current.position <= previous.position + 0.5:
            flags.append("CTR_DROP_REVIEW")
        if previous.clicks >= min_prior_clicks and current.clicks <= previous.clicks * 0.7:
            flags.append("CLICK_DROP_REVIEW")
    return flags


def render_report(
    current: dict[str, Metric],
    previous: dict[str, Metric],
    dimension: str,
    min_impressions: int = 100,
    include_all: bool = False,
) -> str:
    candidates = []
    for key, now in current.items():
        before = previous.get(key)
        flags = review_flags(now, before, min_impressions=min_impressions)
        if not flags and not include_all:
            continue
        candidates.append((key, now, before, flags))
    candidates.sort(key=lambda r: (-bool(r[3]), -r[1].impressions, r[0]))
    lines = [
        f"# GSC {dimension} review candidates",
        "",
        "> REVIEW FLAGS ONLY — not root-cause diagnoses, indexing evidence, ranking guarantees or observed user sessions.",
        "> Verify both exports use the same property, country, search type, dimension, filters and completed equal-length non-overlapping windows.",
        "> Missing keys may reflect GSC export row limits; not appearing in an export is NOT proof of zero impressions.",
        "",
        f"Current export rows: {len(current)}; prior export rows: {len(previous)}; review rows: {len(candidates)}.",
        "",
        f"| {dimension.title()} | Impr now | Clicks now | CTR now | Pos now | Prev clicks | Flags |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for key, now, before, flags in candidates:
        safe_key = key.replace("|", r"\|").replace("\n", " ").replace("\r", " ")
        old_clicks = str(before.clicks) if before is not None else "UNKNOWN"
        lines.append(
            f"| {safe_key} | {now.impressions} | {now.clicks} | {now.ctr:.2%} | {now.position:.1f} | {old_clicks} | {', '.join(flags) or 'none'} |"
        )
    if not candidates:
        lines.append(f"| No rows met the supplied review threshold ({min_impressions} impressions) | — | — | — | — | — | — |")
    lines.extend([
        "",
        "## Follow-up required",
        "",
        "- Inspect the exact query/URL and market; position and CTR changes are sensitive to query mix and reporting aggregation.",
        "- Check source SERP, existing canonical intent and tool usefulness before drafting a change.",
        "- Route verified technical issues to `$technical-seo-audit` and quality gaps to `$helpful-value-audit`.",
        "- Produce a reviewable PR only after a separate code-change authorization and appropriate tests.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--current", required=True, type=Path, help="Current completed-window GSC CSV")
    parser.add_argument("--previous", required=True, type=Path, help="Prior same-filter/window GSC CSV")
    parser.add_argument("--dimension", choices=("page", "query"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-impressions", type=int, default=100)
    parser.add_argument("--all", action="store_true", help="Also show rows without review flags")
    args = parser.parse_args()
    if args.min_impressions < 1:
        parser.error("--min-impressions must be >= 1")
    try:
        current = read_export(args.current, args.dimension)
        previous = read_export(args.previous, args.dimension)
        result = render_report(current, previous, args.dimension, args.min_impressions, args.all)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    except (OSError, ExportError) as exc:
        parser.error(str(exc))
    print(f"Wrote read-only review report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
