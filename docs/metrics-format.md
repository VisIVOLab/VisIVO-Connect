# Metrics Format

Use a single JSON report to capture the measurements needed for demo readiness and performance review.

## Fields

- `schemaVersion`: report schema identifier, currently `1`.
- `generatedAt`: ISO-8601 timestamp for report creation.
- `build`: optional build or commit identifier.
- `environment`: runtime context, such as browser, device, network class, and viewport.
- `runs`: array of test runs.

Each run should record:

- `renderTimeMs`: time from data availability to first visible render.
- `encodeTimeMs`: time spent encoding the frame or payload.
- `networkLatencyMs`: estimated one-way or round-trip network latency, but label it consistently.
- `frameDeliveryLatencyMs`: time from frame ready to delivered/displayed.
- `inputToVisibleLatencyMs`: time from user input to visible UI update.
- `notes`: optional free-form annotations for anomalies.

## Minimal Report Shape

```json
{
  "schemaVersion": 1,
  "generatedAt": "2026-03-18T14:20:00Z",
  "build": "local-demo-build",
  "environment": {
    "device": "demo-laptop",
    "network": "wired",
    "viewport": "1440x900"
  },
  "runs": [
    {
      "label": "baseline",
      "samples": 20,
      "renderTimeMs": [12, 14, 11],
      "encodeTimeMs": [4, 5, 4],
      "networkLatencyMs": [18, 20, 19],
      "frameDeliveryLatencyMs": [32, 35, 31],
      "inputToVisibleLatencyMs": [54, 58, 52],
      "notes": "No packet loss."
    }
  ]
}
```

## Collection Guidance

- Record raw samples when possible.
- Keep the unit in milliseconds.
- Use the same clock source for all timings inside a single run.
- Separate estimated network latency from measured app latency so they can be compared without conflating transport and rendering.

## Report Output

The summary CLI in `tools/metrics/summarize-metrics.mjs` converts raw arrays into aggregate statistics:

- `count`
- `avg`
- `min`
- `p50`
- `p95`
- `max`

That lets you keep raw timing history while still producing a compact demo report.
