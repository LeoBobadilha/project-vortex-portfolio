from __future__ import annotations

import csv
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
errors: list[str] = []


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if values.get("href"):
            self.hrefs.append(values["href"] or "")
        if values.get("src"):
            self.srcs.append(values["src"] or "")


html_path = DIST / "index.html"
if not html_path.is_file():
    errors.append("dist/index.html is missing; run npm run build first")
else:
    html = html_path.read_text(encoding="utf-8")
    parser = Links()
    parser.feed(html)
    for href in parser.hrefs:
        parts = urlsplit(href)
        if parts.scheme or href.startswith("#") or not parts.path:
            if href.startswith("#") and href[1:] not in parser.ids:
                errors.append(f"Broken in-page link: {href}")
            continue
        target = (DIST / parts.path).resolve()
        if not target.is_relative_to(DIST.resolve()) or not target.exists():
            errors.append(f"Broken local link: {href}")
    for src in parser.srcs:
        parts = urlsplit(src)
        if parts.scheme or not parts.path:
            continue
        target = (DIST / parts.path).resolve()
        if not target.is_relative_to(DIST.resolve()) or not target.is_file():
            errors.append(f"Broken local asset: {src}")
    for css in (DIST / "css").glob("*.css"):
        body = css.read_text(encoding="utf-8")
        for raw in re.findall(r"url\(['\"]?([^)'\"]+)", body):
            parts = urlsplit(raw)
            if parts.scheme or raw.startswith("data:") or not parts.path:
                continue
            target = (css.parent / parts.path).resolve()
            if not target.is_relative_to(DIST.resolve()) or not target.exists():
                errors.append(f"Broken CSS asset in {css.name}: {raw}")
    if "report-gallery.png" in html:
        errors.append("Withheld Power BI contact sheet is still referenced by the page")
    if "Past performance, including historical backtests and simulated trading results" not in html:
        errors.append("Historical-performance disclosure is missing")

for name in ("benchmark_summary.csv", "annual_portfolio_results.csv", "monthly_portfolio_results.csv"):
    file = DIST / "data" / name
    if not file.is_file():
        errors.append(f"Missing public aggregate CSV: {name}")
        continue
    with file.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.reader(stream)
        headers = next(rows, [])
        if not headers or next(rows, None) is None:
            errors.append(f"CSV has no data rows: {name}")
        if {"TradeID", "OpportunityID", "EntryPrice", "ExitPrice", "SignalTimeUTC"} & set(headers):
            errors.append(f"Trade-level fields found in public CSV: {name}")

if (DIST / "images/powerbi/report-gallery.png").exists():
    errors.append("Zoom-contaminated Power BI gallery was copied to dist")

print(f"Static-site smoke test: {len(errors)} error(s)")
for error in errors:
    print(f"- {error}")
if errors:
    raise SystemExit(1)
