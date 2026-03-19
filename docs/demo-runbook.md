# Demo Runbook

## Purpose

This runbook is for a live or recorded demo of this repository. It focuses on making latency, rendering, and input responsiveness observable enough to trust.

## Start Sequence

1. Start the backend (`uvicorn backend.main:app --host 0.0.0.0 --port 8080`).
2. Open the web client from browser (`http://<host>:8080/`).
3. Press `Connect`.
4. Confirm the control websocket endpoint (`ws://<host>:8080/ws`) is reachable.
5. Run the metrics summary against the latest report.
6. Run a burst-input test at low volume first.
7. Increase burst size only if the control channel stays stable.
8. Watch for render stalls, encode spikes, or missing frame deliveries.

## Recommended Command Flow

```bash
node tools/metrics/summarize-metrics.mjs --input tools/metrics/sample-report.json
node tools/control-burst-input.mjs --url ws://localhost:8080/ws --count 20 --burst-size 5 --interval-ms 250
python tools/validate_fits_datacube.py --output /tmp/visivo-sample.fits --size 32
python tools/validate_fits_datacube.py --input /tmp/visivo-sample.fits --hdu 1
.venv/bin/python -m pytest backend/tests/test_render_protocol_validation.py -q
```

## WebSocket Smoke

The backend test slice exercises the following control-plane messages:

```json
{"type":"hello","sessionId":"demo-1","viewport":{"width":1280,"height":720,"dpr":1}}
{"type":"render.mode","mode":"interactive"}
{"type":"render.params","params":{"mode":"high-quality","scale":1,"targetFps":30,"bitrateMbps":10}}
{"type":"render.params","params":{"visualizationMode":"isosurface","isoValue":0.42,"volume":{"sampleDistanceScale":2.0}}}
{"type":"interaction.start"}
{"type":"interaction.end"}
```

Validation-only coverage also checks visualization pass-through for `volume`
and `isosurface` together with `isoValue` updates in the session layer.

## FITS Validation

- `astropy` is required for the FITS validation path and the associated tests.
- The FITS helper script creates a synthetic cube in a secondary HDU, then reloads it to verify HDU selection.
- NaN/Inf values are sanitized to `0.0` before the cube is handed off to downstream code.

## If Something Fails

- If the websocket disconnects, reduce burst size and retry once.
- If render time spikes, capture the sample report and note the load conditions.
- If input-to-visible latency becomes inconsistent, stop the demo and switch to a fallback artifact.
- If the app does not recover quickly, do not keep sending bursts into it.

## After The Demo

- Save the final metrics report.
- Archive the burst test output.
- Note any user-visible latency or frame-delivery issues.
- Record the exact environment used for the demo.
