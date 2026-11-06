export function positionStateAt(data, index, outcome = null) {
  const current = Math.max(0, Math.min(data.candles.length - 1, index));
  const exitIndex = outcome?.exitIndex ?? null;
  if (outcome && current >= exitIndex) {
    const legs = data.events.filter((event) => event.type === "entry" && event.index <= current)
      .map((event) => ({ quantity: event.quantity, entryPrice: event.price, label: event.label }));
    const total = legs.reduce((sum, leg) => sum + leg.quantity, 0);
    const averageEntryPrice = total ? legs.reduce((sum, leg) => sum + leg.entryPrice * leg.quantity, 0) / total : null;
    return { quantity: 0, legs, averageEntryPrice, openGrossBRL: null,
      realizedGrossBRL: outcome.grossBRL, realizedNetBRL: outcome.netBRL, closed: true };
  }
  const legs = data.events
    .filter((event) => event.type === "entry" && event.index <= current)
    .map((event) => ({ quantity: event.quantity, entryPrice: event.price, label: event.label }));
  const quantity = legs.reduce((sum, leg) => sum + leg.quantity, 0);
  const averageEntryPrice = quantity
    ? legs.reduce((sum, leg) => sum + leg.entryPrice * leg.quantity, 0) / quantity
    : null;
  const close = data.candles[current].c;
  const openGrossBRL = legs.reduce(
    (sum, leg) => sum + (close - leg.entryPrice) * leg.quantity * data.brlPerPointPerContract,
    0,
  );
  return { quantity, legs, averageEntryPrice, openGrossBRL, realizedGrossBRL: null,
    realizedNetBRL: null, closed: false };
}

export function validateReplay(data, outcome) {
  const errors = [];
  const { candles, events, indices } = data;
  if (data.sourceSessionDate !== "2022-09-30" || data.sourceTimezoneAuthenticated !== false) errors.push("Source session date and timezone qualification must be explicit");
  if (!Array.isArray(candles) || candles.length !== 107) errors.push("Expected all 107 session candles");
  if (data.tickSizePoints !== 5 || data.exchangeExecutablePricesVerified !== false) errors.push("WIN tick size and adjusted-price non-executable status must be explicit");
  if (indices.entry1 !== 31 || indices.pullback !== 33 || indices.entry2 !== 34 || indices.exit !== 67) errors.push("Event indexes do not match the verified session sequence");
  if (candles?.length - 1 - indices.exit < 5) errors.push("Fewer than five real post-exit bars are available");
  if (!events.some((event) => event.type === "entry" && event.index === indices.entry1 && event.quantity === 1)) errors.push("First one-contract entry is missing");
  if (!events.some((event) => event.type === "entry" && event.index === indices.entry2 && event.quantity === 1)) errors.push("Distinct second one-contract entry is missing");
  if (!events.some((event) => event.type === "pullback" && event.index === indices.pullback)) errors.push("Intervening pullback event is missing");
  for (let i = 0; i < candles.length; i += 1) {
    const c = candles[i];
    if (!(c.l <= Math.min(c.o, c.c) && Math.max(c.o, c.c) <= c.h)) errors.push(`Invalid OHLC geometry at candle ${i}`);
    if (i && c.t - candles[i - 1].t !== 5) errors.push(`Non-chronological M5 interval at candle ${i}`);
  }
  const entryEvents = events.filter((event) => event.type === "entry").sort((a, b) => a.index - b.index);
  if (!outcome) {
    if (entryEvents.length !== 2 || entryEvents[0].quantity !== 1 || entryEvents[1].quantity !== 1) errors.push("Position must be built by two independent one-contract entries");
    if (entryEvents[0].index >= indices.pullback || indices.pullback >= entryEvents[1].index) errors.push("Pullback must occur between the two fills");
    return errors;
  }
  const exitPrice = outcome.exitPrice;
  if (outcome.resultBasis !== "unrounded arithmetic from adjusted-price research-model fills; not exchange-executable P&L") errors.push("BRL outcomes must be classified as non-executable adjusted-price model outputs");
  if (outcome.tickGridAssessment?.exchangeExecutablePricesVerified !== false) errors.push("Tick-grid assessment must not claim exchange-verified prices");
  if (entryEvents[0].price % data.tickSizePoints !== 0 || entryEvents[1].price % data.tickSizePoints !== 3 || exitPrice % data.tickSizePoints !== 2) errors.push("Off-grid fill residuals must be retained without snapping");
  const legPoints = outcome.legs.map((leg) => exitPrice - leg.entryPrice);
  if (entryEvents.length !== 2 || entryEvents[0].quantity !== 1 || entryEvents[1].quantity !== 1) errors.push("Position must be built by two independent one-contract entries");
  if (entryEvents[0].index >= indices.pullback || indices.pullback >= entryEvents[1].index) errors.push("Pullback must occur between the two fills");
  if (outcome.exitQuantity !== 2 || outcome.legs.length !== 2) errors.push("Exit must close exactly two legs");
  if (legPoints[0] !== outcome.legs[0].grossPoints || legPoints[1] !== outcome.legs[1].grossPoints) errors.push("Per-leg points do not reconcile");
  if (outcome.grossPoints !== outcome.legs.reduce((sum, leg) => sum + leg.grossPoints, 0)) errors.push("Combined point result does not reconcile");
  if (Math.abs(outcome.grossBRL - outcome.legs.reduce((sum, leg) => sum + leg.grossBRL, 0)) > 0.001) errors.push("Combined gross BRL does not reconcile");
  const expectedCosts = outcome.exitQuantity * (outcome.costModel.roundTripBrokerageBRLPerContract + outcome.costModel.adverseRoundTripPointsPerContract * outcome.costModel.brlPerPointPerContract);
  if (Math.abs(outcome.costBRL - expectedCosts) > 0.001) errors.push("S2 costs must be applied once per recorded contract");
  if (Math.abs(outcome.netBRL - (outcome.grossBRL - outcome.costBRL)) > 0.001) errors.push("Net result does not equal gross less S2 costs");
  const average = (entryEvents[0].price + entryEvents[1].price) / 2;
  if (Math.abs(outcome.averageEntryPrice - average) > 0.001) errors.push("Weighted average entry does not reconcile");
  const beforeExit = positionStateAt(data, indices.exit - 1, outcome);
  const afterExit = positionStateAt(data, indices.exit, outcome);
  if (beforeExit.quantity !== 2 || afterExit.quantity !== 0 || !afterExit.closed) errors.push("Position quantity must progress 0 → 1 → 2 → 0");
  if (afterExit.realizedNetBRL !== outcome.netBRL) errors.push("Realized net result is not locked after exit");
  return errors;
}
