# VisIVO Connect

Prototype of **remote scientific visualization** with:

- datacube hosted on server/HPC
- server-side offscreen 3D VTK rendering
- browser-based web client (desktop + Android + large touch displays)
- real-time interaction via a dedicated control plane
- remote stream via a dedicated render plane

## Status

Working in this version:

- remote user session
- server-side datacube rendering in VTK
- browser video streaming via WebRTC
- camera control via WebSocket (rotate/pan/zoom, touch + mouse)
- automatic switch between `interactive` and `high-quality`
- basic metrics and burst-test tooling

## Architecture

- **VTK backend**: [backend/rendering/vtk_datacube_renderer.py](backend/rendering/vtk_datacube_renderer.py)
- **Session manager**: [backend/core/session.py](backend/core/session.py)
- **Transport/stream**: [backend/transport/video_track.py](backend/transport/video_track.py)
- **API + signaling + control**: [backend/app/main.py](backend/app/main.py)
- **Web client**: [web/index.html](web/index.html), [web/styles.css](web/styles.css), [web/app.js](web/app.js)

Details: [docs/architecture.md](docs/architecture.md), [docs/protocol.md](docs/protocol.md)

## Technical Decisions

1. **VTK datacube representation**
   - Volume rendering on `vtkImageData`.
   - Supported inputs: `.vti`, `.mhd/.mha`, `.npy`, `.fits/.fit/.fts` (including `.fits.gz`), synthetic fallback (`vtkRTAnalyticSource`).
   - FITS HDU selection through path fragment: `.../cube.fits#hdu=1` or `.../cube.fits#hdu=SCI`.

2. **Interaction mode strategy**
   - Low-res profile while moving: higher sample distance, lighter shading, outline on.
   - Rationale: preserve volumetric context while reducing GPU/CPU cost.

3. **Automatic interaction -> quality transition**
   - `interaction.start` forces `interactive`.
   - `interaction.end` forces `high-quality`.

4. **Efficient server-side frame capture**
   - Offscreen `vtkRenderWindow` + `vtkWindowToImageFilter`.
   - Frame converted to NumPy BGR for WebRTC encoding.

5. **Browser streaming**
   - RTP video over WebRTC (`aiortc`, `VideoStreamTrack`).
   - Native browser decode.

6. **Input path**
   - WebSocket JSON on `/ws` (control plane), separated from WebRTC media plane.

7. **No frame backlog**
   - Latest-frame-wins in session buffer.
   - Render thread overwrites older frames; track sends only the latest serial.

8. **Android / 65" whiteboard UX**
   - Pointer events, pinch/wheel, fullscreen, responsive viewport, normalized coordinates.

## Setup

Prerequisites:

- Python 3.10+ (3.11/3.12 recommended for `aiortc/av` stability on macOS)
- system packages compatible with VTK offscreen rendering
- modern browser with WebRTC (Chrome/Edge/Firefox, Android included)

Installation:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

For tests:

```bash
pip install -r backend/requirements-dev.txt
```

Generate a demo datacube (optional):

```bash
python tools/generate_sample_datacube.py --size 192 --output web/data/sample_datacube.npy
```

Validate synthetic FITS loading path:

```bash
python tools/validate_fits_datacube.py --output /tmp/visivo-sample.fits --size 32
python tools/validate_fits_datacube.py --input /tmp/visivo-sample.fits --hdu 1
```

## Run

Start server:

```bash
source .venv/bin/activate
export VISIVO_DATACUBE_PATH="$(pwd)/web/data/sample_datacube.npy"  # optional
# FITS example with explicit HDU:
# export VISIVO_DATACUBE_PATH="/hpc/data/my_cube.fits#hdu=SCI"
# optional:
# export VISIVO_AUTH_TOKEN="demo-secret"
# export VISIVO_METRICS_TOKEN="metrics-secret"
# export VISIVO_MAX_SESSIONS="24"
# export VISIVO_IDLE_TIMEOUT_S="1200"
# export VISIVO_STABILITY_MODE="1"  # recommended on macOS
# export VISIVO_ICE_SERVERS='[{"urls":["stun:stun.l.google.com:19302"]},{"urls":["turn:turn.example.org:3478"],"username":"user","credential":"pass"}]'
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --loop asyncio
```

Open client:

- `http://localhost:8080/`
- or `http://<server-hpc>:8080/` from tablet/whiteboard on the same network

Client usage:

- `Connect`
- drag = rotate/pan
- pinch/wheel = zoom
- during input: interactive mode
- on release: high-quality mode

WS control examples:

```json
{"type":"hello","sessionId":"demo-1","viewport":{"width":1280,"height":720,"dpr":1}}
{"type":"interaction.start"}
{"type":"render.mode","mode":"interactive"}
{"type":"render.params","params":{"mode":"high-quality","scale":1,"targetFps":30,"bitrateMbps":10}}
{"type":"render.params","params":{"visualizationMode":"isosurface","isoValue":0.42,"volume":{"sampleDistanceScale":2.0}}}
{"type":"interaction.end"}
```

Validation-oriented examples:

```json
{"type":"render.params","params":{"visualizationMode":"volume"}}
{"type":"render.params","params":{"visualizationMode":"isosurface"}}
{"type":"render.params","params":{"visualizationMode":"isosurface","isoValue":0.42,"volume":{"sampleDistanceScale":2.0},"scale":0.85,"targetFps":18}}
```

