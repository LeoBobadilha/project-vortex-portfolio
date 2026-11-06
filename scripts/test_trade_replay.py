from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "public/data/replay/pyramiding-win-session.json"
OUTCOME_PATH = ROOT / "public/data/replay/pyramiding-win-outcome.json"
HTML_PATH = ROOT / "src/index.html"
SCRIPT_PATH = ROOT / "src/js/trade-replay.js"
ERRORS: list[str] = []

data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
outcome = json.loads(OUTCOME_PATH.read_text(encoding="utf-8"))
candles = data["candles"]
indices = data["indices"]
events = data["events"]
entries = sorted((event for event in events if event["type"] == "entry"), key=lambda e: e["index"])

if len(candles) != 107 or data["session"]["barCount"] != 107:
    ERRORS.append("Replay must contain the complete 107-bar available session")
if indices != {"entry1": 31, "pullback": 33, "entry2": 34, "exit": 67, "postExitCheckpoint": 72}:
    ERRORS.append("Event positions must match the audited session chronology")
if candles[0]["t"] != 0 or candles[-1]["t"] != 530:
    ERRORS.append("Session-relative timestamps do not span the full source session")
if any(candles[i]["t"] - candles[i - 1]["t"] != 5 for i in range(1, len(candles))):
    ERRORS.append("All M5 candles must remain chronological with five-minute spacing")
if len(candles) - 1 - indices["exit"] < 5:
    ERRORS.append("At least five real candles must follow the recorded exit")
if len(entries) != 2 or [event["quantity"] for event in entries] != [1, 1]:
    ERRORS.append("Two separately recorded one-contract entry events are required")
if entries[0]["index"] >= indices["pullback"] or indices["pullback"] >= entries[1]["index"]:
    ERRORS.append("A genuine intervening pullback must precede the separately recorded add-on")
if outcome["exitQuantity"] != 2 or outcome["exitIndex"] != indices["exit"]:
    ERRORS.append("The exit must close the complete two-contract position at the audited event")
if data.get("tickSizePoints") != 5 or data.get("exchangeExecutablePricesVerified") is not False:
    ERRORS.append("WIN tick size and non-executable adjusted-price classification must be explicit")
if data.get("sourceSessionDate") != "2022-09-30" or data.get("sourceTimezoneAuthenticated") is not False:
    ERRORS.append("Source market-session date and unauthenticated timezone status must be explicit")
if data.get("sourceSessionClockStart") != "09:00" or data.get("sourceSessionClockTimezoneAuthenticated") is not False:
    ERRORS.append("Source-session clock start and unauthenticated timezone status must be explicit")
clock_start_hour, clock_start_minute = (int(part) for part in data.get("sourceSessionClockStart", "00:00").split(":"))
clock_at_start = f"{clock_start_hour:02d}:{clock_start_minute:02d}"
clock_end_total = clock_start_hour * 60 + clock_start_minute + candles[-1]["t"]
clock_at_end = f"{(clock_end_total // 60) % 24:02d}:{clock_end_total % 60:02d}"
if clock_at_start != "09:00" or clock_at_end != "17:50":
    ERRORS.append(f"Source-session clock labels must span 09:00 to 17:50; found {clock_at_start} to {clock_at_end}")
clock_script = SCRIPT_PATH.read_text(encoding="utf-8")
for clock_use in (
    "const sourceClock =",
    "tickMarkFormatter: (time) => sourceClock(Number(time) / 60)",
    "timeFormatter: (time) => sourceClock(Number(time) / 60)",
    "sourceClock(data.candles[ix].t)",
    "Source-session clock ${sourceClock(candle.t)}",
):
    if clock_use not in clock_script:
        ERRORS.append(f"Chart clock label is not wired to the qualified source clock formatter: {clock_use}")
if data.get("privacy", {}).get("sourceSessionDatePublished") is not True:
    ERRORS.append("Public privacy metadata must record the authorized date disclosure")
if outcome.get("resultBasis") != "unrounded arithmetic from adjusted-price research-model fills; not exchange-executable P&L":
    ERRORS.append("BRL result must be identified as adjusted-price model arithmetic, not executable P&L")
if outcome.get("tickGridAssessment", {}).get("exchangeExecutablePricesVerified") is not False:
    ERRORS.append("Replay must not claim the modeled fills are exchange-verified")
if [entry["price"] % data["tickSizePoints"] for entry in entries] != [0, 3]:
    ERRORS.append("Public translated entry prices must preserve the audited grid residuals without snapping")
if outcome["exitPrice"] % data["tickSizePoints"] != 2:
    ERRORS.append("Public translated exit price must preserve its audited off-grid residual")
for i, candle in enumerate(candles):
    if not (candle["l"] <= min(candle["o"], candle["c"]) <= max(candle["o"], candle["c"]) <= candle["h"]):
        ERRORS.append(f"Invalid OHLC geometry at candle {i}")
for entry in entries:
    bar = candles[entry["index"]]
    if not bar["l"] <= entry["price"] <= bar["h"]:
        ERRORS.append(f"{entry['label']} simulated fill is outside its associated M5 envelope")
exit_bar = candles[outcome["exitIndex"]]
if not exit_bar["l"] <= outcome["exitPrice"] <= exit_bar["h"]:
    ERRORS.append("The modeled exit price is outside its associated M5 envelope")
