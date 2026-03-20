const elements = {
  appShell: document.getElementById("appShell"),
  stageFrame: document.getElementById("stageFrame"),
  stageOverlay: document.getElementById("stageOverlay"),
  remoteVideo: document.getElementById("remoteVideo"),
  fallbackImage: document.getElementById("fallbackImage"),
  gestureLayer: document.getElementById("gestureLayer"),
  connectionState: document.getElementById("connectionState"),
  renderState: document.getElementById("renderState"),
  qualityBadge: document.getElementById("qualityBadge"),
  autoContrastButton: document.getElementById("autoContrastButton"),
  sessionId: document.getElementById("sessionId"),
  viewportValue: document.getElementById("viewportValue"),
  wsUrl: document.getElementById("wsUrl"),
  authToken: document.getElementById("authToken"),
  connectButton: document.getElementById("connectButton"),
  disconnectButton: document.getElementById("disconnectButton"),
  fullscreenButton: document.getElementById("fullscreenButton"),
  renderScale: document.getElementById("renderScale"),
  renderScaleValue: document.getElementById("renderScaleValue"),
  bitrate: document.getElementById("bitrate"),
  bitrateValue: document.getElementById("bitrateValue"),
  targetFps: document.getElementById("targetFps"),
  targetFpsValue: document.getElementById("targetFpsValue"),
  visualizationMode: document.getElementById("visualizationMode"),
  isoControls: document.getElementById("isoControls"),
  isoValue: document.getElementById("isoValue"),
  isoValueNumber: document.getElementById("isoValueNumber"),
  isoValueValue: document.getElementById("isoValueValue"),
  volumeControls: document.getElementById("volumeControls"),
  volumeRenderMode: document.getElementById("volumeRenderMode"),
  volumeOpacityScale: document.getElementById("volumeOpacityScale"),
  volumeOpacityScaleValue: document.getElementById("volumeOpacityScaleValue"),
  volumePalette: document.getElementById("volumePalette"),
  volumeScaleMode: document.getElementById("volumeScaleMode"),
  volumeSampleDistanceScale: document.getElementById("volumeSampleDistanceScale"),
  volumeSampleDistanceScaleValue: document.getElementById("volumeSampleDistanceScaleValue"),
  volumeImageSampleDistance: document.getElementById("volumeImageSampleDistance"),
  volumeImageSampleDistanceValue: document.getElementById("volumeImageSampleDistanceValue"),
  volumeShade: document.getElementById("volumeShade"),
  sliceControls: document.getElementById("sliceControls"),
  sliceAxis: document.getElementById("sliceAxis"),
  slicePosition: document.getElementById("slicePosition"),
  slicePositionValue: document.getElementById("slicePositionValue"),
  cropControls: document.getElementById("cropControls"),
  cropEnabled: document.getElementById("cropEnabled"),
  cropXMin: document.getElementById("cropXMin"),
  cropXMax: document.getElementById("cropXMax"),
  cropYMin: document.getElementById("cropYMin"),
  cropYMax: document.getElementById("cropYMax"),
  cropZMin: document.getElementById("cropZMin"),
  cropZMax: document.getElementById("cropZMax"),
  interactiveModeButton: document.getElementById("interactiveModeButton"),
  hqModeButton: document.getElementById("hqModeButton"),
  interactiveDownsample: document.getElementById("interactiveDownsample"),
  interactiveDownsampleValue: document.getElementById("interactiveDownsampleValue"),
  hqDetailPreset: document.getElementById("hqDetailPreset"),
  eventLog: document.getElementById("eventLog"),
  clearLogButton: document.getElementById("clearLogButton"),
  metricsStatus: document.getElementById("metricsStatus"),
  metricsSessionId: document.getElementById("metricsSessionId"),
  metricsVisualizationMode: document.getElementById("metricsVisualizationMode"),
  metricsDataset: document.getElementById("metricsDataset"),
  metricsFirstFrameLatency: document.getElementById("metricsFirstFrameLatency"),
  metricsFirstFrameSessionInit: document.getElementById("metricsFirstFrameSessionInit"),
  metricsFirstFrameSignalingSetup: document.getElementById("metricsFirstFrameSignalingSetup"),
  metricsFirstFrameFitsLoad: document.getElementById("metricsFirstFrameFitsLoad"),
  metricsFirstFrameSanitizeConvert: document.getElementById("metricsFirstFrameSanitizeConvert"),
  metricsFirstFrameVtkBuild: document.getElementById("metricsFirstFrameVtkBuild"),
  metricsFirstFrameRendererWarmup: document.getElementById("metricsFirstFrameRendererWarmup"),
  metricsFirstFrameRender: document.getElementById("metricsFirstFrameRender"),
  metricsFirstFrameCapture: document.getElementById("metricsFirstFrameCapture"),
  metricsFirstFrameConversion: document.getElementById("metricsFirstFrameConversion"),
  metricsFirstFrameEncode: document.getElementById("metricsFirstFrameEncode"),
  metricsFirstFrameSend: document.getElementById("metricsFirstFrameSend"),
  metricsInteractiveFps: document.getElementById("metricsInteractiveFps"),
  metricsHighQualityRenderTime: document.getElementById("metricsHighQualityRenderTime"),
  metricsMemoryRss: document.getElementById("metricsMemoryRss"),
  metricsRenderPath: document.getElementById("metricsRenderPath"),
  metricsCapabilityProfile: document.getElementById("metricsCapabilityProfile"),
  metricsRenderBackend: document.getElementById("metricsRenderBackend"),
  metricsVolumeMapper: document.getElementById("metricsVolumeMapper"),
  metricsOpenGLVendor: document.getElementById("metricsOpenGLVendor"),
  metricsOpenGLRenderer: document.getElementById("metricsOpenGLRenderer"),
  metricsOpenGLVersion: document.getElementById("metricsOpenGLVersion"),
  metricsGpuOffscreen: document.getElementById("metricsGpuOffscreen"),
  metricsCpuFallback: document.getElementById("metricsCpuFallback"),
  metricsFallbackReason: document.getElementById("metricsFallbackReason"),
  metricsWarmupRenderWindow: document.getElementById("metricsWarmupRenderWindow"),
  metricsWarmupDatasetLoad: document.getElementById("metricsWarmupDatasetLoad"),
  metricsWarmupScalarSummary: document.getElementById("metricsWarmupScalarSummary"),
  metricsWarmupScalarSummaryCacheHit: document.getElementById("metricsWarmupScalarSummaryCacheHit"),
  metricsWarmupScalarSummarySampleCount: document.getElementById("metricsWarmupScalarSummarySampleCount"),
  metricsWarmupVolumePipeline: document.getElementById("metricsWarmupVolumePipeline"),
  metricsWarmupOutline: document.getElementById("metricsWarmupOutline"),
  metricsWarmupSlice: document.getElementById("metricsWarmupSlice"),
  metricsWarmupIsosurface: document.getElementById("metricsWarmupIsosurface"),
  metricsWarmupSliceDeferred: document.getElementById("metricsWarmupSliceDeferred"),
  metricsWarmupIsosurfaceDeferred: document.getElementById("metricsWarmupIsosurfaceDeferred"),
  metricsWarmupSliceDeferredInit: document.getElementById("metricsWarmupSliceDeferredInit"),
  metricsWarmupIsosurfaceDeferredInit: document.getElementById("metricsWarmupIsosurfaceDeferredInit"),
  metricsWarmupFirstIsosurfaceActivation: document.getElementById("metricsWarmupFirstIsosurfaceActivation"),
  metricsWarmupAttach: document.getElementById("metricsWarmupAttach"),
  metricsWarmupCamera: document.getElementById("metricsWarmupCamera"),
  metricsWarmupCapabilityDetect: document.getElementById("metricsWarmupCapabilityDetect"),
  metricsWarmupProbeDeferred: document.getElementById("metricsWarmupProbeDeferred"),
  metricsWarmupProbeAfterRender: document.getElementById("metricsWarmupProbeAfterRender"),
  metricsWarmupFirstVisibleRender: document.getElementById("metricsWarmupFirstVisibleRender"),
  metricsWarmupHiddenPrewarm: document.getElementById("metricsWarmupHiddenPrewarm"),
  metricsWarmupHiddenPrewarmSize: document.getElementById("metricsWarmupHiddenPrewarmSize"),
  metricsWarmupTotal: document.getElementById("metricsWarmupTotal"),
  metricsEffectiveInteractiveScale: document.getElementById("metricsEffectiveInteractiveScale"),
  metricsEffectiveInteractiveSampleScale: document.getElementById("metricsEffectiveInteractiveSampleScale"),
  metricsEffectiveInteractiveImageSample: document.getElementById("metricsEffectiveInteractiveImageSample"),
  metricsEffectiveHqScale: document.getElementById("metricsEffectiveHqScale"),
  metricsEffectiveHqSampleScale: document.getElementById("metricsEffectiveHqSampleScale"),
  metricsEffectiveHqImageSample: document.getElementById("metricsEffectiveHqImageSample"),
  metricsEffectiveHqBitrate: document.getElementById("metricsEffectiveHqBitrate"),
  metricsActiveMapperClass: document.getElementById("metricsActiveMapperClass"),
  metricsRequestedMapperClass: document.getElementById("metricsRequestedMapperClass"),
  metricsSmartMapperRequestedMode: document.getElementById("metricsSmartMapperRequestedMode"),
  metricsSmartMapperLastUsedMode: document.getElementById("metricsSmartMapperLastUsedMode"),
  metricsPipelineRenderTime: document.getElementById("metricsPipelineRenderTime"),
  metricsPipelineCaptureTime: document.getElementById("metricsPipelineCaptureTime"),
  metricsPipelineConversionTime: document.getElementById("metricsPipelineConversionTime"),
  metricsPipelineEncodeTime: document.getElementById("metricsPipelineEncodeTime"),
  metricsPipelinePacingTime: document.getElementById("metricsPipelinePacingTime"),
  metricsPipelineTotalTime: document.getElementById("metricsPipelineTotalTime"),
  metricsRequestedBitrate: document.getElementById("metricsRequestedBitrate"),
  metricsStreamFrameSize: document.getElementById("metricsStreamFrameSize"),
  metricsDisplayScale: document.getElementById("metricsDisplayScale"),
  metricsIceRelayOnly: document.getElementById("metricsIceRelayOnly"),
  metricsIceGatheringTime: document.getElementById("metricsIceGatheringTime"),
  metricsIceFirstCandidate: document.getElementById("metricsIceFirstCandidate"),
  metricsIceSelectedCandidateTime: document.getElementById("metricsIceSelectedCandidateTime"),
  metricsIceSelectedCandidateType: document.getElementById("metricsIceSelectedCandidateType"),
  metricsIceCandidateCount: document.getElementById("metricsIceCandidateCount"),
  metricsIceCandidateSplit: document.getElementById("metricsIceCandidateSplit"),
  metricsIceFilteredSplit: document.getElementById("metricsIceFilteredSplit"),
  metricsIceConnectionState: document.getElementById("metricsIceConnectionState"),
  metricsPcConnectionState: document.getElementById("metricsPcConnectionState"),
  metricsFitsOpen: document.getElementById("metricsFitsOpen"),
  metricsHduSelect: document.getElementById("metricsHduSelect"),
  metricsSanitizeConvert: document.getElementById("metricsSanitizeConvert"),
  metricsVtkBuild: document.getElementById("metricsVtkBuild"),
  metricsFitsTotal: document.getElementById("metricsFitsTotal"),
  metricsFitsCacheHit: document.getElementById("metricsFitsCacheHit"),
  touchRotateSensitivity: document.getElementById("touchRotateSensitivity"),
  touchRotateSensitivityValue: document.getElementById("touchRotateSensitivityValue"),
  touchPanSensitivity: document.getElementById("touchPanSensitivity"),
  touchPanSensitivityValue: document.getElementById("touchPanSensitivityValue"),
  touchZoomSensitivity: document.getElementById("touchZoomSensitivity"),
  touchZoomSensitivityValue: document.getElementById("touchZoomSensitivityValue"),
  touchDeadZonePx: document.getElementById("touchDeadZonePx"),
  touchDeadZonePxValue: document.getElementById("touchDeadZonePxValue"),
  touchMoveClampPx: document.getElementById("touchMoveClampPx"),
  touchMoveClampPxValue: document.getElementById("touchMoveClampPxValue"),
  touchPinchClampPercent: document.getElementById("touchPinchClampPercent"),
  touchPinchClampPercentValue: document.getElementById("touchPinchClampPercentValue"),
  mouseRotateSensitivity: document.getElementById("mouseRotateSensitivity"),
  mouseRotateSensitivityValue: document.getElementById("mouseRotateSensitivityValue"),
  mousePanSensitivity: document.getElementById("mousePanSensitivity"),
  mousePanSensitivityValue: document.getElementById("mousePanSensitivityValue"),
  mouseZoomSensitivity: document.getElementById("mouseZoomSensitivity"),
  mouseZoomSensitivityValue: document.getElementById("mouseZoomSensitivityValue"),
  mouseMoveClampPx: document.getElementById("mouseMoveClampPx"),
  mouseMoveClampPxValue: document.getElementById("mouseMoveClampPxValue"),
  controlDrawerToggle: document.getElementById("controlDrawerToggle"),
  controlDrawerClose: document.getElementById("controlDrawerClose"),
};
const controlTabButtons = Array.from(document.querySelectorAll("[data-tab-target]"));
const controlTabPanels = Array.from(document.querySelectorAll("[data-tab-panel]"));

