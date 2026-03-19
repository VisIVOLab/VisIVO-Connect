# Protocol

Control and signaling share a single WebSocket at `/ws`.
Video stream uses WebRTC RTP media.

## Client -> Server

- `hello`
  - `sessionId`: string
  - `viewport`: `{ width, height, dpr }`
  - optional `datasetPath`
  - optional `token` (se auth abilitata)
- `resize`
  - `viewport`
- `interaction.start`
- `interaction.end`
- `camera.pointer`
  - `action`: `down|move|up`
  - normalized positions + deltas
- `camera.wheel`
  - wheel deltas and mode (`zoom|pan`)
- `camera.pinch`
  - `scale`
- `render.mode`
  - runtime profiles: `interactive|high-quality`
  - runtime visualization aliases accepted: `volume|isosurface|isosurface`
- `render.params`
  - supports: `mode`, `visualizationMode`, `visualization_mode`, `isoValue`, `volume`, `scale`, `targetFps`, `bitrateMbps` (hint)
- `answer`
  - WebRTC SDP answer
- `ice-candidate`
  - ICE candidate payload
- `ping`
  - optional telemetry ping (`ts` in milliseconds)
- `control-input`
  - test message used by `tools/control-burst-input.mjs`

## Server -> Client

- `offer`
  - WebRTC SDP offer for recv-only video peer
- `ice`
  - ICE candidate
- `stream-ready`
- `state`
  - current render mode and optional text
- `pong`
  - ping reply
- `control-ack`
  - acknowledgement for burst test message
- `error`
  - protocol/runtime errors

## Validation Harness

The backend tests use a fake renderer and a session shim to validate the
control-plane contract without depending on a live VTK renderer.

Examples used in the tests:

```json
{"type":"render.params","params":{"visualizationMode":"volume"}}
{"type":"render.params","params":{"visualizationMode":"isosurface"}}
{"type":"render.params","params":{"visualizationMode":"isosurface","isoValue":0.42,"volume":{"sampleDistanceScale":2.0},"scale":0.85,"targetFps":18}}
```

Current runtime supports both visualization modes (`volume`, `isosurface`)
plus quality profiles (`interactive`, `high-quality`).
