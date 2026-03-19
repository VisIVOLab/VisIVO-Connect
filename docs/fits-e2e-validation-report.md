# FITS E2E Validation Report

Date: 2026-03-18

## Scope

Validation and observability for the FITS remote-render pipeline:
- FITS load + HDU selection + sanitize + VTK conversion
- session/render timing and runtime metrics
- interactive soak behavior (latest-frame-wins and interactive->HQ transition)
- bottleneck split across loader, renderer, and encoder/streaming

## Files Changed

Runtime:
- `backend/core/observability.py`
- `backend/data/importers.py`
- `backend/core/session.py`
- `backend/app/main.py`
- `backend/rendering/vtk_datacube_renderer.py`

Tests / tools:
- `backend/tests/test_dataset_importer_fits_robustness.py`
- `backend/tests/test_soak_remote_render.py`
- `tools/soak_remote_render.py`

Docs:
- `docs/fits-e2e-validation-report.md`
- `docs/bottleneck-notes.md`

## Metrics Added

Importer (FITS path):
- `fits_open_ms`
- `hdu_select_ms`
- `sanitize_convert_ms`
- `vtk_build_ms`
- `fits_total_ms`

Session/runtime:
- `first_frame_latency_ms`
- `high_quality_render_time_ms`
- `interactive_fps`
- `memory_rss_mb` (best-effort)

Exposed via `GET /api/metrics/{sessionId}` in additive fields:
- `importMetrics`
- `runtimeMetrics`

## Validation Executed

### Automated tests

Command:
```bash
.venv/bin/python -m pytest backend/tests -q
```

Result:
- `19 passed`

### Importer metric smoke (FITS -> VTK only)

Command:
```bash
.venv/bin/python - <<'PY'
from pathlib import Path
from tools.validate_fits_datacube import create_synthetic_fits_cube
from backend.data import load_image_data
from backend.core.observability import consume_last_fits_import_metrics

p = Path('/tmp/visivo-import-metrics.fits')
create_synthetic_fits_cube(p, size=48)
img = load_image_data(f'{p}#hdu=1')
print('dims', img.GetDimensions())
print('import_metrics', consume_last_fits_import_metrics())
PY
```

Observed sample:
- dims: `(48, 48, 48)`
- fits_open_ms: `0.436`
- hdu_select_ms: `0.470`
- sanitize_convert_ms: `0.276`
- vtk_build_ms: `0.181`
- fits_total_ms: `11.335`

### Interactive soak (deterministic harness)

Command:
```bash
.venv/bin/python tools/soak_remote_render.py --duration-s 0.3 --burst-size 4 --input-hz 40 --target-fps 15 --hq-snapshots 2 --json
```

Observed sample:
- backlogStable: `true`
- latestFrameWins: `true`
- interactiveToHqTransition: `true`
- fpsEstimate: `13.11`
- deliveredFrames: `7`
- droppedFrames: `6`
- renderAvg: `18.01 ms`
- inputToVisibleAvg: `80.29 ms`

## Bottlenecks and Current State

Loader FITS:
- Instrumented and measurable end-to-end.
- Main cost captured in `fits_total_ms`; HDU and sanitize/conversion split is visible.

Renderer:
- Robust initial transfer-function defaults now use percentile-based range (`p1/p99`, sampled).
- This improves first visual quality stability on outlier-heavy volumes.

Encoder/streaming/runtime:
- Real-renderer soak execution currently fails in this environment (`process exited -1`), indicating a native runtime issue in render/codec path.
- This is distinct from importer correctness (import tests pass and importer metrics are produced).

## Prioritized TODO

1. Run `tools/soak_remote_render.py --real-renderer` on target HPC/runtime with crash diagnostics enabled and collect failure signature.
2. Add persistent run artifact export (`.json`) for soak and endpoint metrics snapshots.
3. Add side-by-side baseline scenario (`.npy` vs `.fits`) in the same soak harness.
4. Add optional websocket-level soak mode (current harness is session-level).