const state = {
  ws: null,
  wsUrl: "",
  reconnectTimer: null,
  reconnectAttempts: 0,
  reconnectEnabled: true,
  shouldReconnect: true,
  pc: null,
  iceServers: null,
  pendingRemoteIceCandidates: [],
  remoteStream: null,
  sessionId: createSessionId(),
  connectionState: "connecting",
  renderMode: "interactive",
  interactionActive: false,
  activePointers: new Map(),
  pointerBaseline: null,
  gestureStartDistance: 0,
  gestureStartScale: 1,
  pendingResize: 0,
  pendingInteractionEnd: 0,
  videoTrackFound: false,
  renderParams: {
    scale: 1,
    bitrate: 14,
    targetFps: 30,
  },
  visualization: {
    mode: "volume",
    isoValue: 0,
    isoRangeMin: -1,
    isoRangeMax: 1,
  },
  volume: {
    renderMode: "composite",
    palette: "Inferno",
    scaleMode: "linear",
    availablePalettes: ["Inferno"],
    opacityScale: 1.8,
    sampleDistanceScale: null,
    sampleDistanceManual: false,
    imageSampleDistance: null,
    imageSampleDistanceManual: false,
    shade: true,
    sliceAxis: "z",
    slicePosition: 0.5,
    cropping: {
      enabled: false,
      bounds: [0, 1, 0, 1, 0, 1],
    },
  },
  quality: {
    interactiveDownsample: 1.6,
    hqDetailPreset: "sharp",
  },
  ui: {
    activeTab: "session",
  },
  metrics: {
    pollTimer: 0,
    pending: false,
    lastSessionId: "",
  },
  touch: {
    rotateSensitivity: 0.45,
    panSensitivity: 0.4,
    zoomSensitivity: 0.35,
    deadZonePx: 2,
    moveClampPx: 24,
    pinchClampPercent: 5,
    pinchDeadZonePercent: 1.2,
    minSendIntervalMs: 16,
    rotateSmoothTauMs: 24,
    panSmoothTauMs: 30,
    pinchSmoothTauMs: 38,
  },
  mouse: {
    rotateSensitivity: 0.75,
    panSensitivity: 0.6,
    zoomSensitivity: 0.85,
    moveClampPx: 20,
    deadZonePx: 0.75,
  },
  touchGesture: {
    rafId: 0,
    pending: false,
    lastFlushTs: 0,
    smoothRotateDx: 0,
    smoothRotateDy: 0,
    smoothPanDx: 0,
    smoothPanDy: 0,
    smoothPinchLog: 0,
  },
  rtc: {
    offerReceivedAtMs: 0,
    connectedAtMs: 0,
    queuedRemoteIce: 0,
    appliedRemoteIce: 0,
    failedRemoteIce: 0,
    restartTimer: 0,
    lastRestartAtMs: 0,
    forceRelayOnly: false,
    statsTimer: 0,
    lastPairSummary: "",
    lastInboundBytes: 0,
    lastInboundFrames: 0,
    lastInboundTimestampMs: 0,
    lastInboundSummary: "",
  },
  transport: {
    forceWsFallback: false,
    fallbackTimer: 0,
    fallbackTimeoutMs: 7000,
    wsFallbackRequested: false,
    wsFallbackActive: false,
    wsFrameCount: 0,
  },
  display: {
    incomingFrameWidth: 0,
    incomingFrameHeight: 0,
  },
};

const DEFAULT_WS_URL = "/ws";
{
  const query = new URLSearchParams(window.location.search);
  const initialWsUrl = pickInitialWsUrl();
  state.rtc.forceRelayOnly = isTruthyQueryParam(query.get("relayOnly")) || isTruthyQueryParam(query.get("forceRelay"));
  state.transport.forceWsFallback = isTruthyQueryParam(query.get("wsFallback"));
  const fallbackTimeoutMs = Number(query.get("fallbackTimeoutMs"));
  if (Number.isFinite(fallbackTimeoutMs) && fallbackTimeoutMs >= 1000) {
    state.transport.fallbackTimeoutMs = Math.min(Math.round(fallbackTimeoutMs), 30000);
  }
  elements.wsUrl.value = initialWsUrl && initialWsUrl.trim() ? initialWsUrl.trim() : DEFAULT_WS_URL;
  console.info(
    "[VisIVO Connect] bootstrap wsUrl=",
    elements.wsUrl.value,
    "location=",
    window.location.href,
    "relayOnly=",
    state.rtc.forceRelayOnly,
    "wsFallback=",
    state.transport.forceWsFallback
  );
}
elements.sessionId.textContent = state.sessionId;
elements.renderScaleValue.textContent = formatScale(state.renderParams.scale);
elements.bitrateValue.textContent = formatBitrate(state.renderParams.bitrate);
elements.targetFpsValue.textContent = formatFps(state.renderParams.targetFps);
elements.interactiveDownsampleValue.textContent = `${state.quality.interactiveDownsample.toFixed(1)}x`;
elements.hqDetailPreset.value = state.quality.hqDetailPreset;
elements.visualizationMode.value = state.visualization.mode;
elements.volumePalette.value = state.volume.palette;
elements.volumeScaleMode.value = state.volume.scaleMode;
applyIsoRange(state.visualization.isoRangeMin, state.visualization.isoRangeMax);
elements.isoValue.value = String(state.visualization.isoValue);
elements.isoValueNumber.value = String(state.visualization.isoValue);
elements.isoValueValue.textContent = formatIso(state.visualization.isoValue);
syncVolumeControlsToUI();
toggleVisualizationControls();
setMode("interactive", false);
setConnectionState("connecting", "warn");
logEvent("Ready. Connect to begin.");
updateViewportValue();
syncTouchTuningUI();
syncMouseTuningUI();
installControlPanelUI();
elements.remoteVideo?.addEventListener("loadedmetadata", () => {
  state.display.incomingFrameWidth = Number(elements.remoteVideo.videoWidth || 0);
  state.display.incomingFrameHeight = Number(elements.remoteVideo.videoHeight || 0);
  logEvent(
    `Video loadedmetadata ${elements.remoteVideo.videoWidth}x${elements.remoteVideo.videoHeight} readyState=${elements.remoteVideo.readyState}`
  );
  const display = computeDisplayScaleSummary();
  if (display) {
    logEvent(`Display scale ${display}`);
  }
  const maybePlay = elements.remoteVideo.play?.();
  if (maybePlay && typeof maybePlay.catch === "function") {
    maybePlay.catch((error) => {
      logEvent(`Video play() rejected: ${error?.name || "Error"}`);
    });
  }
});
elements.remoteVideo?.addEventListener("playing", () => {
  logEvent(
    `Video playing readyState=${elements.remoteVideo.readyState} currentTime=${elements.remoteVideo.currentTime.toFixed(2)}`
  );
});
elements.remoteVideo?.addEventListener("waiting", () => {
  logEvent(`Video waiting readyState=${elements.remoteVideo.readyState}`);
});
elements.remoteVideo?.addEventListener("stalled", () => {
  logEvent(`Video stalled readyState=${elements.remoteVideo.readyState}`);
});
elements.remoteVideo?.addEventListener("error", () => {
  const err = elements.remoteVideo.error;
  logEvent(`Video error code=${err?.code || "unknown"}`);
});

elements.connectButton.addEventListener("click", () => {
  connect(elements.wsUrl.value.trim());
});

elements.disconnectButton.addEventListener("click", () => {
  disconnect(false);
});

elements.fullscreenButton.addEventListener("click", async () => {
  if (!document.fullscreenElement) {
    await elements.stageFrame.requestFullscreen?.();
  } else {
    await document.exitFullscreen?.();
  }
});

elements.clearLogButton.addEventListener("click", () => {
  elements.eventLog.textContent = "";
});

elements.autoContrastButton.addEventListener("click", () => {
  applyAutoContrastPreset();
  sendRenderParams();
  logEvent("Auto contrast preset applied");
});

elements.renderScale.addEventListener("input", () => {
  state.renderParams.scale = Number(elements.renderScale.value);
  elements.renderScaleValue.textContent = formatScale(state.renderParams.scale);
  sendRenderParams();
});

elements.bitrate.addEventListener("input", () => {
  state.renderParams.bitrate = Number(elements.bitrate.value);
  elements.bitrateValue.textContent = formatBitrate(state.renderParams.bitrate);
  sendRenderParams();
});
elements.targetFps.addEventListener("input", () => {
  state.renderParams.targetFps = Number(elements.targetFps.value);
  elements.targetFpsValue.textContent = formatFps(state.renderParams.targetFps);
  sendRenderParams();
});

elements.touchRotateSensitivity?.addEventListener("input", () => {
  state.touch.rotateSensitivity = clampFloat(Number(elements.touchRotateSensitivity.value), 0.1, 1.5, 0.45);
  syncTouchTuningUI();
});

elements.touchPanSensitivity?.addEventListener("input", () => {
  state.touch.panSensitivity = clampFloat(Number(elements.touchPanSensitivity.value), 0.1, 1.5, 0.4);
  syncTouchTuningUI();
});

elements.touchZoomSensitivity?.addEventListener("input", () => {
  state.touch.zoomSensitivity = clampFloat(Number(elements.touchZoomSensitivity.value), 0.1, 1.5, 0.35);
  syncTouchTuningUI();
});

elements.touchDeadZonePx?.addEventListener("input", () => {
  state.touch.deadZonePx = clampFloat(Number(elements.touchDeadZonePx.value), 0, 12, 2);
  syncTouchTuningUI();
});

elements.touchMoveClampPx?.addEventListener("input", () => {
  state.touch.moveClampPx = clampFloat(Number(elements.touchMoveClampPx.value), 4, 60, 24);
  syncTouchTuningUI();
});

elements.touchPinchClampPercent?.addEventListener("input", () => {
  state.touch.pinchClampPercent = clampFloat(Number(elements.touchPinchClampPercent.value), 1, 20, 5);
  syncTouchTuningUI();
});

elements.mouseRotateSensitivity?.addEventListener("input", () => {
  state.mouse.rotateSensitivity = clampFloat(Number(elements.mouseRotateSensitivity.value), 0.1, 1.5, 0.75);
  syncMouseTuningUI();
});

elements.mousePanSensitivity?.addEventListener("input", () => {
  state.mouse.panSensitivity = clampFloat(Number(elements.mousePanSensitivity.value), 0.1, 1.5, 0.6);
  syncMouseTuningUI();
});

elements.mouseZoomSensitivity?.addEventListener("input", () => {
  state.mouse.zoomSensitivity = clampFloat(Number(elements.mouseZoomSensitivity.value), 0.1, 1.5, 0.85);
  syncMouseTuningUI();
});

elements.mouseMoveClampPx?.addEventListener("input", () => {
  state.mouse.moveClampPx = clampFloat(Number(elements.mouseMoveClampPx.value), 4, 80, 20);
  syncMouseTuningUI();
});

elements.visualizationMode.addEventListener("change", () => {
  state.visualization.mode = elements.visualizationMode.value;
  toggleVisualizationControls();
  sendRenderParams();
});

elements.isoValue.addEventListener("input", () => {
  const value = Number(elements.isoValue.value);
  if (!Number.isFinite(value)) {
    return;
  }
  syncIsoControls(value);
  elements.isoValueValue.textContent = formatIso(state.visualization.isoValue);
  sendRenderParams();
});

elements.isoValueNumber.addEventListener("input", () => {
  const value = Number(elements.isoValueNumber.value);
  if (!Number.isFinite(value)) {
    return;
  }
  syncIsoControls(value);
  elements.isoValueValue.textContent = formatIso(state.visualization.isoValue);
  sendRenderParams();
});

elements.volumeRenderMode.addEventListener("change", () => {
  state.volume.renderMode = elements.volumeRenderMode.value;
  toggleVisualizationControls();
  sendRenderParams();
});

elements.volumeOpacityScale.addEventListener("input", () => {
  state.volume.opacityScale = Number(elements.volumeOpacityScale.value);
  elements.volumeOpacityScaleValue.textContent = formatFloat(state.volume.opacityScale);
  sendRenderParams();
});

elements.volumePalette.addEventListener("change", () => {
  state.volume.palette = elements.volumePalette.value || "Inferno";
  sendRenderParams();
});

elements.volumeScaleMode.addEventListener("change", () => {
  state.volume.scaleMode = elements.volumeScaleMode.value === "log" ? "log" : "linear";
  sendRenderParams();
});

elements.volumeSampleDistanceScale.addEventListener("input", () => {
  state.volume.sampleDistanceScale = Number(elements.volumeSampleDistanceScale.value);
  state.volume.sampleDistanceManual = true;
  elements.volumeSampleDistanceScaleValue.textContent = formatFloat(state.volume.sampleDistanceScale);
  sendRenderParams();
});

elements.volumeImageSampleDistance.addEventListener("input", () => {
  state.volume.imageSampleDistance = Math.max(1.0, Number(elements.volumeImageSampleDistance.value));
  state.volume.imageSampleDistanceManual = true;
  elements.volumeImageSampleDistanceValue.textContent = formatFloat(state.volume.imageSampleDistance);
  sendRenderParams();
});

