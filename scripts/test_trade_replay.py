from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public/data/replay/two-contract-win.json"
OUTCOME = ROOT / "public/data/replay/two-contract-win-outcome.json"
HTML = ROOT / "src/index.html"
SCRIPT = ROOT / "src/js/trade-replay.js"
errors: list[str] = []

if not PUBLIC.is_file() or not OUTCOME.is_file():
    errors.append("Sanitized replay files are missing")
else:
    data = json.loads(PUBLIC.read_text(encoding="utf-8"))
    outcome = json.loads(OUTCOME.read_text(encoding="utf-8"))
    candles = data["candles"]
    if data.get("contracts") != 2:
        errors.append("Replay must describe exactly two contracts")
    if data.get("direction") not in {"LONG", "SHORT"}:
        errors.append("Replay direction is invalid")
    if len(candles) != 21:
        errors.append("Replay must include the verified 21-bar window")
    if not (0 <= data["entryIndex"] < data["exitIndex"] < len(candles)):
        errors.append("Entry/exit chronology is outside the candle window")
    if candles[data["entryIndex"]]["t"] != 0:
        errors.append("Entry candle must be the zero-minute reference")
    if candles[data["exitIndex"]]["t"] != outcome["durationMinutes"]:
        errors.append("Exit event does not match the recorded elapsed duration")
    for i, candle in enumerate(candles):
        if not (candle["l"] <= min(candle["o"], candle["c"]) <= max(candle["o"], candle["c"]) <= candle["h"]):
            errors.append(f"Candle {i} has invalid OHLC geometry")
        if i and candle["t"] - candles[i - 1]["t"] != 5:
            errors.append(f"Candle {i} is not exactly five minutes after the previous bar")
    entry = data["entryPrice"]
    exit_price = outcome["exitPrice"]
    directional_points = entry - exit_price if data["direction"] == "SHORT" else exit_price - entry
    if directional_points != outcome["grossPoints"] or directional_points <= 0:
        errors.append("Directional points do not match the selected winning trade")
    if outcome["grossBRL"] != outcome["grossPoints"] * data["contracts"] * 0.2:
        errors.append("Gross BRL does not match the WIN point-value calculation")
    if outcome["costBRL"] != 30 * data["contracts"] * 0.2:
        errors.append("C30 costs are not charged once per contract")
    if outcome["netBRL"] != outcome["grossBRL"] - outcome["costBRL"]:
        errors.append("Net C30 does not reconcile to gross less one cost deduction")
    in_trade = candles[data["entryIndex"] : data["exitIndex"] + 1]
    mfe = max(entry - c["l"] for c in in_trade) if data["direction"] == "SHORT" else max(c["h"] - entry for c in in_trade)
    mae = max(c["h"] - entry for c in in_trade) if data["direction"] == "SHORT" else max(entry - c["l"] for c in in_trade)
    if mfe != outcome["mfePoints"] or mae != outcome["maePoints"]:
        errors.append("MFE/MAE do not match the displayed entry-to-exit bar envelope")
    combined = json.dumps(data) + json.dumps(outcome)
    if re.search(r"\b(?:202[0-9]-[01][0-9]-[0-3][0-9]|\d{2}:\d{2}|AAF_DESC|TRIANGLE_V1|WING26)\b", combined):
        errors.append("Public replay contains a source date, clock time, contract expiry or private strategy identifier")
    if any(k in data for k in ("grossPoints", "grossBRL", "netBRL", "mfePoints", "maePoints")):
        errors.append("Completed-trade metrics must be kept out of the initial candle payload")

html = HTML.read_text(encoding="utf-8")
script = SCRIPT.read_text(encoding="utf-8")
if 'src="js/trade-replay.js" defer' not in html or 'id="trade-replay"' not in html:
    errors.append("Replay section or controller is not connected to the page")
if "data/replay/two-contract-win-outcome.json" not in script:
    errors.append("Completion summary endpoint is missing")
elif not re.search(r"if\(current>=data\.exitIndex\)\{stop\(\);loadOutcome\(\)", script):
    errors.append("Completion summary is not gated on reaching the exit candle")
if 'fetch("data/replay/two-contract-win.json")' not in script:
    errors.append("Initial replay candle request is missing")
if "prefers-reduced-motion" not in script or "prefers-reduced-motion" not in (ROOT / "src/css/site.css").read_text(encoding="utf-8"):
    errors.append("Reduced-motion preference is not addressed")
for control in ("play", "pause", "restart", "previous", "next", "entry", "exit"):
    if f'data-replay-action="{control}"' not in html:
        errors.append(f"Missing replay control: {control}")

print(f"Historical replay audit: {len(errors)} error(s)")
for error in errors:
    print(f"- {error}")
if errors:
    raise SystemExit(1)