Volume modes (`vtkGPUVolumeRayCastMapper`, no fake separate “raytracing” mode):

```json
{"type":"render.params","params":{"visualizationMode":"volume","volume":{"renderMode":"composite"}}}
{"type":"render.params","params":{"visualizationMode":"volume","volume":{"renderMode":"mip"}}}
{"type":"render.params","params":{"visualizationMode":"volume","volume":{"renderMode":"slice","sliceAxis":"z","slicePosition":0.5}}}
{"type":"render.params","params":{"visualizationMode":"volume","volume":{"sampleDistanceScale":1.6,"imageSampleDistance":2.4}}}
{"type":"render.params","params":{"visualizationMode":"volume","volume":{"cropping":{"enabled":true,"bounds":[0.2,0.9,0.1,0.85,0.15,0.8]}}}}
```

## Metrics and Demo Tests

Session metrics:

- `GET /api/metrics/<sessionId>`
- if `VISIVO_METRICS_TOKEN` is set: `GET /api/metrics/<sessionId>?token=<token>`

Burst input test:

```bash
npm init -y
npm install ws
node tools/control-burst-input.mjs --url ws://localhost:8080/ws --count 50 --burst-size 10 --interval-ms 120
```

Summary tool:

```bash
node tools/metrics/summarize-metrics.mjs --input tools/metrics/sample-report.json
```

## FITS E2E Validation

Deterministic soak test (session-level, without browser WebSocket):

```bash
.venv/bin/python tools/soak_remote_render.py --duration-s 3 --burst-size 6 --input-hz 90 --target-fps 30 --hq-snapshots 4 --json
```

Soak attempt with real VTK renderer:

```bash
.venv/bin/python tools/soak_remote_render.py --dataset-path /path/to/cube.fits --real-renderer --duration-s 2 --json
```

Full backend test suite:

```bash
.venv/bin/python -m pytest backend/tests -q
```

Protocol validation slice:

```bash
.venv/bin/python -m pytest backend/tests/test_render_protocol_validation.py -q
```

Compact technical report:

- [docs/fits-e2e-validation-report.md](docs/fits-e2e-validation-report.md)

## Added Dependencies

Python:

- `fastapi`
- `uvicorn[standard]`
- `aiortc`
- `av`
- `numpy`
- `vtk`
- `pydantic`
- `astropy`

## FITS -> VTK Flow (Backend)

1. `datasetPath` comes from websocket `hello` (or `VISIVO_DATACUBE_PATH`).
2. `backend/data/importers.py` detects input type and opens FITS with `astropy.io.fits`.
3. HDU is selected by index/name, or the first available 3D+ HDU.
4. Datacube is validated, converted to `float32`, sanitized (`NaN/Inf/BLANK -> 0.0`).
5. NumPy array (shape `z,y,x`) is converted to `vtkImageData` (`x,y,z`).
6. VTK renderer uses the same volume for interactive/high-quality by changing sampling/shading profile.

Node tooling:

- `ws`

## End-to-End Pipeline

1. Browser opens websocket `/ws` and sends `hello`.
2. Server creates/resumes an offscreen VTK session.
3. Server creates WebRTC peer and sends `offer` over websocket.
4. Browser sends `answer`; ICE exchange follows.
5. Server streams remote-rendered video.
6. Browser sends camera/resize events over websocket.
7. Session updates camera and requests render.
8. Render thread produces frames and keeps only the latest.
9. VideoTrack delivers the latest available frame to the browser.
10. Metrics are collected and exposed by API.

## Current Limits

- no production-grade session authentication/authorization
- no TURN/STUN configured by default (simple LAN focus)
- sender-side bitrate adaptation is basic
- single Python process (no horizontal scaling yet)
- automated tests are focused on demo-critical paths

## Future Improvements

- production-grade TURN + ICE for WAN/NAT
- hardware encoding + dynamic bitrate/fps policy
- multi-session scheduler with GPU resource isolation
- multi-pass progressive refinement (advanced preview/slice proxies)
- distributed tracing from input -> render -> display

## Clear Distinction

Already working:

- server-side remote VTK rendering
- WebRTC browser visualization
- camera/touch controls
- interactive/high-quality switch
- latest-frame-wins and backlog dropping
- baseline metrics and demo tooling

Next TODOs:

- WebRTC networking hardening (TURN/STUN + security)
- HPC production performance optimization
- end-to-end test suite and CI

## Implemented TODO Update

Implemented now:

- basic hardening:
  - optional websocket token (`VISIVO_AUTH_TOKEN`)
  - optional metrics endpoint token (`VISIVO_METRICS_TOKEN`)
  - configurable ICE servers (`VISIVO_ICE_SERVERS`)
- performance adaptation:
  - `targetFps` client -> server
  - `renderScale` client -> server
  - interactive auto-tuning based on `renderTimeMs`
- basic scalability:
  - session limit (`VISIVO_MAX_SESSIONS`) with LRU-like eviction
  - idle session cleanup (`VISIVO_IDLE_TIMEOUT_S`)
- minimal automated tests:
  - ICE config parsing
  - session manager eviction/idle cleanup
  - synthetic FITS validation with HDU selection and NaN/Inf sanitization