elements.volumeShade.addEventListener("change", () => {
  state.volume.shade = Boolean(elements.volumeShade.checked);
  sendRenderParams();
});

elements.sliceAxis.addEventListener("change", () => {
  state.volume.sliceAxis = elements.sliceAxis.value;
  sendRenderParams();
});

elements.slicePosition.addEventListener("input", () => {
  state.volume.slicePosition = Number(elements.slicePosition.value);
  elements.slicePositionValue.textContent = formatFloat(state.volume.slicePosition);
  sendRenderParams();
});

elements.cropEnabled.addEventListener("change", () => {
  state.volume.cropping.enabled = Boolean(elements.cropEnabled.checked);
  sendRenderParams();
});

[
  elements.cropXMin,
  elements.cropXMax,
  elements.cropYMin,
  elements.cropYMax,
  elements.cropZMin,
  elements.cropZMax,
].forEach((el) => {
  el.addEventListener("input", () => {
    syncCropBoundsFromUI();
    sendRenderParams();
  });
});

elements.interactiveModeButton.addEventListener("click", () => {
  setMode("interactive", true);
});

elements.hqModeButton.addEventListener("click", () => {
  setMode("high-quality", true);
});

elements.interactiveDownsample.addEventListener("input", () => {
  state.quality.interactiveDownsample = Number(elements.interactiveDownsample.value);
  elements.interactiveDownsampleValue.textContent = `${state.quality.interactiveDownsample.toFixed(1)}x`;
  sendRenderParams();
});

elements.hqDetailPreset.addEventListener("change", () => {
  state.quality.hqDetailPreset = elements.hqDetailPreset.value;
  sendRenderParams();
});

document.addEventListener("fullscreenchange", () => {
  reportResize(true);
});

window.addEventListener("resize", () => reportResize());
window.addEventListener("orientationchange", () => reportResize(true));

const resizeObserver = new ResizeObserver(() => reportResize());
resizeObserver.observe(elements.stageFrame);

installGestureHandlers(elements.gestureLayer);

if (elements.wsUrl.value) {
  connect(elements.wsUrl.value.trim());
}

function connect(url) {
  const safeUrl = url && url.trim() ? url.trim() : DEFAULT_WS_URL;
  if (elements.wsUrl && !elements.wsUrl.value.trim()) {
    elements.wsUrl.value = safeUrl;
  }

  disconnect(true);
  const token = elements.authToken.value.trim();
  state.wsUrl = buildWsUrl(safeUrl, token);
  state.shouldReconnect = true;
  state.reconnectAttempts = 0;
  openSocket();
}

function openSocket() {
  clearTimeout(state.reconnectTimer);
  if (!state.wsUrl) {
    state.wsUrl = elements.wsUrl.value.trim();
  }

  setConnectionState(state.reconnectAttempts > 0 ? "reconnecting" : "connecting", state.reconnectAttempts > 0 ? "warn" : "subtle");
  logEvent(`WS connect ${state.wsUrl}`);

  let socket;
  try {
    socket = new WebSocket(state.wsUrl);
  } catch (error) {
    handleSocketError(error);
    return;
  }

  state.ws = socket;

  socket.addEventListener("open", () => {
    state.reconnectAttempts = 0;
    state.transport.wsFallbackRequested = false;
    state.transport.wsFallbackActive = false;
    state.transport.wsFrameCount = 0;
    showWebRtcVideo();
    elements.disconnectButton.disabled = false;
    elements.connectButton.disabled = true;
    setConnectionState("connected", "ok");
    logEvent("WS open");
    send({
      type: "hello",
      sessionId: state.sessionId,
      token: elements.authToken.value.trim() || undefined,
      ua: navigator.userAgent,
      viewport: currentViewport(),
      renderMode: state.renderMode,
      initialRenderParams: {
        mode: state.renderMode,
        scale: effectiveRenderScaleForMode(state.renderMode),
        bitrateMbps: effectiveBitrateForMode(state.renderMode),
        targetFps: state.renderParams.targetFps,
        visualizationMode: state.visualization.mode,
        isoValue: state.visualization.isoValue,
        volume: buildVolumeParamsPayload(),
        qualityProfiles: buildQualityProfilesPayload(),
      },
      forceRelayOnly: state.rtc.forceRelayOnly,
      forceWsFallback: state.transport.forceWsFallback,
    });
    sendRenderParams();
    reportResize(true);
    startMetricsPolling();
  });

  socket.addEventListener("message", (event) => {
    handleSocketMessage(event.data);
  });

  socket.addEventListener("close", (event) => {
    state.ws = null;
    state.transport.wsFallbackRequested = false;
    state.transport.wsFallbackActive = false;
    state.transport.wsFrameCount = 0;
    elements.fallbackImage.removeAttribute("src");
    showWebRtcVideo();
    elements.disconnectButton.disabled = true;
    elements.connectButton.disabled = false;
    stopMetricsPolling();
    clearWsFallbackTimer();
    cleanupPeerConnection();
    const closeText = `WS closed ${event.code}${event.reason ? ` ${event.reason}` : ""}`;
    logEvent(closeText);

    if (socket.__suppressReconnect) {
      return;
    }

    if (event.code === 4401) {
      setConnectionState("error", "danger", "Unauthorized token");
      state.shouldReconnect = false;
      return;
    }

    if (state.shouldReconnect && !event.wasClean) {
      scheduleReconnect();
    } else if (state.shouldReconnect) {
      scheduleReconnect();
    } else {
      setConnectionState("idle", "subtle");
    }
  });

  socket.addEventListener("error", (error) => {
    handleSocketError(error);
  });
}

function disconnect(manual = true) {
  state.shouldReconnect = !manual;
  clearTimeout(state.reconnectTimer);
  state.reconnectTimer = null;
  stopMetricsPolling();
  stopWsFallback("", false);

  if (state.ws) {
    try {
      state.ws.__suppressReconnect = true;
      state.ws.close(1000, manual ? "client disconnect" : "reconnect");
    } catch {}
  }

  state.ws = null;
  cleanupPeerConnection();
  elements.disconnectButton.disabled = true;
  elements.connectButton.disabled = false;
  setConnectionState(manual ? "idle" : "reconnecting", manual ? "subtle" : "warn");
}

function scheduleReconnect() {
  const delay = Math.min(1000 * 2 ** Math.min(state.reconnectAttempts, 5), 15000);
  state.reconnectAttempts += 1;
  setConnectionState("reconnecting", "warn", `Retrying in ${Math.round(delay / 1000)}s`);
  clearTimeout(state.reconnectTimer);
  state.reconnectTimer = window.setTimeout(() => {
    openSocket();
  }, delay);
}

function handleSocketError(error) {
  console.error(error);
  elements.stageOverlay.classList.remove("hidden");
  setConnectionState("error", "danger", "Socket error (check /ws URL)");
  logEvent("WS error");
}

function handleSocketMessage(raw) {
  let message = raw;
  if (typeof raw === "string") {
    try {
      message = JSON.parse(raw);
    } catch {
      logEvent(`RX text ${raw}`);
      return;
    }
  }

  if (!message || typeof message !== "object") {
    return;
  }

  switch (message.type) {
    case "offer":
    case "webrtc.offer":
      state.rtc.offerReceivedAtMs = performance.now();
      updateIceServersFromSignal(message.iceServers);
      maybeCreatePeerConnection();
      applyRemoteDescription(message.description || message);
      break;
    case "answer":
    case "webrtc.answer":
      applyRemoteDescription(message.description || message);
      break;
    case "ice":
    case "ice-candidate":
    case "webrtc.ice":
      addIceCandidate(message.candidate || message.iceCandidate || message);
      break;
    case "state":
    case "status":
      if (message.mode === "high-quality" || message.state === "high-quality") {
        setMode("high-quality", false);
      } else if (message.mode === "interactive" || message.state === "interactive") {
        setMode("interactive", false);
      }
      if (message.visualizationMode === "volume" || message.visualizationMode === "isosurface") {
        state.visualization.mode = message.visualizationMode;
        elements.visualizationMode.value = state.visualization.mode;
        toggleVisualizationControls();
      }
      const isoRangeMin = Number(message.isoRangeMin);
      const isoRangeMax = Number(message.isoRangeMax);
      if (Number.isFinite(isoRangeMin) && Number.isFinite(isoRangeMax) && isoRangeMax > isoRangeMin) {
        state.visualization.isoRangeMin = isoRangeMin;
        state.visualization.isoRangeMax = isoRangeMax;
        applyIsoRange(isoRangeMin, isoRangeMax);
      }
      const isoValue = Number(message.isoValue);
      if (Number.isFinite(isoValue)) {
        state.visualization.isoValue = isoValue;
        syncIsoControls(isoValue);
        elements.isoValueValue.textContent = formatIso(isoValue);
      }
      if (message.volume && typeof message.volume === "object") {
        mergeVolumeParams(message.volume);
        syncVolumeControlsToUI();
      }
      if (message.text) {
        logEvent(message.text);
      }
      break;
    case "stream-ready":
      logEvent("VisIVO Connect stream ready");
      break;
    case "ws-stream.started":
      state.transport.wsFallbackActive = true;
      logEvent(`WS fallback started (${Math.round(Number(message.fps) || 0)} fps)`);
      break;
    case "ws-stream.stopped":
      state.transport.wsFallbackActive = false;
      logEvent("WS fallback stopped");
      break;
    case "ws-frame":
      handleWsFrame(message);
      break;
    case "error":
      setConnectionState("error", "danger", message.message || "Server error");
      break;
    case "pong":
      break;
    default:
      logEvent(`RX ${message.type || "unknown"}`);
  }
}

function showWebRtcVideo() {
  elements.remoteVideo.classList.remove("hidden");
  elements.fallbackImage.classList.add("hidden");
}

function showWsFallbackImage() {
  elements.remoteVideo.classList.add("hidden");
  elements.fallbackImage.classList.remove("hidden");
}

function clearWsFallbackTimer() {
  clearTimeout(state.transport.fallbackTimer);
  state.transport.fallbackTimer = 0;
}

function scheduleWsFallbackTimer() {
  clearWsFallbackTimer();
  if (state.transport.forceWsFallback || state.transport.wsFallbackActive) {
    return;
  }
  state.transport.fallbackTimer = window.setTimeout(() => {
    state.transport.fallbackTimer = 0;
    const pc = state.pc;
    if (!pc || pc.connectionState === "connected") {
      return;
    }
    startWsFallback("rtc-timeout");
  }, state.transport.fallbackTimeoutMs);
}

function startWsFallback(reason = "manual") {
  clearWsFallbackTimer();
  if (!state.ws || state.ws.readyState !== WebSocket.OPEN) {
    return;
  }
  if (state.transport.wsFallbackRequested || state.transport.wsFallbackActive) {
    return;
  }
  cleanupPeerConnection();
  state.transport.wsFallbackRequested = true;
  state.transport.wsFrameCount = 0;
  send({ type: "webrtc.stop", sessionId: state.sessionId });
  send({
    type: "ws-stream.start",
    sessionId: state.sessionId,
    fps: Math.max(2, Math.min(12, Math.round(state.renderParams.targetFps / 2))),
  });
  showWsFallbackImage();
  setConnectionState("connected", "warn", "Fallback WS stream");
  logEvent(`WS fallback requested (${reason})`);
}

function stopWsFallback(reason = "rtc-connected", notifyServer = true) {
  clearWsFallbackTimer();
  if (notifyServer && (state.transport.wsFallbackRequested || state.transport.wsFallbackActive)) {
    send({ type: "ws-stream.stop", sessionId: state.sessionId });
  }
  state.transport.wsFallbackRequested = false;
  state.transport.wsFallbackActive = false;
  state.transport.wsFrameCount = 0;
  elements.fallbackImage.removeAttribute("src");
  showWebRtcVideo();
  if (reason) {
    logEvent(`WS fallback off (${reason})`);
  }
}

function handleWsFrame(message) {
  if (!message || typeof message.data !== "string" || !message.data) {
    return;
  }
  state.transport.wsFallbackRequested = false;
  state.transport.wsFallbackActive = true;
  state.transport.wsFrameCount += 1;
  showWsFallbackImage();
  elements.fallbackImage.src = `data:${message.mime || "image/jpeg"};base64,${message.data}`;
  elements.stageOverlay.classList.add("hidden");
  if (state.transport.wsFrameCount === 1) {
    logEvent("WS fallback frame received");
  }
}