pullback_event = next(event for event in events if event["type"] == "pullback")
if candles[pullback_event["index"]]["l"] != pullback_event["price"]:
    ERRORS.append("The pullback marker does not match its historical low")
if candles[indices["pullback"]]["l"] >= candles[indices["entry1"]]["h"]:
    ERRORS.append("The pullback marker does not coincide with a retracement from the first-entry candle")
if len(outcome["legs"]) != 2:
    ERRORS.append("Per-leg outcome records are required")
else:
    for index, leg in enumerate(outcome["legs"]):
        if leg["quantity"] != 1:
            ERRORS.append(f"Leg {index + 1} quantity must be one contract")
        points = leg["exitPrice"] - leg["entryPrice"]
        if points != leg["grossPoints"]:
            ERRORS.append(f"Leg {index + 1} points do not reconcile")
        if round(points * data["brlPerPointPerContract"], 2) != leg["grossBRL"]:
            ERRORS.append(f"Leg {index + 1} gross BRL does not reconcile")
        if round(leg["grossBRL"] - leg["costBRL"], 2) != leg["netBRL"]:
            ERRORS.append(f"Leg {index + 1} net BRL does not reconcile")
    if outcome["averageEntryPrice"] != sum(leg["entryPrice"] for leg in outcome["legs"]) / 2:
        ERRORS.append("Weighted average entry price is incorrect")
if (outcome["grossPoints"], outcome["grossBRL"], outcome["costBRL"], outcome["netBRL"]) != (3751, 750.2, 12.0, 738.2):
    ERRORS.append("Adjusted-price model arithmetic must reconcile to 3,751 points / R$750.20 gross / R$12 S2 / R$738.20 net")
cost_model = outcome["costModel"]
expected_cost = outcome["exitQuantity"] * (cost_model["roundTripBrokerageBRLPerContract"] + cost_model["adverseRoundTripPointsPerContract"] * cost_model["brlPerPointPerContract"])
if expected_cost != outcome["costBRL"] or outcome["costScenario"] != "S2 research stress scenario":
    ERRORS.append("S2 costs must be applied once per contract and must not be labelled C30")
if "off WIN's 5-point tick grid" not in HTML_PATH.read_text(encoding="utf-8"):
    ERRORS.append("The non-executable tick-grid limitation must be prominent in the replay UI")
html = HTML_PATH.read_text(encoding="utf-8")
if '<time datetime="2022-09-30">30 Sep 2022</time>' not in html or "source clock timezone is unverified" not in html.lower():
    ERRORS.append("The visible source date must be accompanied by its timezone qualification")
if "Source-session clock · timezone unverified" not in html or "displayed source-session clock runs from 09:00 to 17:50" not in html:
    ERRORS.append("The chart must identify its qualified source-session clock convention")
if "Simulated position" not in html or "Live position" in html:
    ERRORS.append("The replay must not describe a historical simulation as a live position")
if any(key in data for key in ("grossBRL", "netBRL", "exitPrice", "sourceDate", "sourceTimestamps")):
    ERRORS.append("Final outcome data must remain separate from the initial candle payload")
combined = json.dumps(data) + json.dumps(outcome)
combined = combined.replace("2022-09-30", "").replace("09:00", "").replace("17:50", "")
if re.search(r"\b(?:202[0-9]-[01][0-9]-[0-3][0-9]|\d{2}:\d{2}|ZZP-FLAG|H36AAA|P1_ENTRY_CUTOFF|PB1)\b", combined):
    ERRORS.append("Public replay contains a source date, clock time, internal ID, variant, or strategy label")
if "pyramiding-win-session.json" not in SCRIPT_PATH.read_text(encoding="utf-8"):
    ERRORS.append("Replay controller does not request the new sanitized session dataset")
script = SCRIPT_PATH.read_text(encoding="utf-8")
html = HTML_PATH.read_text(encoding="utf-8")
for action in ("play", "pause", "restart", "previous", "next", "entry1", "pullback", "entry2", "exit", "postexit", "zoomout", "zoomin", "fit", "fit-session"):
    if f'data-replay-action="{action}"' not in html:
        ERRORS.append(f"Missing functional replay action: {action}")
if "slice(0, current + 1)" not in script:
    ERRORS.append("Chart renderer must withhold candles beyond the current playback index")
if "go(current + 1).then(play)" not in script:
    ERRORS.append("Playback must continue after the exit through post-exit candles")
if 'fetch("data/replay/pyramiding-win-outcome.json"' not in script:
    ERRORS.append("The completed outcome request is missing")
if "TradingView Lightweight Charts" not in html or "vendor/lightweight-charts" not in html:
    ERRORS.append("Chart library attribution or local asset reference is missing")
if "priceRange" not in script or "current + 1" not in script:
    ERRORS.append("Chart viewport must use only the candles already revealed, with a deterministic visible-data range")
if "WATCH THE HISTORICAL" not in html.upper() and "Watch the Historical Trade Replay" not in html:
    ERRORS.append("The replay must be discoverable from the project introduction")

print(f"Pyramiding replay data audit: {len(ERRORS)} error(s)")
for error in ERRORS:
    print(f"- {error}")
if ERRORS:
    raise SystemExit(1)
