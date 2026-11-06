import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { positionStateAt, validateReplay } from "../src/js/replay-model.mjs";

const data = JSON.parse(await readFile(new URL("../public/data/replay/pyramiding-win-session.json", import.meta.url), "utf8"));
const outcome = JSON.parse(await readFile(new URL("../public/data/replay/pyramiding-win-outcome.json", import.meta.url), "utf8"));
assert.deepEqual(validateReplay(data, outcome), []);

const initial = positionStateAt(data, data.indices.entry1 - 1, null);
assert.equal(initial.quantity, 0);
assert.equal(initial.openGrossBRL, 0);

const first = positionStateAt(data, data.indices.entry1, null);
assert.equal(first.quantity, 1);
assert.equal(first.averageEntryPrice, 100000);
assert.equal(first.openGrossBRL, (data.candles[data.indices.entry1].c - 100000) * 0.2);

const beforeAdd = positionStateAt(data, data.indices.entry2 - 1, null);
assert.equal(beforeAdd.quantity, 1);
const built = positionStateAt(data, data.indices.entry2, null);
assert.equal(built.quantity, 2);
assert.equal(built.averageEntryPrice, 100151.5);
assert.equal(built.openGrossBRL,
  ((data.candles[data.indices.entry2].c - 100000) + (data.candles[data.indices.entry2].c - 100303)) * 0.2);

const closed = positionStateAt(data, data.indices.exit, outcome);
const postExit = positionStateAt(data, data.indices.postExitCheckpoint, outcome);
assert.equal(closed.quantity, 0);
assert.equal(closed.realizedGrossBRL, 750.2);
assert.equal(closed.realizedNetBRL, 738.2);
assert.equal(outcome.tickGridAssessment.exchangeExecutablePricesVerified, false);
assert.equal(outcome.grossBRL * 5 % 1, 0);
assert.notEqual(outcome.grossPoints % data.tickSizePoints, 0,
  "The fractional-real result is retained as exact adjusted-price model arithmetic, not snapped to an exchange tick grid");
assert.deepEqual(postExit, closed);
assert.equal(positionStateAt(data, data.indices.entry2, outcome).quantity, 2,
  "Seeking backward must restore the historical open two-leg position");

console.log("Replay model tests: position sequence, per-leg mark, average entry, close and post-exit lock passed.");