function maybeCreatePeerConnection() {
  if (state.pc) {
    return state.pc;
  }
  if (state.transport.forceWsFallback) {
    return null;
  }

  const iceServers = Array.isArray(state.iceServers) ? state.iceServers : [];
  const pc = new RTCPeerConnection({
    iceServers,
    iceTransportPolicy: state.rtc.forceRelayOnly ? "relay" : "all",
  });
  logEvent(`RTC config ICE servers=${iceServers.length} relayOnly=${state.rtc.forceRelayOnly ? "on" : "off"}`);
  state.pc = pc;
  startRtcStatsPolling(pc);

  pc.addEventListener("track", (event) => {
    logEvent(`ontrack kind=${event.track?.kind || "unknown"} streams=${event.streams?.length || 0}`);
    const [stream] = event.streams;
    if (stream) {
      state.remoteStream = stream;
      elements.remoteVideo.srcObject = stream;
      logEvent(`video.srcObject set tracks=${stream.getTracks().length}`);
      const maybePlay = elements.remoteVideo.play?.();
      if (maybePlay && typeof maybePlay.catch === "function") {
        maybePlay.catch((error) => {
          logEvent(`Video play() rejected: ${error?.name || "Error"}`);
        });
      }
      state.videoTrackFound = true;
      stopWsFallback("", false);
      elements.stageOverlay.classList.add("hidden");
      logEvent("VisIVO Connect track attached");
    }
  });

  pc.addEventListener("icecandidate", (event) => {
    if (event.candidate) {
      logEvent(`Local ICE candidate (${event.candidate.type || "unknown"})`);
      send({
        type: "ice-candidate",
        candidate: event.candidate,
        sessionId: state.sessionId,
      });
    }
  });

  pc.addEventListener("connectionstatechange", () => {
    logEvent(`RTC ${pc.connectionState}`);
    if (pc.connectionState === "connected") {
      clearWsFallbackTimer();
      state.rtc.connectedAtMs = performance.now();
      if (state.rtc.offerReceivedAtMs > 0) {
        const connectMs = Math.max(0, state.rtc.connectedAtMs - state.rtc.offerReceivedAtMs);
        logEvent(
          `RTC connected in ${Math.round(connectMs)}ms · ICE queued=${state.rtc.queuedRemoteIce} applied=${state.rtc.appliedRemoteIce} failed=${state.rtc.failedRemoteIce}`
        );
      }
      elements.stageOverlay.classList.add("hidden");
      stopWsFallback("", false);
      setConnectionState("connected", "ok");
    }
    if (pc.connectionState === "failed" || pc.connectionState === "disconnected") {
      setConnectionState("reconnecting", "warn", "RTC reconnecting");
      scheduleRtcRestart(`rtc-${pc.connectionState}`);
    }
  });
  pc.addEventListener("iceconnectionstatechange", () => {
    logEvent(`RTC ice=${pc.iceConnectionState}`);
  });

  pc.addTransceiver("video", { direction: "recvonly" });
  scheduleWsFallbackTimer();
  return pc;
}

async function applyRemoteDescription(payload) {
  const pc = maybeCreatePeerConnection();
  if (!pc) {
    return;
  }
  const sdp = normalizeDescription(payload);
  if (!sdp) {
    return;
  }

  await pc.setRemoteDescription(sdp);
  await flushPendingRemoteIceCandidates(pc);
  if (sdp.type === "offer") {
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    send({
      type: "answer",
      sdp: pc.localDescription,
      sessionId: state.sessionId,
    });
  }
}

async function addIceCandidate(payload) {
  const pc = maybeCreatePeerConnection();
  if (!pc) {
    return;
  }
  const candidate = payload?.candidate ?? payload;
  if (!candidate) {
    return;
  }
  if (!pc.remoteDescription) {
    state.pendingRemoteIceCandidates.push(candidate);
    state.rtc.queuedRemoteIce += 1;
    return;
  }
  try {
    if (candidate && typeof candidate.candidate === "string") {
      const typeMatch = candidate.candidate.match(/\btyp\s+([a-z]+)/i);
      const type = typeMatch ? typeMatch[1] : "unknown";
      logEvent(`Remote ICE candidate (${type})`);
    }
    await pc.addIceCandidate(candidate);
    state.rtc.appliedRemoteIce += 1;
  } catch (error) {
    console.warn("Failed to add ICE candidate", error);
    state.rtc.failedRemoteIce += 1;
    logEvent("Failed to add remote ICE candidate");
  }
}

async function flushPendingRemoteIceCandidates(pc) {
  if (!pc?.remoteDescription || state.pendingRemoteIceCandidates.length === 0) {
    return;
  }
  const queued = state.pendingRemoteIceCandidates.splice(0, state.pendingRemoteIceCandidates.length);
  for (const candidate of queued) {
    try {
      if (candidate && typeof candidate.candidate === "string") {
        const typeMatch = candidate.candidate.match(/\btyp\s+([a-z]+)/i);
        const type = typeMatch ? typeMatch[1] : "unknown";
        logEvent(`Remote ICE candidate (${type})`);
      }
      await pc.addIceCandidate(candidate);
      state.rtc.appliedRemoteIce += 1;
    } catch (error) {
      console.warn("Failed to add queued ICE candidate", error);
      state.rtc.failedRemoteIce += 1;
      logEvent("Failed to add queued remote ICE candidate");
    }
  }
}

function scheduleRtcRestart(reason) {
  const now = performance.now();
  if (state.rtc.restartTimer) {
    return;
  }
  if (now - state.rtc.lastRestartAtMs < 1500) {
    return;
  }
  state.rtc.restartTimer = window.setTimeout(() => {
    state.rtc.restartTimer = 0;
    state.rtc.lastRestartAtMs = performance.now();
    logEvent(`RTC restart (${reason})`);
    if (!state.wsUrl) {
      return;
    }
    disconnect(false);
    openSocket();
  }, 250);
}

function cleanupPeerConnection() {
  clearWsFallbackTimer();
  clearTimeout(state.rtc.restartTimer);
  state.rtc.restartTimer = 0;
  clearTimeout(state.pendingInteractionEnd);
  if (state.touchGesture.rafId) {
    cancelAnimationFrame(state.touchGesture.rafId);
    state.touchGesture.rafId = 0;
  }
  state.touchGesture.pending = false;
  state.touchGesture.lastFlushTs = 0;
  state.touchGesture.smoothRotateDx = 0;
  state.touchGesture.smoothRotateDy = 0;
  state.touchGesture.smoothPanDx = 0;
  state.touchGesture.smoothPanDy = 0;
  state.touchGesture.smoothPinchLog = 0;
  state.interactionActive = false;
  state.activePointers.clear();
  state.pointerBaseline = null;
  state.gestureStartDistance = 0;
  state.gestureStartScale = 1;

  if (state.pc) {
    try {
      state.pc.getSenders().forEach((sender) => sender.track?.stop?.());
      state.pc.close();
    } catch {}
  }
  state.pc = null;
  clearInterval(state.rtc.statsTimer);
  state.rtc.statsTimer = 0;
  state.rtc.lastPairSummary = "";
  state.rtc.lastInboundBytes = 0;
  state.rtc.lastInboundFrames = 0;
  state.rtc.lastInboundTimestampMs = 0;
  state.rtc.lastInboundSummary = "";
  state.pendingRemoteIceCandidates = [];
  state.rtc.offerReceivedAtMs = 0;
  state.rtc.connectedAtMs = 0;
  state.rtc.queuedRemoteIce = 0;
  state.rtc.appliedRemoteIce = 0;
  state.rtc.failedRemoteIce = 0;
  state.remoteStream = null;
  state.videoTrackFound = false;
  elements.remoteVideo.srcObject = null;
  if (!state.transport.wsFallbackActive) {
    elements.stageOverlay.classList.remove("hidden");
  }
}

function startRtcStatsPolling(pc) {
  clearInterval(state.rtc.statsTimer);
  state.rtc.statsTimer = window.setInterval(() => {
    if (!state.pc || state.pc !== pc) {
      return;
    }
    logSelectedCandidatePair(state.pc);
    logInboundVideoStats(state.pc);
  }, 2000);
}

async function logSelectedCandidatePair(pc) {
  if (!pc || typeof pc.getStats !== "function") {
    return;
  }
  try {
    const stats = await pc.getStats();
    const pair = findSelectedCandidatePair(stats);
    if (!pair) {
      return;
    }
    const local = pair.localCandidateId ? stats.get(pair.localCandidateId) : null;
    const remote = pair.remoteCandidateId ? stats.get(pair.remoteCandidateId) : null;
    const localType = local?.candidateType || "unknown";
    const remoteType = remote?.candidateType || "unknown";
    const protocol = local?.protocol || pair.protocol || "unknown";
    const localAddr = local?.address || local?.ip || "?";
    const localPort = local?.port || "?";
    const remoteAddr = remote?.address || remote?.ip || "?";
    const remotePort = remote?.port || "?";
    const pairState = pair?.state || "?";
    const relaySelected = localType === "relay" || remoteType === "relay";
    const summary = `RTC pair ${localType}/${remoteType} ${protocol} ${localAddr}:${localPort}->${remoteAddr}:${remotePort} state=${pairState} relay=${relaySelected ? "yes" : "no"}`;
    if (summary !== state.rtc.lastPairSummary) {
      state.rtc.lastPairSummary = summary;
      logEvent(summary);
    }
  } catch {
    // ignore stats failures
  }
}

function findSelectedCandidatePair(stats) {
  let selectedId = null;
  for (const stat of stats.values()) {
    if (stat.type === "transport" && stat.selectedCandidatePairId) {
      selectedId = stat.selectedCandidatePairId;
      break;
    }
  }
  if (selectedId) {
    return stats.get(selectedId) || null;
  }
  for (const stat of stats.values()) {
    if (stat.type === "candidate-pair" && (stat.selected || stat.nominated || stat.state === "succeeded")) {
      return stat;
    }
  }
  return null;
}

async function logInboundVideoStats(pc) {
  if (!pc || typeof pc.getStats !== "function") {
    return;
  }
  try {
    const stats = await pc.getStats();
    let inbound = null;
    for (const stat of stats.values()) {
      if (stat.type === "inbound-rtp" && stat.kind === "video") {
        inbound = stat;
        break;
      }
    }
    if (!inbound) {
      return;
    }

    const bytes = Number(inbound.bytesReceived || 0);
    const frames = Number(inbound.framesDecoded || inbound.framesReceived || 0);
    const ts = Number(inbound.timestamp || performance.now());
    const dtMs = state.rtc.lastInboundTimestampMs > 0 ? ts - state.rtc.lastInboundTimestampMs : 0;
    const dBytes = state.rtc.lastInboundTimestampMs > 0 ? Math.max(0, bytes - state.rtc.lastInboundBytes) : 0;
    const dFrames = state.rtc.lastInboundTimestampMs > 0 ? Math.max(0, frames - state.rtc.lastInboundFrames) : 0;

    state.rtc.lastInboundTimestampMs = ts;
    state.rtc.lastInboundBytes = bytes;
    state.rtc.lastInboundFrames = frames;

    if (dtMs <= 0) {
      return;
    }
    const kbps = (dBytes * 8) / dtMs;
    const fps = (dFrames * 1000) / dtMs;
    const packetsLost = Number(inbound.packetsLost || 0);
    const jitter = Number(inbound.jitter || 0);
    const summary = `RTP in video ${kbps.toFixed(1)} kbps ${fps.toFixed(1)} fps lost=${packetsLost} jitter=${jitter.toFixed(4)}`;
    if (summary !== state.rtc.lastInboundSummary) {
      state.rtc.lastInboundSummary = summary;
      logEvent(summary);
    }
  } catch {
    // ignore stats failures
  }
}

function updateIceServersFromSignal(iceServers) {
  if (!Array.isArray(iceServers)) {
    return;
  }
  state.iceServers = iceServers
    .filter((entry) => entry && typeof entry === "object")
    .map((entry) => ({
      urls: entry.urls,
      username: entry.username,
      credential: entry.credential,
    }))
    .filter((entry) => entry.urls);
}

function send(payload) {
  if (!state.ws || state.ws.readyState !== WebSocket.OPEN) {
    return false;
  }
  state.ws.send(JSON.stringify(payload));
  return true;
}

function sendRenderParams() {
  const effectiveScale = effectiveRenderScaleForMode(state.renderMode);
  const effectiveBitrate = effectiveBitrateForMode(state.renderMode);
  send({
    type: "render.params",
    sessionId: state.sessionId,
    params: {
      mode: state.renderMode,
      scale: effectiveScale,
      bitrateMbps: effectiveBitrate,
      targetFps: state.renderParams.targetFps,
      visualizationMode: state.visualization.mode,
      isoValue: state.visualization.isoValue,
      volume: buildVolumeParamsPayload(),
      qualityProfiles: buildQualityProfilesPayload(),
    },
  });
  logEvent(
    `Render params scale=${effectiveScale.toFixed(2)} bitrate=${effectiveBitrate.toFixed(0)}Mbps vis=${state.visualization.mode} mode=${state.volume.renderMode} palette=${state.volume.palette} scaleMode=${state.volume.scaleMode} iso=${formatIso(state.visualization.isoValue)} interactiveDownsample=${state.quality.interactiveDownsample.toFixed(1)}x hq=${currentHqDetailPreset().label}`
  );
}

function setMode(mode, notify = true) {
  state.renderMode = mode;
  elements.interactiveModeButton.classList.toggle("active", mode === "interactive");
  elements.hqModeButton.classList.toggle("active", mode === "high-quality");
  elements.renderState.textContent = mode;
  elements.qualityBadge.textContent = mode;
  if (notify) {
    send({
      type: "render.mode",
      sessionId: state.sessionId,
      mode,
    });
    sendRenderParams();
    logEvent(`Mode ${mode}`);
  }
}

