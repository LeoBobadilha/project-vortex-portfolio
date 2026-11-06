from __future__ import annotations

import csv
import re
import struct
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
        self.pbi_images: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if values.get("href"):
            self.hrefs.append(values["href"] or "")
        if values.get("src"):
            self.srcs.append(values["src"] or "")
        if values.get("data-pbi-image"):
            self.pbi_images.append(values["data-pbi-image"] or "")


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
    expected_current = {"01-Knowledge.png", "02-Research.png", "03-Executive.png", "12-W06-Win.png", "13-L01-Loss.png", "14-L02-Loss.png"}
    expected_full = expected_current | {"04-Performance.png", "05-Risk.png", "06-Trade-Explorer.png", "07-Validation.png", "08-W02-Win.png", "09-W03-Win.png", "10-W04-Win.png", "11-W05-Win.png"}
    image_dir = DIST / "images" / "powerbi"
    actual_images = {p.name for p in image_dir.glob("[0-9][0-9]-*.png")}
    if actual_images not in (expected_current, expected_full):
        errors.append(f"Power BI gallery assets must be the reviewed six-image set or complete 14-image set; found {sorted(actual_images)}")
    gallery_count = html.count('class="pbi-thumb"')
    linked_images = {Path(name).name for name in parser.pbi_images}
    if gallery_count != len(actual_images) or linked_images != actual_images:
        errors.append(f"Gallery links/count do not match available approved PNGs: {gallery_count} buttons, {len(linked_images)} links, {len(actual_images)} files")
    dimensions = set()
    for name in actual_images:
        path = image_dir / name
        raw = path.read_bytes()
        if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR":
            errors.append(f"Power BI gallery image is not a decodable PNG header: {name}")
        else:
            dimensions.add(struct.unpack(">II", raw[16:24]))
    if len(dimensions) > 1:
        errors.append(f"Power BI screenshot dimensions differ: {sorted(dimensions)}")
    if actual_images == expected_full:
        if "14 Power BI report pages — 14 verified screenshots" not in html:
            errors.append("Full gallery does not state that all 14 report pages have verified screenshots")
    else:
        if "six approved captures available today" not in html or "Pages 04–11 remain part of the PBIP but are not shown here" not in html:
            errors.append("Partial gallery must clearly disclose its six-image coverage and withheld pages")
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

print(f"Static-site smoke test: {len(errors)} error(s)")
for error in errors:
    print(f"- {error}")
if errors:
    raise SystemExit(1)
