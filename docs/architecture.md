# Architecture

## Goal

Demonstrate remote scientific visualization with this split:

- datacube stored on HPC/server storage
- VTK rendering performed server-side (offscreen)
- browser client receives a remote stream and sends interaction events

## Final Architecture

### Render Plane

- Transport: WebRTC video track (`aiortc`)
- Producer: `LatestFrameVideoTrack`
- Source: `RemoteRenderSession.latest_frame()`
- Policy: latest-frame-wins
  - rendering thread overwrites previous frame buffer
  - track sends only newest serial
  - obsolete frames are dropped by design

### Control Plane

- Transport: WebSocket (`/ws`)
- Messages from client:
  - session bootstrap (`hello`)
  - interaction lifecycle (`interaction.start`, `interaction.end`)
  - camera controls (`camera.pointer`, `camera.wheel`, `camera.pinch`)
  - viewport updates (`resize`)
  - render control (`render.mode`, `render.params`)
- Messages from server:
  - signaling (`offer`, `ice`)
  - state (`state`)
  - telemetry acknowledgments (`pong`, `control-ack`)

### Session Layer

`SessionManager` keeps per-user session state:

- camera state in VTK renderer
- viewport size + dpr
- mode (`interactive` / `high-quality`)
- latest frame buffer + serial
- metrics samples

### Rendering Strategy

Implemented strategy for datacube volume rendering:

- High-quality mode:
  - full render scale
  - low sample distance
  - shading enabled
- Interactive mode:
  - reduced render scale
  - increased sample distance
  - shading disabled
  - outline visible

Switch policy:

- on `interaction.start` -> force `interactive`
- on `interaction.end` -> force `high-quality`

This gives fluid interaction while moving and best quality once input stops.

## Touch/Android Notes

- browser input uses Pointer Events + Wheel + Pinch logic
- fullscreen and responsive layout target tablet / large touch board
- interaction messages are normalized in [0,1] viewport coordinates for device-independent behavior