function setConnectionState(label, tone = "subtle", detail = "") {
  state.connectionState = label;
  elements.connectionState.textContent = detail ? `${label} · ${detail}` : label;
  elements.connectionState.dataset.tone = tone;
}

function reportResize(force = false) {
  clearTimeout(state.pendingResize);
  const flush = () => {
    const viewport = currentViewport();
    elements.viewportValue.textContent = `${viewport.width} x ${viewport.height} @ ${viewport.dpr.toFixed(2)}x`;
    send({
      type: "resize",
      sessionId: state.sessionId,
      viewport,
      fullscreen: Boolean(document.fullscreenElement),
    });
  };

  if (force) {
    flush();
    return;
  }

  state.pendingResize = window.setTimeout(flush, 80);
}

function currentViewport() {
  const rect = elements.stageFrame.getBoundingClientRect();
  return {
    width: Math.round(rect.width),
    height: Math.round(rect.height),
    dpr: window.devicePixelRatio || 1,
  };
}

function updateViewportValue() {
  const viewport = currentViewport();
  elements.viewportValue.textContent = `${viewport.width} x ${viewport.height} @ ${viewport.dpr.toFixed(2)}x`;
}

function installGestureHandlers(target) {
  const pointerMove = (event) => {
    const pointer = state.activePointers.get(event.pointerId);
    if (!pointer) {
      return;
    }

    const coalesced = typeof event.getCoalescedEvents === "function" ? event.getCoalescedEvents() : [event];
    const latest = coalesced.length > 0 ? coalesced[coalesced.length - 1] : event;
    const point = normalizePoint(latest);
    pointer.last = point;
    state.activePointers.set(event.pointerId, pointer);

    if (pointer.kind === "touch") {
      scheduleTouchGestureFlush();
      return;
    }

    if (state.activePointers.size === 1) {
      const prev = pointer.lastSent || point;
      const delta = normalizeDeltaFromPoints(prev, point);
      pointer.lastSent = point;
      state.activePointers.set(event.pointerId, pointer);
      const moveMode = event.buttons === 2 ? "pan" : "rotate";
      const tuned = tuneMouseDelta(delta.dx, delta.dy, moveMode);
      if (!tuned) {
        return;
      }
      sendInteractionMove({
        kind: pointer.kind,
        pointerId: event.pointerId,
        x: point.x,
        y: point.y,
        dx: tuned.dx,
        dy: tuned.dy,
        buttons: event.buttons,
        pressure: event.pressure,
      });
    } else if (state.activePointers.size >= 2) {
      const [first, second] = [...state.activePointers.values()];
      const center = midpoint(first.last, second.last);
      const firstPrev = first.lastSent || first.last;
      const secondPrev = second.lastSent || second.last;
      const prevDistance = Math.hypot(secondPrev.x - firstPrev.x, secondPrev.y - firstPrev.y);
      const distance = Math.hypot(second.last.x - first.last.x, second.last.y - first.last.y);
      let scale = prevDistance > 0 ? distance / prevDistance : 1;
      if (Number.isFinite(scale)) {
        const logDelta = Math.log(scale) * state.mouse.zoomSensitivity;
        const maxLog = Math.log(1 + state.touch.pinchClampPercent / 100);
        scale = clampFloat(Math.exp(clampFloat(logDelta, -maxLog, maxLog, 0)), 0.9, 1.1, 1);
      } else {
        scale = 1;
      }
      first.lastSent = first.last;
      second.lastSent = second.last;
      send({
        type: "camera.pinch",
        sessionId: state.sessionId,
        centerX: center.x,
        centerY: center.y,
        scale,
        baseScale: state.gestureStartScale,
      });
    }
  };

  const scheduleTouchGestureFlush = () => {
    state.touchGesture.pending = true;
    if (state.touchGesture.rafId) {
      return;
    }
    state.touchGesture.rafId = window.requestAnimationFrame((ts) => {
      state.touchGesture.rafId = 0;
      flushTouchGestures(ts);
    });
  };

  const flushTouchGestures = (tsMs) => {
    if (!state.touchGesture.pending) {
      return;
    }
    state.touchGesture.pending = false;

    if (state.activePointers.size === 0) {
      return;
    }

    const minInterval = state.touch.minSendIntervalMs;
    const sinceLast = tsMs - state.touchGesture.lastFlushTs;
    if (state.touchGesture.lastFlushTs > 0 && sinceLast < minInterval) {
      scheduleTouchGestureFlush();
      return;
    }

    const dtMs = state.touchGesture.lastFlushTs > 0 ? sinceLast : minInterval;
    state.touchGesture.lastFlushTs = tsMs;

    if (state.activePointers.size === 1) {
      const [entry] = [...state.activePointers.entries()];
      const [pointerId, pointer] = entry;
      if (pointer.kind !== "touch") {
        return;
      }
      const prev = pointer.lastSent || pointer.last;
      const delta = normalizeDeltaFromPoints(prev, pointer.last);
      pointer.lastSent = pointer.last;
      state.activePointers.set(pointerId, pointer);
      const tuned = tuneTouchDelta(delta.dx, delta.dy, "rotate", dtMs);
      if (!tuned) {
        return;
      }
      sendInteractionMove({
        kind: pointer.kind,
        pointerId,
        x: pointer.last.x,
        y: pointer.last.y,
        dx: tuned.dx,
        dy: tuned.dy,
        buttons: 1,
        pressure: 0.5,
      });
      return;
    }

    const [firstEntry, secondEntry] = [...state.activePointers.entries()];
    if (!firstEntry || !secondEntry) {
      return;
    }
    const [firstId, first] = firstEntry;
    const [, second] = secondEntry;
    if (first.kind !== "touch" || second.kind !== "touch") {
      return;
    }

    const firstPrev = first.lastSent || first.last;
    const secondPrev = second.lastSent || second.last;
    const centerPrev = midpoint(firstPrev, secondPrev);
    const centerNow = midpoint(first.last, second.last);
    const panDelta = normalizeDeltaFromPoints(centerPrev, centerNow);
    const tunedPan = tuneTouchDelta(panDelta.dx, panDelta.dy, "pan", dtMs);
    if (tunedPan) {
      sendInteractionMove({
        kind: "touch",
        pointerId: firstId,
        x: centerNow.x,
        y: centerNow.y,
        dx: tunedPan.dx,
        dy: tunedPan.dy,
        buttons: 2,
        pressure: 0.5,
      });
    }

    const prevDistance = Math.hypot(secondPrev.x - firstPrev.x, secondPrev.y - firstPrev.y);
    const nowDistance = Math.hypot(second.last.x - first.last.x, second.last.y - first.last.y);
    const pinchScale = tuneTouchPinchScale(prevDistance, nowDistance, dtMs);
    if (pinchScale !== null) {
      send({
        type: "camera.pinch",
        sessionId: state.sessionId,
        centerX: centerNow.x,
        centerY: centerNow.y,
        scale: pinchScale,
        baseScale: 1,
      });
    }

    first.lastSent = first.last;
    second.lastSent = second.last;
    state.activePointers.set(firstId, first);
    state.activePointers.set(secondEntry[0], second);
  };

  target.addEventListener("pointerdown", (event) => {
    if (event.button !== undefined && event.button !== 0 && event.pointerType !== "touch") {
      return;
    }
    target.setPointerCapture?.(event.pointerId);
    const point = normalizePoint(event);
    state.activePointers.set(event.pointerId, {
      kind: event.pointerType,
      start: point,
      last: point,
      lastSent: point,
    });
    if (!state.interactionActive) {
      startInteraction(event.pointerType);
    }
    if (!state.pointerBaseline) {
      state.pointerBaseline = point;
    }
    if (state.activePointers.size >= 2) {
      const [first, second] = [...state.activePointers.values()];
      state.gestureStartDistance = Math.hypot(second.last.x - first.last.x, second.last.y - first.last.y);
      state.gestureStartScale = 1;
      state.touchGesture.smoothPinchLog = 0;
    }
    send({
      type: "camera.pointer",
      sessionId: state.sessionId,
      action: "down",
      pointerId: event.pointerId,
      pointerType: event.pointerType,
      ...point,
      buttons: event.buttons,
      pressure: event.pressure,
    });
    logGesture("pointerdown", `${event.pointerType} ${Math.round(point.x)},${Math.round(point.y)}`);
  });

  target.addEventListener("pointermove", pointerMove);

  target.addEventListener("pointerup", finishPointer);
  target.addEventListener("pointercancel", finishPointer);

  target.addEventListener("wheel", (event) => {
    event.preventDefault();
    if (!state.interactionActive) {
      startInteraction("wheel");
    }
    const normalizedWheel = normalizeWheelDelta(event);
    const mouseClamp = Math.max(8, state.mouse.moveClampPx * 2);
    const mode = event.ctrlKey ? "zoom" : "pan";
    const wheelScale = mode === "zoom" ? state.mouse.zoomSensitivity : state.mouse.panSensitivity;
    const payload = {
      type: "camera.wheel",
      sessionId: state.sessionId,
      deltaX: clampFloat(normalizedWheel.deltaX * wheelScale, -mouseClamp, mouseClamp, 0),
      deltaY: clampFloat(normalizedWheel.deltaY * wheelScale, -mouseClamp, mouseClamp, 0),
      deltaMode: 0,
      ctrlKey: event.ctrlKey,
      shiftKey: event.shiftKey,
      altKey: event.altKey,
      mode,
    };
    send(payload);
    logGesture("wheel", `${payload.mode} ${Math.round(event.deltaX)},${Math.round(event.deltaY)}`);
    scheduleInteractionEnd();
  }, { passive: false });

  target.addEventListener("contextmenu", (event) => {
    event.preventDefault();
  });

  function finishPointer(event) {
    if (event.pointerType === "touch") {
      resetTouchGestureState();
    }
    send({
      type: "camera.pointer",
      sessionId: state.sessionId,
      action: "up",
      pointerId: event.pointerId,
      pointerType: event.pointerType,
      ...normalizePoint(event),
      buttons: event.buttons,
      pressure: event.pressure,
    });
    state.activePointers.delete(event.pointerId);
    if (state.activePointers.size < 2) {
      state.gestureStartDistance = 0;
      state.gestureStartScale = 1;
      state.touchGesture.smoothPinchLog = 0;
      const [remainingId, remainingPointer] = [...state.activePointers.entries()][0] || [];
      if (remainingPointer) {
        remainingPointer.lastSent = remainingPointer.last;
        state.activePointers.set(remainingId, remainingPointer);
      }
    }
    if (state.activePointers.size === 0) {
      state.pointerBaseline = null;
      resetTouchGestureState();
      scheduleInteractionEnd();
    }
    logGesture("pointerup", `${event.pointerType}`);
  }

  function resetTouchGestureState() {
    state.touchGesture.pending = false;
    state.touchGesture.lastFlushTs = 0;
    state.touchGesture.smoothRotateDx = 0;
    state.touchGesture.smoothRotateDy = 0;
    state.touchGesture.smoothPanDx = 0;
    state.touchGesture.smoothPanDy = 0;
    state.touchGesture.smoothPinchLog = 0;
  }
}

function startInteraction(source) {
  if (state.interactionActive) {
    return;
  }
  state.interactionActive = true;
  clearTimeout(state.pendingInteractionEnd);
  send({
    type: "interaction.start",
    sessionId: state.sessionId,
    source,
    viewport: currentViewport(),
    mode: state.renderMode,
  });
  logEvent(`Interaction start (${source})`);
}

function scheduleInteractionEnd() {
  clearTimeout(state.pendingInteractionEnd);
  state.pendingInteractionEnd = window.setTimeout(() => {
    if (state.activePointers.size > 0) {
      return;
    }
    if (!state.interactionActive) {
      return;
    }
    state.interactionActive = false;
    send({
      type: "interaction.end",
      sessionId: state.sessionId,
      viewport: currentViewport(),
      mode: state.renderMode,
    });
    logEvent("Interaction end");
  }, 180);
}

function sendInteractionMove(payload) {
  send({
    type: "camera.pointer",
    sessionId: state.sessionId,
    action: "move",
    ...payload,
  });
}

function normalizePoint(event) {
  const rect = elements.stageFrame.getBoundingClientRect();
  return {
    x: Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width)),
    y: Math.max(0, Math.min(1, (event.clientY - rect.top) / rect.height)),
  };
}

function midpoint(a, b) {
  return {
    x: (a.x + b.x) / 2,
    y: (a.y + b.y) / 2,
  };
}

function normalizeDeltaFromPoints(prev, next) {
  const rect = elements.stageFrame.getBoundingClientRect();
  const minSide = Math.max(1, Math.min(rect.width, rect.height));
  const dxPx = (next.x - prev.x) * rect.width;
  const dyPx = (next.y - prev.y) * rect.height;
  return {
    dx: dxPx / minSide,
    dy: dyPx / minSide,
  };
}

