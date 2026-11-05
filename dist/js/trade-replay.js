import { positionStateAt, validateReplay } from "./replay-model.mjs";

const root = document.getElementById("trade-replay");
if (root) {
  const host = document.getElementById("trade-replay-chart");
  const slider = document.getElementById("replay-timeline");
  const speed = document.getElementById("replay-speed");
  const status = document.getElementById("replay-live-status");
  const hover = document.getElementById("replay-hover");
  const number = new Intl.NumberFormat("en-GB", { maximumFractionDigits: 1 });
  const currency = new Intl.NumberFormat("en-GB", { style: "currency", currency: "BRL", minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let data, outcome, outcomePromise, chart, series, markerApi, resizeObserver, timer;
  let priceLines = [], current = -1, follow = true, programmaticRange = false;
  const byId = (id) => document.getElementById(id);
  const text = (id, value) => { byId(id).textContent = value; };
  const elapsed = (minute) => `+${String(Math.floor(minute / 60)).padStart(2, "0")}h ${String(minute % 60).padStart(2, "0")}m`;
  const fmtMoney = (value) => currency.format(value).replace(/\u00a0/g, " ");
  const setEnabled = (enabled) => root.querySelectorAll("button,input,select").forEach((node) => { node.disabled = !enabled; });
  const stop = () => { if (timer) { clearTimeout(timer); timer = null; } };

  function fail(error) {
    stop(); setEnabled(false); host.hidden = true; byId("replay-error").hidden = false;
    byId("replay-chart-state").textContent = "Replay unavailable";
    status.textContent = "The sanitized historical replay could not be loaded. Please reload the page.";
    console.error("Historical replay failed:", error);
  }

  function createChart() {
    const lib = window.LightweightCharts;
    if (!lib) throw new Error("The locally bundled chart engine is unavailable.");
    chart = lib.createChart(host, {
      width: Math.max(320, host.clientWidth), height: host.clientHeight || 430,
      layout: { background: { color: "#0b1420" }, textColor: "#dce6f0", fontFamily: "Inter,system-ui,sans-serif", fontSize: 12, attributionLogo: true },
      grid: { vertLines: { color: "#1c2b3a" }, horzLines: { color: "#1c2b3a" } },
      crosshair: { mode: lib.CrosshairMode.Normal, vertLine: { color: "#71879a", style: lib.LineStyle.Dashed, labelBackgroundColor: "#24394d" }, horzLine: { color: "#71879a", style: lib.LineStyle.Dashed, labelBackgroundColor: "#24394d" } },
      rightPriceScale: { borderColor: "#33485b", autoScale: true, scaleMargins: { top: 0.14, bottom: 0.16 }, minimumWidth: 72 },
      timeScale: { borderColor: "#33485b", timeVisible: true, secondsVisible: false, rightOffset: 4, barSpacing: 9, minBarSpacing: 3, lockVisibleTimeRangeOnResize: true, tickMarkFormatter: (time) => elapsed(Number(time) / 60) },
      handleScroll: { mouseWheel: true, pressedMouseMove: true, horzTouchDrag: true, vertTouchDrag: false },
      handleScale: { mouseWheel: true, pinch: true, axisPressedMouseMove: true, axisDoubleClickReset: true },
      localization: { locale: "en-GB", timeFormatter: (time) => elapsed(Number(time) / 60) },
    });
    series = chart.addSeries(lib.CandlestickSeries, {
      upColor: "#38c9a0", downColor: "#ff7585", borderUpColor: "#38c9a0", borderDownColor: "#ff7585", wickUpColor: "#38c9a0", wickDownColor: "#ff7585", priceLineVisible: false, lastValueVisible: true,
      priceFormat: { type: "price", precision: 1, minMove: 0.5 },
      autoscaleInfoProvider: () => {
        if (!data || current < 0) return null;
        const shown = data.candles.slice(0, current + 1);
        const low = Math.min(...shown.map((c) => c.l)), high = Math.max(...shown.map((c) => c.h));
        const padding = Math.max(20, (high - low) * 0.035);
        return { priceRange: { minValue: low - padding, maxValue: high + padding } };
      },
    });
    markerApi = lib.createSeriesMarkers(series, []);
    chart.subscribeCrosshairMove((event) => {
      const candle = event?.seriesData?.get(series);
      const ix = event?.time === undefined ? -1 : Math.round(Number(event.time) / 300);
      if (!candle || ix < 0 || ix > current) { hover.hidden = true; return; }
      hover.textContent = `${elapsed(data.candles[ix].t)} · O ${number.format(candle.open)} · H ${number.format(candle.high)} · L ${number.format(candle.low)} · C ${number.format(candle.close)}`;
      hover.hidden = false;
    });
    chart.timeScale().subscribeVisibleLogicalRangeChange((range) => {
      if (!programmaticRange && range && current >= 0 && range.to < current - 1) follow = false;
    });
    resizeObserver = new ResizeObserver(([entry]) => { if (entry?.contentRect.width) chart.applyOptions({ width: Math.max(320, Math.floor(entry.contentRect.width)) }); });
    resizeObserver.observe(host);
  }

  function markers() {
    const result = [];
    const add = (ix, position, shape, color) => { if (ix <= current) result.push({ time: data.candles[ix].t * 60, position, shape, color, size: 1.5 }); };
    add(data.indices.entry1, "belowBar", "arrowUp", "#59d7f1");
    add(data.indices.pullback, "aboveBar", "circle", "#f1c66b");
    add(data.indices.entry2, "aboveBar", "arrowUp", "#a992ff");
    if (outcome && current >= outcome.exitIndex) add(outcome.exitIndex, "aboveBar", "arrowDown", "#ff8d98");
    return result;
  }

  function setLines(state) {
    priceLines.forEach((line) => series.removePriceLine(line)); priceLines = [];
    state.legs.forEach((leg, i) => priceLines.push(series.createPriceLine({ price: leg.entryPrice, color: i ? "#a992ff" : "#59d7f1", lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: i ? "Entry 2" : "Entry 1" })));
    if (state.quantity === 2) priceLines.push(series.createPriceLine({ price: state.averageEntryPrice, color: "#e7edf3", lineWidth: 1, lineStyle: 1, axisLabelVisible: true, title: "Weighted average" }));
  }

  function stage() {
    const i = data.indices;
    if (current < i.entry1) return ["STAGE 01 · MARKET CONTEXT", "The session opens with no position", "The complete pre-entry session is visible. The position remains flat while the price structure develops."];
    if (current < i.pullback) return ["STAGE 02 · INITIAL ENTRY", "Entry 1 opens one WIN contract", "The separate research ledger records one simulated long contract. The open mark uses this completed M5 candle and the visible position leg."];
    if (current < i.entry2) return ["STAGE 03 · PULLBACK", "Price retraces before the add-on", "The highlighted retracement appears in the historical M5 bars. The replay describes observable price movement without inferring proprietary trigger rules."];
    if (current < i.exit) return ["STAGE 04 · POSITION BUILT", "Entry 2 adds one more contract", "A distinct one-contract event increases exposure from one to two. The weighted average uses both fills, and open gross P&L is marked separately for each leg."];
    if (current < i.postExitCheckpoint) return ["STAGE 05 · EXIT RECORDED", "The model exit closes both legs", "The recorded research exit returns the position to flat. Realized results are locked while playback continues; no open P&L is calculated after exit."];
    return ["STAGE 06 · POST-EXIT CONTEXT", "The market continues after the exit", "Five or more later candles remain visible. The position stays flat and realized P&L does not change with later prices."];
  }

  function readout() {
    const s = positionStateAt(data, current, outcome), closed = s.closed;
    const pill = byId("replay-position-state"); pill.textContent = closed ? "CLOSED" : s.quantity ? "OPEN" : "FLAT"; pill.classList.toggle("is-open", !closed && s.quantity > 0);
    text("replay-position", `${s.quantity} contract${s.quantity === 1 ? "" : "s"}`);
    const mark = byId("replay-mark"); mark.classList.toggle("is-positive", s.openGrossBRL > 0 || (closed && s.realizedNetBRL > 0));
    text("replay-mark-title", closed ? "Realized gross P&L" : "Open gross P&L");
    mark.textContent = closed ? `${fmtMoney(s.realizedGrossBRL)} realized` : s.quantity ? fmtMoney(s.openGrossBRL) : "—";
    text("replay-mark-label", closed ? "Final realized gross is held constant after the modeled exit." : s.quantity ? "Open gross mark at the latest visible completed M5 close; before costs." : "No position is open. Replay begins with the full pre-entry session context.");
    text("replay-average", s.averageEntryPrice === null ? "—" : number.format(s.averageEntryPrice));
    const e1 = data.events.find((e) => e.type === "entry" && e.index === data.indices.entry1), e2 = data.events.find((e) => e.type === "entry" && e.index === data.indices.entry2);
    text("replay-entry1-price", current >= data.indices.entry1 ? number.format(e1.price) : "—");
    text("replay-entry2-price", current >= data.indices.entry2 ? number.format(e2.price) : "—");
    const [label, title, copy] = stage(); text("replay-stage-label", label); text("replay-stage-title", title); text("replay-stage-copy", copy);
    byId("replay-outcome").hidden = !closed;
    if (closed) {
      text("replay-leg1-gross", `${fmtMoney(outcome.legs[0].grossBRL)} · ${number.format(outcome.legs[0].grossPoints)} points`);
      text("replay-leg2-gross", `${fmtMoney(outcome.legs[1].grossBRL)} · ${number.format(outcome.legs[1].grossPoints)} points`);
      text("replay-final-gross", fmtMoney(outcome.grossBRL)); text("replay-final-cost", `−${fmtMoney(outcome.costBRL)}`); text("replay-final-net", fmtMoney(outcome.netBRL));
      text("replay-postexit-note", current >= data.indices.postExitCheckpoint ? `${current - outcome.exitIndex} post-exit candles are visible. Position remains flat; realized P&L is unchanged.` : "The position is closed. Continue playback to review later bars; realized P&L remains fixed.");
    }
    const candle = data.candles[current]; text("replay-progress-text", `Candle ${current + 1} of ${data.candles.length} · Session ${elapsed(candle.t)}`);
    text("replay-chart-state", `Showing ${current + 1} of ${data.candles.length} verified M5 candles`); slider.value = String(current);
    host.setAttribute("aria-label", `Interactive WIN M5 historical chart through session ${elapsed(candle.t)}. ${current + 1} of ${data.candles.length} candles are visible; later candles are withheld. Current candle OHLC: open ${number.format(candle.o)}, high ${number.format(candle.h)}, low ${number.format(candle.l)}, close ${number.format(candle.c)}.`);
    byId("trade-replay").querySelector('[data-replay-action="fit-session"]').disabled = current !== data.candles.length - 1;
    status.textContent = closed ? `${current >= data.indices.postExitCheckpoint ? "Post-exit context" : "Position closed"}. Flat. Realized net ${fmtMoney(outcome.netBRL)} under the S2 research cost scenario. Candle ${current + 1} of ${data.candles.length}.` : s.quantity ? `Position open: ${s.quantity} WIN contract${s.quantity === 1 ? "" : "s"}. Current gross mark ${fmtMoney(s.openGrossBRL)}. Candle ${current + 1} of ${data.candles.length}.` : `Flat. No position is open. Candle ${current + 1} of ${data.candles.length}.`;
  }

  function render() {
    if (!chart || current < 0) return;
    series.setData(data.candles.slice(0, current + 1).map((c) => ({ time: c.t * 60, open: c.o, high: c.h, low: c.l, close: c.c })));
    markerApi.setMarkers(markers()); setLines(positionStateAt(data, current, outcome));
    if (current === data.indices.entry1 - 1 && chart.timeScale().getVisibleLogicalRange() === null) {
      programmaticRange = true; chart.timeScale().setVisibleLogicalRange({ from: 0, to: current }); programmaticRange = false;
    } else if (follow) { programmaticRange = true; chart.timeScale().scrollToRealTime(); programmaticRange = false; }
    readout();
  }

  async function loadOutcome() {
    if (outcome) return outcome;
    if (!outcomePromise) outcomePromise = fetch("data/replay/pyramiding-win-outcome.json", { cache: "no-cache" }).then((r) => { if (!r.ok) throw new Error("Completed position results are unavailable."); return r.json(); }).then((value) => { outcome = value; return value; });
    return outcomePromise;
  }
  async function go(index) { current = Math.max(0, Math.min(data.candles.length - 1, index)); if (current >= data.indices.exit) await loadOutcome(); render(); }
  function jump(index) { stop(); void go(index).catch(fail); }
  function zoom(factor) {
    const range = chart.timeScale().getVisibleLogicalRange(); if (!range) return;
    const center = (range.from + range.to) / 2, half = Math.max(5, (range.to - range.from) * factor / 2);
    chart.timeScale().setVisibleLogicalRange({ from: Math.max(0, center - half), to: Math.min(current + 0.75, center + half) }); follow = false;
  }
  function play() {
    if (timer || current >= data.candles.length - 1) return;
    timer = setTimeout(() => { timer = null; go(current + 1).then(play).catch(fail); }, reduced.matches ? 1200 : 650 / Number(speed.value));
  }

  root.querySelectorAll("[data-replay-action]").forEach((button) => button.addEventListener("click", () => {
    const action = button.dataset.replayAction, i = data.indices;
    if (action === "play") play(); else if (action === "pause") stop();
    else if (action === "restart") { follow = true; jump(i.entry1 - 1); }
    else if (action === "previous") jump(current - 1); else if (action === "next") jump(current + 1);
    else if (action === "entry1") jump(i.entry1); else if (action === "pullback") jump(i.pullback);
    else if (action === "entry2") jump(i.entry2); else if (action === "exit") jump(i.exit);
    else if (action === "postexit") jump(i.postExitCheckpoint);
    else if (action === "zoomout") zoom(1.4); else if (action === "zoomin") zoom(0.72);
    else if (action === "fit") { chart.timeScale().fitContent(); follow = current === data.candles.length - 1; }
    else if (action === "fit-session" && current === data.candles.length - 1) { chart.timeScale().fitContent(); follow = true; }
  }));
  slider.addEventListener("input", () => { stop(); void go(Number(slider.value)).catch(fail); });
  speed.addEventListener("change", () => { if (timer) { stop(); play(); } });
  reduced.addEventListener?.("change", () => { if (timer) { stop(); play(); } });

  (async () => {
    setEnabled(false);
    try {
      const response = await fetch("data/replay/pyramiding-win-session.json", { cache: "no-cache" });
      if (!response.ok) throw new Error("Full-session sanitized candles could not be loaded.");
      data = await response.json();
      const errors = validateReplay(data, null); if (errors.length) throw new Error(errors.join("; "));
      slider.max = String(data.candles.length - 1); createChart(); current = data.indices.entry1 - 1; render(); setEnabled(true);
    } catch (error) { fail(error); }
  })();
  window.addEventListener("pagehide", () => { stop(); resizeObserver?.disconnect(); chart?.remove(); });
}
