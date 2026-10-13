# Errors and What They Mean

Find the error message you are seeing, then follow the fix.

### `'PricingFuture' object has no attribute …` / `Cannot evaluate results under the same pricing context being used to produce them`
Inside a `PricingContext`, calculations return futures that are filled in when the context exits.
Call `.result()` after the `with` block, not inside it. Outside any context, calculations return
the value directly.

### `received 1000 (OK); then sent 1000 (OK)` / `Fatal error with websocket`
The websocket used by `is_batch=True` dropped. Rerun with `is_batch=False` (`run_backtest` accepts
it too). These errors never give wrong numbers, only missing ones.

### `504` / `Okay... There's a problem, but we're on it.` (an HTML error page)
A service behind gs_quant timed out or is having trouble. If the code sends many small requests
(e.g. a loop of one instrument and one measure), group them first; see "Choosing contexts" in
`pricing.md`. Otherwise the cause is on the server side (e.g. a service restart, queued jobs or
a wider Marquee issue), so retry later; if it persists, see "If nothing here fixes it".

### `ReadTimeout: … Read timed out. (read timeout=65)`
gs_quant's generic request timeout: the service it called (a dataset query, for example) didn't
answer within 65 seconds. Retry; if it keeps happening, ask for less per call (for datasets, see
"Iterating Over Large Queries" in `datasets.md`).

## If nothing here fixes it

**Isolate the problem with the user before they contact support.** Cut their code down to the
shortest snippet that still shows the error or the wrong number: as few lines, instruments and
measures as possible, no helper functions, classes or notebooks, every value written inline, and
an explicit pricing date and `market_data_location`. Confirm the snippet still reproduces it.

**Then tell the user to email `gs-quant-support@ny.email.gs.com`** with that snippet, its full
output (the error, or the number they got and the one they expected, plus any tracing link it
shows) and the gs_quant version (`gs_quant.__version__`).