function tuneTouchDelta(dx, dy, mode, dtMs) {
  const deadZoneNorm = touchPxToNorm(state.touch.deadZonePx);
  let outDx = dx;
  let outDy = dy;
  let magnitude = Math.hypot(outDx, outDy);
  if (!Number.isFinite(magnitude) || magnitude < deadZoneNorm) {
    if (mode === "rotate") {
      state.touchGesture.smoothRotateDx = 0;
      state.touchGesture.smoothRotateDy = 0;
    } else {
      state.touchGesture.smoothPanDx = 0;
      state.touchGesture.smoothPanDy = 0;
    }
    return null;
  }

  const sensitivity = mode === "rotate" ? state.touch.rotateSensitivity : state.touch.panSensitivity;
  outDx *= sensitivity;
  outDy *= sensitivity;

  const clampNorm = touchPxToNorm(state.touch.moveClampPx);
  magnitude = Math.hypot(outDx, outDy);
  if (magnitude > clampNorm && magnitude > 0) {
    const ratio = clampNorm / magnitude;
    outDx *= ratio;
    outDy *= ratio;
  }

  const tau = mode === "rotate" ? state.touch.rotateSmoothTauMs : state.touch.panSmoothTauMs;
  const alpha = 1 - Math.exp(-Math.max(1, dtMs) / Math.max(1, tau));
  if (mode === "rotate") {
    state.touchGesture.smoothRotateDx += alpha * (outDx - state.touchGesture.smoothRotateDx);
    state.touchGesture.smoothRotateDy += alpha * (outDy - state.touchGesture.smoothRotateDy);
    return { dx: state.touchGesture.smoothRotateDx, dy: state.touchGesture.smoothRotateDy };
  }

  state.touchGesture.smoothPanDx += alpha * (outDx - state.touchGesture.smoothPanDx);
  state.touchGesture.smoothPanDy += alpha * (outDy - state.touchGesture.smoothPanDy);
  return { dx: state.touchGesture.smoothPanDx, dy: state.touchGesture.smoothPanDy };
}

function tuneTouchPinchScale(prevDistance, nowDistance, dtMs) {
  if (!Number.isFinite(prevDistance) || !Number.isFinite(nowDistance) || prevDistance <= 0 || nowDistance <= 0) {
    return null;
  }

  let logDelta = Math.log(nowDistance / prevDistance);
  if (!Number.isFinite(logDelta)) {
    return null;
  }

  const deadzoneLog = Math.log(1 + state.touch.pinchDeadZonePercent / 100);
  if (Math.abs(logDelta) < deadzoneLog) {
    state.touchGesture.smoothPinchLog = 0;
    return null;
  }

  logDelta *= state.touch.zoomSensitivity;
  const maxLog = Math.log(1 + state.touch.pinchClampPercent / 100);
  logDelta = clampFloat(logDelta, -maxLog, maxLog, 0);

  const alpha = 1 - Math.exp(-Math.max(1, dtMs) / Math.max(1, state.touch.pinchSmoothTauMs));
  state.touchGesture.smoothPinchLog += alpha * (logDelta - state.touchGesture.smoothPinchLog);

  if (Math.abs(state.touchGesture.smoothPinchLog) < 0.0008) {
    return null;
  }
  return clampFloat(Math.exp(state.touchGesture.smoothPinchLog), 0.9, 1.1, 1);
}

function touchPxToNorm(px) {
  const rect = elements.stageFrame.getBoundingClientRect();
  const minSide = Math.max(1, Math.min(rect.width, rect.height));
  return px / minSide;
}

function tuneMouseDelta(dx, dy, mode) {
  const deadZoneNorm = touchPxToNorm(state.mouse.deadZonePx);
  let outDx = dx;
  let outDy = dy;
  let magnitude = Math.hypot(outDx, outDy);
  if (!Number.isFinite(magnitude) || magnitude < deadZoneNorm) {
    return null;
  }

  const sensitivity = mode === "pan" ? state.mouse.panSensitivity : state.mouse.rotateSensitivity;
  outDx *= sensitivity;
  outDy *= sensitivity;

  const clampNorm = touchPxToNorm(state.mouse.moveClampPx);
  magnitude = Math.hypot(outDx, outDy);
  if (magnitude > clampNorm && magnitude > 0) {
    const ratio = clampNorm / magnitude;
    outDx *= ratio;
    outDy *= ratio;
  }
  return { dx: outDx, dy: outDy };
}

function normalizeWheelDelta(event) {
  let factor = 1;
  if (event.deltaMode === 1) {
    factor = 16;
  } else if (event.deltaMode === 2) {
    factor = Math.max(1, elements.stageFrame.getBoundingClientRect().height * 0.85);
  }
  return {
    deltaX: event.deltaX * factor,
    deltaY: event.deltaY * factor,
  };
}

function normalizeDescription(payload) {
  if (payload?.type && payload?.sdp) {
    return payload;
  }
  if (payload?.description?.type && payload?.description?.sdp) {
    return payload.description;
  }
  if (payload?.sdp && payload?.type) {
    return payload;
  }
  if (payload?.sdp && payload?.type !== undefined) {
    return { type: payload.type, sdp: payload.sdp };
  }
  return null;
}

function formatScale(value) {
  return `${Number(value).toFixed(2)}x`;
}

function formatBitrate(value) {
  return `${Number(value)} Mbps`;
}

function formatFps(value) {
  return `${Number(value)} fps`;
}

function formatIso(value) {
  return Number(value).toFixed(2);
}

function formatFloat(value) {
  return Number(value).toFixed(2);
}

function clampFloat(value, min, max, fallback) {
  if (!Number.isFinite(value)) {
    return fallback;
  }
  return Math.min(max, Math.max(min, value));
}

function syncTouchTuningUI() {
  if (elements.touchRotateSensitivity) {
    elements.touchRotateSensitivity.value = state.touch.rotateSensitivity.toFixed(2);
  }
  if (elements.touchRotateSensitivityValue) {
    elements.touchRotateSensitivityValue.textContent = formatFloat(state.touch.rotateSensitivity);
  }

  if (elements.touchPanSensitivity) {
    elements.touchPanSensitivity.value = state.touch.panSensitivity.toFixed(2);
  }
  if (elements.touchPanSensitivityValue) {
    elements.touchPanSensitivityValue.textContent = formatFloat(state.touch.panSensitivity);
  }

  if (elements.touchZoomSensitivity) {
    elements.touchZoomSensitivity.value = state.touch.zoomSensitivity.toFixed(2);
  }
  if (elements.touchZoomSensitivityValue) {
    elements.touchZoomSensitivityValue.textContent = formatFloat(state.touch.zoomSensitivity);
  }

  if (elements.touchDeadZonePx) {
    elements.touchDeadZonePx.value = state.touch.deadZonePx.toFixed(1);
  }
  if (elements.touchDeadZonePxValue) {
    elements.touchDeadZonePxValue.textContent = `${state.touch.deadZonePx.toFixed(1)} px`;
  }

  if (elements.touchMoveClampPx) {
    elements.touchMoveClampPx.value = String(Math.round(state.touch.moveClampPx));
  }
  if (elements.touchMoveClampPxValue) {
    elements.touchMoveClampPxValue.textContent = `${Math.round(state.touch.moveClampPx)} px`;
  }

  if (elements.touchPinchClampPercent) {
    elements.touchPinchClampPercent.value = String(Math.round(state.touch.pinchClampPercent));
  }
  if (elements.touchPinchClampPercentValue) {
    elements.touchPinchClampPercentValue.textContent = `${Math.round(state.touch.pinchClampPercent)}%`;
  }
}

function syncMouseTuningUI() {
  if (elements.mouseRotateSensitivity) {
    elements.mouseRotateSensitivity.value = state.mouse.rotateSensitivity.toFixed(2);
  }
  if (elements.mouseRotateSensitivityValue) {
    elements.mouseRotateSensitivityValue.textContent = formatFloat(state.mouse.rotateSensitivity);
  }

  if (elements.mousePanSensitivity) {
    elements.mousePanSensitivity.value = state.mouse.panSensitivity.toFixed(2);
  }
  if (elements.mousePanSensitivityValue) {
    elements.mousePanSensitivityValue.textContent = formatFloat(state.mouse.panSensitivity);
  }

  if (elements.mouseZoomSensitivity) {
    elements.mouseZoomSensitivity.value = state.mouse.zoomSensitivity.toFixed(2);
  }
  if (elements.mouseZoomSensitivityValue) {
    elements.mouseZoomSensitivityValue.textContent = formatFloat(state.mouse.zoomSensitivity);
  }

  if (elements.mouseMoveClampPx) {
    elements.mouseMoveClampPx.value = String(Math.round(state.mouse.moveClampPx));
  }
  if (elements.mouseMoveClampPxValue) {
    elements.mouseMoveClampPxValue.textContent = `${Math.round(state.mouse.moveClampPx)} px`;
  }
}

function toggleVisualizationControls() {
  const isIso = state.visualization.mode === "isosurface";
  const isVolume = state.visualization.mode === "volume";
  const isSlice = isVolume && state.volume.renderMode === "slice";
  elements.isoControls.classList.toggle("hidden", !isIso);
  elements.volumeControls.classList.toggle("hidden", !isVolume);
  elements.sliceControls.classList.toggle("hidden", !isSlice);
  elements.cropControls.classList.toggle("hidden", !isVolume);
}

function applyIsoRange(min, max) {
  elements.isoValue.min = String(min);
  elements.isoValue.max = String(max);
  elements.isoValueNumber.min = String(min);
  elements.isoValueNumber.max = String(max);
  syncIsoControls(state.visualization.isoValue);
}

function syncIsoControls(value) {
  const min = Number(elements.isoValue.min);
  const max = Number(elements.isoValue.max);
  const safe = Number.isFinite(value) ? value : 0;
  const clamped = Number.isFinite(min) && Number.isFinite(max) && max > min
    ? Math.min(max, Math.max(min, safe))
    : safe;
  state.visualization.isoValue = clamped;
  elements.isoValue.value = String(clamped);
  elements.isoValueNumber.value = clamped.toFixed(2);
}

function syncCropBoundsFromUI() {
  const raw = [
    Number(elements.cropXMin.value),
    Number(elements.cropXMax.value),
    Number(elements.cropYMin.value),
    Number(elements.cropYMax.value),
    Number(elements.cropZMin.value),
    Number(elements.cropZMax.value),
  ];
  state.volume.cropping.bounds = raw.map((v) => clamp01(v));
  elements.cropXMin.value = formatFloat(state.volume.cropping.bounds[0]);
  elements.cropXMax.value = formatFloat(state.volume.cropping.bounds[1]);
  elements.cropYMin.value = formatFloat(state.volume.cropping.bounds[2]);
  elements.cropYMax.value = formatFloat(state.volume.cropping.bounds[3]);
  elements.cropZMin.value = formatFloat(state.volume.cropping.bounds[4]);
  elements.cropZMax.value = formatFloat(state.volume.cropping.bounds[5]);
}

function syncVolumePaletteOptions() {
  const palettes = Array.isArray(state.volume.availablePalettes) && state.volume.availablePalettes.length > 0
    ? state.volume.availablePalettes
    : ["Inferno"];
  const selected = palettes.includes(state.volume.palette) ? state.volume.palette : palettes[0];
  const existing = Array.from(elements.volumePalette.options).map((option) => option.value);
  const needsRebuild = existing.length !== palettes.length || existing.some((value, index) => value !== palettes[index]);
  if (needsRebuild) {
    elements.volumePalette.replaceChildren(
      ...palettes.map((name) => {
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        return option;
      })
    );
  }
  state.volume.palette = selected;
  elements.volumePalette.value = selected;
}

function syncVolumeControlsToUI() {
  syncVolumePaletteOptions();
  elements.volumeRenderMode.value = state.volume.renderMode;
  elements.volumeScaleMode.value = state.volume.scaleMode === "log" ? "log" : "linear";
  elements.volumeOpacityScale.value = String(state.volume.opacityScale);
  elements.volumeOpacityScaleValue.textContent = formatFloat(state.volume.opacityScale);
  const sampleDistanceScale = effectiveVolumeSampleDistanceScale();
  const imageSampleDistance = effectiveVolumeImageSampleDistance();
  elements.volumeSampleDistanceScale.value = String(sampleDistanceScale);
  elements.volumeSampleDistanceScaleValue.textContent = Number.isFinite(state.volume.sampleDistanceScale)
    ? formatFloat(sampleDistanceScale)
    : "profile";
  elements.volumeImageSampleDistance.value = String(imageSampleDistance);
  elements.volumeImageSampleDistanceValue.textContent = Number.isFinite(state.volume.imageSampleDistance)
    ? formatFloat(imageSampleDistance)
    : "profile";
  elements.volumeShade.checked = Boolean(state.volume.shade);
  elements.sliceAxis.value = state.volume.sliceAxis;
  elements.slicePosition.value = String(state.volume.slicePosition);
  elements.slicePositionValue.textContent = formatFloat(state.volume.slicePosition);
  elements.cropEnabled.checked = Boolean(state.volume.cropping.enabled);
  syncCropBoundsFromUI();
  toggleVisualizationControls();
}

