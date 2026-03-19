# Bottleneck Notes

## What To Watch

- `renderTimeMs`
  - High values usually indicate expensive scene construction, layout work, or paint overhead.
- `encodeTimeMs`
  - High values point to serialization, compression, or frame packaging costs.
- `networkLatencyMs`
  - Good for separating transport delay from client-side rendering delay.
- `frameDeliveryLatencyMs`
  - Useful when frame production looks healthy but delivery to the user is delayed.
- `inputToVisibleLatencyMs`
  - The most user-visible end-to-end measure; this is the number to protect during demos.

## Likely Bottleneck Classes

- CPU bound
  - Long render or encode phases.
  - Symptoms include steady slowdowns and higher tail latency.
- Loader bound
  - FITS header scans, HDU selection, or large cube materialization.
  - Symptoms include slow initial frame availability before the render loop becomes active.
- Network bound
  - Uneven transport delay and delayed acknowledgements.
  - Symptoms include burst sensitivity and inconsistent delivery order.
- Event loop bound
  - Input handling stalls or delayed frame scheduling.
  - Symptoms include latency spikes after bursts of interaction.
- Browser bound
  - Main-thread contention, tab throttling, or heavy compositing.
  - Symptoms include visible stutter even when network metrics look fine.

## Demo Triage Order

1. Confirm input-to-visible latency.
2. Check frame-delivery latency.
3. Compare render time versus encode time.
4. Separate network latency from local processing.
5. Only then tune burst size or retry behavior.

## FITS-Specific Check

- If the first frame is delayed on FITS datasets, check loader cost before tuning renderer quality.
- If the first frame is visible but interaction lags, compare render time against the existing `.npy` baseline.
- If transport is healthy but delivery is slow, treat it as the same encoder/streaming investigation used for other volumes.

## Notes Template

- Observation:
- Suspected bottleneck:
- Supporting metric:
- Recovery action:
- Follow-up:
