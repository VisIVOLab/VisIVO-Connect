# Demo Checklist

## Before The Demo

- Confirm dependencies are installed and backend starts (`uvicorn backend.main:app`).
- Verify the control websocket endpoint and any auth token.
- Run the burst-input test once and confirm acknowledgements or echo behavior.
- Generate a fresh metrics report from the latest run.
- Open the demo path in the target browser and clear stale tabs.
- Check audio, display scaling, and network stability.
- Prepare a fallback recording or screenshot set.

## Immediate Preflight

- Reload the app and verify the first render completes.
- Confirm the metrics numbers are within acceptable range.
- Verify the websocket control channel can accept a burst without disconnecting.
- Check browser devtools are closed unless actively debugging.
- Disable notifications and background sync interruptions.

## Demo Evidence To Capture

- Baseline metrics report
- Burst-input script output
- Any visible regressions or jitter
- Final screenshot or recording if the live demo fails