function mergeVolumeParams(incoming) {
  if (typeof incoming.renderMode === "string") {
    state.volume.renderMode = incoming.renderMode;
  }
  if (typeof incoming.palette === "string" && incoming.palette.trim()) {
    state.volume.palette = incoming.palette.trim();
  }
  if (typeof incoming.scaleMode === "string") {
    state.volume.scaleMode = incoming.scaleMode.toLowerCase().startsWith("log") ? "log" : "linear";
  }
  if (Array.isArray(incoming.availablePalettes) && incoming.availablePalettes.length > 0) {
    state.volume.availablePalettes = incoming.availablePalettes
      .filter((value) => typeof value === "string" && value.trim())
      .map((value) => value.trim());
  }
  if (Number.isFinite(incoming.opacityScale)) {
    state.volume.opacityScale = Number(incoming.opacityScale);
  }
  if (Number.isFinite(incoming.sampleDistanceScale)) {
    if (state.volume.sampleDistanceManual) {
      state.volume.sampleDistanceScale = Number(incoming.sampleDistanceScale);
    }
  }
  if (Number.isFinite(incoming.imageSampleDistance)) {
    if (state.volume.imageSampleDistanceManual) {
      state.volume.imageSampleDistance = Math.max(1.0, Number(incoming.imageSampleDistance));
    }
  }
  if (typeof incoming.shade === "boolean") {
    state.volume.shade = incoming.shade;
  }
  if (typeof incoming.sliceAxis === "string") {
    state.volume.sliceAxis = incoming.sliceAxis;
  }
  if (Number.isFinite(incoming.slicePosition)) {
    state.volume.slicePosition = clamp01(Number(incoming.slicePosition));
  }
  if (Number.isFinite(incoming.sliceIndex) && Number.isFinite(incoming.sliceMaxIndex) && incoming.sliceMaxIndex > 0) {
    state.volume.slicePosition = clamp01(Number(incoming.sliceIndex) / Number(incoming.sliceMaxIndex));
  }
  const cropping = incoming.cropping;
  if (cropping && typeof cropping === "object") {
    if (typeof cropping.enabled === "boolean") {
      state.volume.cropping.enabled = cropping.enabled;
    }
    if (Array.isArray(cropping.bounds) && cropping.bounds.length === 6) {
      state.volume.cropping.bounds = cropping.bounds.map((v) => clamp01(Number(v)));
    }
  }
}

function buildVolumeParamsPayload() {
  const payload = {
    renderMode: state.volume.renderMode,
    palette: state.volume.palette,
    scaleMode: state.volume.scaleMode,
    opacityScale: state.volume.opacityScale,
    shade: state.volume.shade,
    sliceAxis: state.volume.sliceAxis,
    slicePosition: state.volume.slicePosition,
    cropping: {
      enabled: state.volume.cropping.enabled,
      bounds: state.volume.cropping.bounds,
    },
  };
  payload.sampleDistanceScale = effectiveVolumeSampleDistanceScale(state.renderMode);
  payload.imageSampleDistance = effectiveVolumeImageSampleDistance(state.renderMode);
  return payload;
}

function applyAutoContrastPreset() {
  state.visualization.mode = "volume";
  elements.visualizationMode.value = "volume";

  if (state.volume.renderMode === "slice") {
    state.volume.renderMode = "composite";
  }

  if (state.volume.renderMode === "mip") {
    state.volume.opacityScale = 1.0;
    state.volume.sampleDistanceScale = null;
    state.volume.sampleDistanceManual = false;
    state.volume.imageSampleDistance = null;
    state.volume.imageSampleDistanceManual = false;
    state.volume.shade = false;
  } else {
    state.volume.renderMode = "composite";
    state.volume.opacityScale = 2.3;
    state.volume.sampleDistanceScale = null;
    state.volume.sampleDistanceManual = false;
    state.volume.imageSampleDistance = null;
    state.volume.imageSampleDistanceManual = false;
    state.volume.shade = true;
  }

  state.volume.cropping.enabled = false;
  state.volume.cropping.bounds = [0, 1, 0, 1, 0, 1];
  syncVolumeControlsToUI();
}

function clamp01(value) {
  if (!Number.isFinite(value)) {
    return 0;
  }
  return Math.min(1, Math.max(0, value));
}

const HQ_DETAIL_PRESETS = {
  balanced: {
    label: "Balanced",
    renderScaleBoost: 1.0,
    sampleDistanceScale: 0.95,
    bitrate: 14,
  },
  sharp: {
    label: "Sharp",
    renderScaleBoost: 1.2,
    sampleDistanceScale: 0.8,
    bitrate: 20,
  },
  ultra: {
    label: "Ultra",
    renderScaleBoost: 1.4,
    sampleDistanceScale: 0.7,
    bitrate: 28,
  },
};

function currentHqDetailPreset() {
  return HQ_DETAIL_PRESETS[state.quality.hqDetailPreset] || HQ_DETAIL_PRESETS.sharp;
}

function effectiveRenderScaleForMode(mode = state.renderMode) {
  const base = Number(state.renderParams.scale || 1);
  if (mode === "interactive") {
    return clampFloat(base / Math.max(state.quality.interactiveDownsample, 1.0), 0.4, 2.0, 1);
  }
  return clampFloat(base * currentHqDetailPreset().renderScaleBoost, 0.4, 2.0, 1);
}

function effectiveBitrateForMode(mode = state.renderMode) {
  const base = Number(state.renderParams.bitrate || 14);
  if (mode === "interactive") {
    return clampFloat(base, 1, 40, 14);
  }
  return clampFloat(Math.max(base, currentHqDetailPreset().bitrate), 1, 40, 14);
}

function buildQualityProfilesPayload() {
  return {
    interactive: {
      renderScale: effectiveRenderScaleForMode("interactive"),
      sampleDistanceScale: effectiveVolumeSampleDistanceScale("interactive"),
      imageSampleDistance: effectiveVolumeImageSampleDistance("interactive"),
      bitrateMbps: effectiveBitrateForMode("interactive"),
    },
    highQuality: {
      renderScale: effectiveRenderScaleForMode("high-quality"),
      sampleDistanceScale: effectiveVolumeSampleDistanceScale("high-quality"),
      imageSampleDistance: effectiveVolumeImageSampleDistance("high-quality"),
      bitrateMbps: effectiveBitrateForMode("high-quality"),
    },
  };
}

function defaultVolumeSampleDistanceScale(mode = state.renderMode) {
  if (state.volume.renderMode === "mip") {
    return mode === "interactive" ? 1.4 : 1.0;
  }
  if (mode === "interactive") {
    const dragPenalty = Math.max(state.quality.interactiveDownsample - 1.0, 0.0);
    return clampFloat(1.1 + dragPenalty * 0.8, 1.1, 2.4, 1.4);
  }
  return currentHqDetailPreset().sampleDistanceScale;
}

function defaultVolumeImageSampleDistance(mode = state.renderMode) {
  if (state.volume.renderMode === "mip") {
    return mode === "interactive" ? 1.6 : 1.0;
  }
  if (mode === "interactive") {
    const dragPenalty = Math.max(state.quality.interactiveDownsample - 1.0, 0.0);
    return clampFloat(1.35 + dragPenalty * 0.55, 1.0, 2.2, 1.6);
  }
  return 1.0;
}

function effectiveVolumeSampleDistanceScale(mode = state.renderMode) {
  if (Number.isFinite(state.volume.sampleDistanceScale) && state.volume.sampleDistanceManual) {
    return Number(state.volume.sampleDistanceScale);
  }
  return defaultVolumeSampleDistanceScale(mode);
}

function effectiveVolumeImageSampleDistance(mode = state.renderMode) {
  if (Number.isFinite(state.volume.imageSampleDistance) && state.volume.imageSampleDistanceManual) {
    return Math.max(1.0, Number(state.volume.imageSampleDistance));
  }
  return Math.max(1.0, defaultVolumeImageSampleDistance(mode));
}

function computeDisplayScaleSummary() {
  const frameWidth = Number(state.display.incomingFrameWidth || 0);
  const frameHeight = Number(state.display.incomingFrameHeight || 0);
  if (!frameWidth || !frameHeight) {
    return "";
  }
  const rect = elements.stageFrame.getBoundingClientRect();
  if (!(rect.width > 0 && rect.height > 0)) {
    return "";
  }
  const scale = Math.min(rect.width / frameWidth, rect.height / frameHeight);
  return `${scale.toFixed(2)}x (${Math.round(rect.width)}x${Math.round(rect.height)} / ${frameWidth}x${frameHeight})`;
}

function qualityProfileFallback(mode) {
  return {
    renderScale: effectiveRenderScaleForMode(mode),
    sampleDistanceScale: effectiveVolumeSampleDistanceScale(mode),
    imageSampleDistance: effectiveVolumeImageSampleDistance(mode),
    bitrateMbps: effectiveBitrateForMode(mode),
  };
}

function createSessionId() {
  const c = typeof globalThis !== "undefined" ? globalThis.crypto : undefined;
  if (c && typeof c.randomUUID === "function") {
    return c.randomUUID();
  }

  // RFC4122-ish fallback for older browsers/environments.
  if (c && typeof c.getRandomValues === "function") {
    const bytes = new Uint8Array(16);
    c.getRandomValues(bytes);
    bytes[6] = (bytes[6] & 0x0f) | 0x40;
    bytes[8] = (bytes[8] & 0x3f) | 0x80;
    const hex = [...bytes].map((b) => b.toString(16).padStart(2, "0"));
    return `${hex.slice(0, 4).join("")}-${hex.slice(4, 6).join("")}-${hex.slice(6, 8).join("")}-${hex.slice(8, 10).join("")}-${hex.slice(10, 16).join("")}`;
  }

  return `session-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function installControlPanelUI() {
  const setActiveTab = (tabKey) => {
    state.ui.activeTab = tabKey;
    controlTabButtons.forEach((button) => {
      const active = button.dataset.tabTarget === tabKey;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", active ? "true" : "false");
    });
    controlTabPanels.forEach((panel) => {
      const active = panel.dataset.tabPanel === tabKey;
      panel.classList.toggle("active", active);
    });
    if (tabKey === "metrics") {
      fetchMetricsNow(true);
    }
  };

  controlTabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const tabKey = button.dataset.tabTarget;
      if (tabKey) {
        setActiveTab(tabKey);
      }
    });
  });

  const openDrawer = () => elements.appShell.classList.add("controls-open");
  const closeDrawer = () => elements.appShell.classList.remove("controls-open");
  elements.controlDrawerToggle?.addEventListener("click", openDrawer);
  elements.controlDrawerClose?.addEventListener("click", closeDrawer);

  elements.stageFrame?.addEventListener("pointerdown", () => {
    if (window.matchMedia("(max-width: 1120px)").matches) {
      closeDrawer();
    }
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeDrawer();
    }
  });
}

function startMetricsPolling() {
  if (state.metrics.pollTimer) {
    return;
  }
  setMetricsStatus("loading");
  fetchMetricsNow(true);
  state.metrics.pollTimer = window.setInterval(() => {
    fetchMetricsNow();
  }, 2500);
}

function stopMetricsPolling() {
  clearInterval(state.metrics.pollTimer);
  state.metrics.pollTimer = 0;
  state.metrics.pending = false;
  setMetricsStatus("idle");
}

async function fetchMetricsNow(force = false) {
  if (state.metrics.pending && !force) {
    return;
  }
  if (!state.sessionId) {
    setMetricsStatus("waiting");
    return;
  }
  if (!state.ws || state.ws.readyState !== WebSocket.OPEN) {
    setMetricsStatus("waiting");
    return;
  }

  state.metrics.pending = true;
  if (state.ui.activeTab === "metrics") {
    setMetricsStatus("loading");
  }

  try {
    const url = buildMetricsUrl();
    const response = await fetch(url, { method: "GET", cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const payload = await response.json();
    state.metrics.lastSessionId = payload.sessionId || "";
    renderMetrics(payload);
    if (state.ui.activeTab === "metrics") {
      setMetricsStatus("ok");
    }
  } catch (error) {
    if (state.ui.activeTab === "metrics") {
      setMetricsStatus("error");
    }
    console.warn("Metrics fetch failed", error);
  } finally {
    state.metrics.pending = false;
  }
}

function buildMetricsUrl() {
  const base = `/api/metrics/${encodeURIComponent(state.sessionId)}`;
  const token = elements.authToken?.value?.trim();
  if (!token) {
    return base;
  }
  return `${base}?token=${encodeURIComponent(token)}`;
}

function renderMetrics(payload) {
  const runtime = payload?.runtimeMetrics || {};
  const importMetrics = payload?.importMetrics || {};
  const renderer = payload?.rendererDiagnostics || {};
  const warmup = renderer?.warmupMetrics || {};
  const pipeline = payload?.pipelineMetrics || {};
  const effectiveQualityProfiles = payload?.effectiveQualityProfiles || {};
  const ice = payload?.iceMetrics || {};
  const datasetName = payload?.datasetName || payload?.datasetPath || "-";
  const interactiveProfile = effectiveQualityProfiles.interactive || qualityProfileFallback("interactive");
  const highQualityProfile = effectiveQualityProfiles.highQuality || qualityProfileFallback("high-quality");

  setText(elements.metricsSessionId, payload?.sessionId || state.sessionId || "-");
  setText(elements.metricsVisualizationMode, payload?.visualizationMode || "-");
  setText(elements.metricsDataset, datasetName);
  setText(elements.metricsFirstFrameLatency, formatMs(runtime.firstFrameLatencyMs));
  setText(elements.metricsFirstFrameSessionInit, formatMs(runtime.firstFrameSessionInitMs));
  setText(elements.metricsFirstFrameSignalingSetup, formatMs(runtime.firstFrameSignalingSetupMs));
  setText(elements.metricsFirstFrameFitsLoad, formatMs(runtime.firstFrameFitsLoadMs));
  setText(elements.metricsFirstFrameSanitizeConvert, formatMs(runtime.firstFrameSanitizeConvertMs));
  setText(elements.metricsFirstFrameVtkBuild, formatMs(runtime.firstFrameVtkBuildMs));
  setText(elements.metricsFirstFrameRendererWarmup, formatMs(runtime.firstFrameRendererWarmupMs));
  setText(elements.metricsFirstFrameRender, formatMs(runtime.firstFrameRenderMs));
  setText(elements.metricsFirstFrameCapture, formatMs(runtime.firstFrameCaptureMs));
  setText(elements.metricsFirstFrameConversion, formatMs(runtime.firstFrameConversionMs));
  setText(elements.metricsFirstFrameEncode, formatMs(runtime.firstFrameEncodeMs));
  setText(elements.metricsFirstFrameSend, formatMs(runtime.firstFrameSendMs));
  setText(elements.metricsInteractiveFps, formatNumber(runtime.interactiveFps, "fps"));
  setText(elements.metricsHighQualityRenderTime, formatMs(runtime.highQualityRenderTimeMs));
  setText(elements.metricsMemoryRss, formatNumber(runtime.memoryRssMb, "MB"));
  setText(elements.metricsRenderPath, renderer.selectedRenderPath || "-");
  setText(elements.metricsCapabilityProfile, renderer.capabilityProfile || "-");
  setText(elements.metricsRenderBackend, renderer.renderWindowBackend || "-");
  setText(elements.metricsVolumeMapper, renderer.volumeMapperClass || renderer.activeMapper || "-");
  setText(elements.metricsOpenGLVendor, renderer.openGLVendor || "-");
  setText(elements.metricsOpenGLRenderer, renderer.openGLRenderer || "-");
  setText(elements.metricsOpenGLVersion, renderer.openGLVersion || "-");
  setText(elements.metricsGpuOffscreen, formatBoolean(renderer.gpuOffscreenAvailable));
  setText(elements.metricsCpuFallback, formatBoolean(renderer.cpuFallbackAvailable));
  setText(elements.metricsFallbackReason, renderer.fallbackReason || "-");
  setText(elements.metricsWarmupRenderWindow, formatMs(warmup.renderWindowCreationMs));
  setText(elements.metricsWarmupDatasetLoad, formatMs(warmup.datasetLoadMs));
  setText(elements.metricsWarmupScalarSummary, formatMs(warmup.scalarSummaryMs));
  setText(elements.metricsWarmupScalarSummaryCacheHit, formatBoolean(warmup.scalarSummaryCacheHit));
  setText(elements.metricsWarmupScalarSummarySampleCount, formatInteger(warmup.scalarSummarySampleCount));
  setText(elements.metricsWarmupVolumePipeline, formatMs(warmup.volumePipelineInitMs));
  setText(elements.metricsWarmupOutline, formatMs(warmup.outlinePipelineInitMs));
  setText(elements.metricsWarmupSlice, formatMs(warmup.slicePipelineInitMs));
  setText(elements.metricsWarmupIsosurface, formatMs(warmup.isosurfacePipelineInitMs));
  setText(elements.metricsWarmupSliceDeferred, formatBoolean(warmup.slicePipelineDeferred));
  setText(elements.metricsWarmupIsosurfaceDeferred, formatBoolean(warmup.isosurfacePipelineDeferred));
  setText(elements.metricsWarmupSliceDeferredInit, formatMs(warmup.sliceDeferredInitMs));
  setText(elements.metricsWarmupIsosurfaceDeferredInit, formatMs(warmup.isosurfaceDeferredInitMs));
  setText(elements.metricsWarmupFirstIsosurfaceActivation, formatMs(warmup.firstIsosurfaceActivationMs));
  setText(elements.metricsWarmupAttach, formatMs(warmup.scenePropAttachMs));
  setText(elements.metricsWarmupCamera, formatMs(warmup.cameraResetMs));
  setText(elements.metricsWarmupCapabilityDetect, formatMs(warmup.capabilityDetectionMs));
  setText(elements.metricsWarmupProbeDeferred, formatBoolean(warmup.capabilityProbeDeferred));
  setText(elements.metricsWarmupProbeAfterRender, formatMs(warmup.capabilityProbeAfterRenderMs));
  setText(elements.metricsWarmupFirstVisibleRender, formatMs(warmup.firstVisibleRenderWarmupMs));
  setText(elements.metricsWarmupHiddenPrewarm, formatMs(warmup.hiddenVolumePrewarmMs));
  setText(
    elements.metricsWarmupHiddenPrewarmSize,
    Number.isFinite(warmup.hiddenVolumePrewarmWidth) && Number.isFinite(warmup.hiddenVolumePrewarmHeight)
      ? `${formatInteger(warmup.hiddenVolumePrewarmWidth)}x${formatInteger(warmup.hiddenVolumePrewarmHeight)}`
      : "-"
  );
  setText(elements.metricsWarmupTotal, formatMs(warmup.totalRendererWarmupMs));
  setText(elements.metricsEffectiveInteractiveScale, formatScale(interactiveProfile.renderScale));
  setText(elements.metricsEffectiveInteractiveSampleScale, formatFloat(interactiveProfile.sampleDistanceScale));
  setText(elements.metricsEffectiveInteractiveImageSample, formatFloat(interactiveProfile.imageSampleDistance));
  setText(elements.metricsEffectiveHqScale, formatScale(highQualityProfile.renderScale));
  setText(elements.metricsEffectiveHqSampleScale, formatFloat(highQualityProfile.sampleDistanceScale));
  setText(elements.metricsEffectiveHqImageSample, formatFloat(highQualityProfile.imageSampleDistance));
  setText(elements.metricsEffectiveHqBitrate, formatBitrate(highQualityProfile.bitrateMbps));
  setText(elements.metricsActiveMapperClass, pipeline.activeMapperClass || renderer.activeMapperClass || "-");
  setText(elements.metricsRequestedMapperClass, pipeline.requestedMapperClass || renderer.requestedMapperClass || "-");
  setText(elements.metricsSmartMapperRequestedMode, pipeline.smartMapperRequestedMode || renderer.smartMapperRequestedMode || "-");
  setText(elements.metricsSmartMapperLastUsedMode, pipeline.smartMapperLastUsedMode || renderer.smartMapperLastUsedMode || "-");
  setText(elements.metricsRequestedBitrate, formatBitrate(effectiveBitrateForMode(state.renderMode)));
  setText(
    elements.metricsStreamFrameSize,
    Number.isFinite(pipeline.frameWidth) && Number.isFinite(pipeline.frameHeight)
      ? `${formatInteger(pipeline.frameWidth)}x${formatInteger(pipeline.frameHeight)}`
      : state.display.incomingFrameWidth > 0 && state.display.incomingFrameHeight > 0
        ? `${formatInteger(state.display.incomingFrameWidth)}x${formatInteger(state.display.incomingFrameHeight)}`
        : "-"
  );
  setText(elements.metricsDisplayScale, computeDisplayScaleSummary() || "-");
  setText(elements.metricsPipelineRenderTime, formatMs(pipeline.renderTimeMs));
  setText(elements.metricsPipelineCaptureTime, formatMs(pipeline.frameCaptureReadbackTimeMs));
  setText(elements.metricsPipelineConversionTime, formatMs(pipeline.frameConversionTimeMs));
  setText(elements.metricsPipelineEncodeTime, formatMs(pipeline.encodeTimeMs));
  setText(elements.metricsPipelinePacingTime, formatMs(pipeline.rtpPacingTimeMs));
  setText(elements.metricsPipelineTotalTime, formatMs(pipeline.totalFramePipelineTimeMs));
  setText(elements.metricsIceRelayOnly, formatBoolean(ice.relayOnly));
  setText(elements.metricsIceGatheringTime, formatMs(ice.iceGatheringTimeMs));
  setText(elements.metricsIceFirstCandidate, formatMs(ice.timeToFirstCandidateMs));
  setText(elements.metricsIceSelectedCandidateTime, formatMs(ice.timeToSelectedCandidateMs));
  setText(elements.metricsIceSelectedCandidateType, ice.selectedCandidateType || "-");
  setText(elements.metricsIceCandidateCount, formatInteger(ice.candidateCount));
  setText(
    elements.metricsIceCandidateSplit,
    `${formatInteger(ice.localCandidateCount)}/${formatInteger(ice.remoteCandidateCount)}`
  );
  setText(
    elements.metricsIceFilteredSplit,
    `${formatInteger(ice.filteredLocalCandidateCount)}/${formatInteger(ice.filteredRemoteCandidateCount)}`
  );
  setText(elements.metricsIceConnectionState, ice.iceConnectionState || "-");
  setText(elements.metricsPcConnectionState, ice.connectionState || "-");

  setText(elements.metricsFitsOpen, formatMs(importMetrics.fitsOpenMs));
  setText(elements.metricsHduSelect, formatMs(importMetrics.hduSelectMs));
  setText(elements.metricsSanitizeConvert, formatMs(importMetrics.sanitizeConvertMs));
  setText(elements.metricsVtkBuild, formatMs(importMetrics.vtkBuildMs));
  setText(elements.metricsFitsTotal, formatMs(importMetrics.fitsTotalMs));
  setText(elements.metricsFitsCacheHit, formatBoolean(importMetrics.cacheHit));
}

function formatBoolean(value) {
  if (value === true) {
    return "yes";
  }
  if (value === false) {
    return "no";
  }
  return "-";
}

function setMetricsStatus(status) {
  if (!elements.metricsStatus) {
    return;
  }
  if (status === "ok") {
    elements.metricsStatus.textContent = "live";
    elements.metricsStatus.classList.remove("subtle");
    return;
  }
  if (status === "loading") {
    elements.metricsStatus.textContent = "loading";
    elements.metricsStatus.classList.add("subtle");
    return;
  }
  if (status === "waiting") {
    elements.metricsStatus.textContent = "waiting";
    elements.metricsStatus.classList.add("subtle");
    return;
  }
  if (status === "error") {
    elements.metricsStatus.textContent = "error";
    elements.metricsStatus.classList.add("subtle");
    return;
  }
  elements.metricsStatus.textContent = "idle";
  elements.metricsStatus.classList.add("subtle");
}

function setText(el, value) {
  if (!el) {
    return;
  }
  el.textContent = value ?? "-";
}

function formatMs(value) {
  if (!Number.isFinite(value)) {
    return "-";
  }
  return `${Number(value).toFixed(1)} ms`;
}

function formatNumber(value, unit) {
  if (!Number.isFinite(value)) {
    return "-";
  }
  return `${Number(value).toFixed(2)} ${unit}`;
}

function formatInteger(value) {
  if (!Number.isFinite(value)) {
    return "-";
  }
  return String(Math.round(Number(value)));
}

function buildWsUrl(raw, token) {
  const fallback = new URL(window.location.href);
  fallback.protocol = fallback.protocol === "https:" ? "wss:" : "ws:";
  fallback.pathname = "/ws";
  fallback.search = "";
  fallback.hash = "";

  const url = new URL(raw || fallback.toString(), window.location.href);
  if (url.protocol === "http:") {
    url.protocol = "ws:";
  } else if (url.protocol === "https:") {
    url.protocol = "wss:";
  } else if (url.protocol !== "ws:" && url.protocol !== "wss:") {
    url.protocol = fallback.protocol;
  }

  if (!url.pathname || url.pathname === "/") {
    url.pathname = "/ws";
  }

  if (token) {
    url.searchParams.set("token", token);
  } else {
    url.searchParams.delete("token");
  }
  return url.toString();
}

function pickInitialWsUrl() {
  const queryWsRaw = new URLSearchParams(window.location.search).get("ws");
  const queryWs = typeof queryWsRaw === "string" ? queryWsRaw.trim() : "";
  if (!queryWs) {
    return DEFAULT_WS_URL;
  }

  try {
    const candidate = new URL(queryWs, window.location.href);
    const isLocalHost =
      candidate.hostname === "localhost" ||
      candidate.hostname === "127.0.0.1" ||
      candidate.hostname === "::1";
    const pageIsRemote =
      window.location.hostname !== "localhost" &&
      window.location.hostname !== "127.0.0.1" &&
      window.location.hostname !== "::1";

    // If the page is opened on a remote host, ignore stale ?ws=localhost links.
    if (isLocalHost && pageIsRemote) {
      return DEFAULT_WS_URL;
    }
  } catch {
    return DEFAULT_WS_URL;
  }

  return queryWs || DEFAULT_WS_URL;
}

function isTruthyQueryParam(value) {
  if (!value) {
    return false;
  }
  const normalized = String(value).trim().toLowerCase();
  return normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "on";
}

function logEvent(message) {
  appendLog(message);
}

function logGesture(kind, detail) {
  appendLog(`${kind}: ${detail}`);
}

function appendLog(message) {
  const row = document.createElement("div");
  row.className = "event-row";
  row.textContent = `${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}  ${message}`;
  elements.eventLog.prepend(row);
  while (elements.eventLog.childElementCount > 18) {
    elements.eventLog.lastElementChild?.remove();
  }
}
