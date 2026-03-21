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
  restorePreviousSession: document.getElementById("restorePreviousSession"),
  savedSessionStatus: document.getElementById("savedSessionStatus"),
  restoreSavedSessionButton: document.getElementById("restoreSavedSessionButton"),
  clearSavedSessionButton: document.getElementById("clearSavedSessionButton"),
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
  datasetBrowserSection: document.getElementById("datasetBrowserSection"),
  datasetOpenButton: document.getElementById("datasetOpenButton"),
  datasetActiveFile: document.getElementById("datasetActiveFile"),
  datasetCurrentPath: document.getElementById("datasetCurrentPath"),
  datasetBrowserStatus: document.getElementById("datasetBrowserStatus"),
  datasetBrowserModal: document.getElementById("datasetBrowserModal"),
  datasetBrowserModalBackdrop: document.getElementById("datasetBrowserModalBackdrop"),
  datasetBrowserCloseButton: document.getElementById("datasetBrowserCloseButton"),
  datasetRefreshButton: document.getElementById("datasetRefreshButton"),
  datasetSearchInput: document.getElementById("datasetSearchInput"),
  datasetBreadcrumb: document.getElementById("datasetBreadcrumb"),
  datasetBrowserList: document.getElementById("datasetBrowserList"),
  datasetDetailsEmpty: document.getElementById("datasetDetailsEmpty"),
  datasetDetailsPanel: document.getElementById("datasetDetailsPanel"),
  datasetDetailsName: document.getElementById("datasetDetailsName"),
  datasetDetailsPath: document.getElementById("datasetDetailsPath"),
  datasetDetailsSize: document.getElementById("datasetDetailsSize"),
  datasetDetailsModified: document.getElementById("datasetDetailsModified"),
  datasetDetailsSupported: document.getElementById("datasetDetailsSupported"),
  datasetDetailsHduCount: document.getElementById("datasetDetailsHduCount"),
  datasetHduSelectionSection: document.getElementById("datasetHduSelectionSection"),
  datasetHduSelect: document.getElementById("datasetHduSelect"),
  datasetHduSelectedSummarySection: document.getElementById("datasetHduSelectedSummarySection"),
  datasetHduSelectedTitle: document.getElementById("datasetHduSelectedTitle"),
  datasetHduSelectedMeta: document.getElementById("datasetHduSelectedMeta"),
  datasetDetailsHdus: document.getElementById("datasetDetailsHdus"),
  datasetDetailsHeader: document.getElementById("datasetDetailsHeader"),
  datasetOpenSelectedButton: document.getElementById("datasetOpenSelectedButton"),
  datasetCancelButton: document.getElementById("datasetCancelButton"),
  datasetLoadingModal: document.getElementById("datasetLoadingModal"),
  datasetLoadingFile: document.getElementById("datasetLoadingFile"),
  datasetLoadingStatus: document.getElementById("datasetLoadingStatus"),
  datasetLoadingSteps: document.getElementById("datasetLoadingSteps"),
  volumeRenderMode: document.getElementById("volumeRenderMode"),
  volumeOpacityScale: document.getElementById("volumeOpacityScale"),
  volumeOpacityScaleValue: document.getElementById("volumeOpacityScaleValue"),
  volumePalettePicker: document.getElementById("volumePalettePicker"),
  volumePaletteButton: document.getElementById("volumePaletteButton"),
  volumePaletteButtonName: document.getElementById("volumePaletteButtonName"),
  volumePaletteButtonBadges: document.getElementById("volumePaletteButtonBadges"),
  volumePaletteButtonSwatch: document.getElementById("volumePaletteButtonSwatch"),
  volumePaletteMenu: document.getElementById("volumePaletteMenu"),
  volumePaletteSearch: document.getElementById("volumePaletteSearch"),
  volumePaletteOptions: document.getElementById("volumePaletteOptions"),
  volumeScaleMode: document.getElementById("volumeScaleMode"),
  volumePalettePreview: document.getElementById("volumePalettePreview"),
  volumePalettePreviewCaption: document.getElementById("volumePalettePreviewCaption"),
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
    paletteCatalog: [],
    palettePreviewColors: [],
    paletteMenuOpen: false,
    paletteFilter: "",
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
  service: {
    backendVersion: "",
    frontendBuild: "",
  },
  datasets: {
    browserEnabled: false,
    currentPath: "",
    parentPath: null,
    activeDatasetPath: "",
    activeDatasetName: "",
    entries: [],
    loading: false,
    error: "",
    filter: "",
    modalOpen: false,
    selectedPath: "",
    selectedEntry: null,
    selectedHduIndex: null,
    details: null,
    detailsLoading: false,
    detailsError: "",
    loadingModalOpen: false,
    loadingStatus: "",
    loadingSteps: [],
    restoredMessage: "",
    restoredTone: "ok",
  },
  persistence: {
    storageKey: "visivo-connect.state.v1",
    preferenceKey: "visivo-connect.preferences.v1",
    restoreOnLoad: true,
    dirty: false,
    restored: false,
    saveTimer: 0,
    noticeTimer: 0,
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
    wsReconnectBaseDelayMs: 1000,
    wsReconnectMaxDelayMs: 15000,
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

function basenameFromPath(value) {
  if (typeof value !== "string" || !value.trim()) {
    return "";
  }
  const normalized = value.trim().split("#", 1)[0].replace(/\\/g, "/");
  const parts = normalized.split("/").filter(Boolean);
  return parts.length > 0 ? parts[parts.length - 1] : normalized || "";
}

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

function applyRuntimeConfig(config) {
  if (!config || typeof config !== "object") {
    return;
  }
  if (typeof config.backendVersion === "string") {
    state.service.backendVersion = config.backendVersion;
  }
  if (typeof config.frontendBuild === "string") {
    state.service.frontendBuild = config.frontendBuild;
  }
  if (typeof config.datasetBrowserEnabled === "boolean") {
    state.datasets.browserEnabled = config.datasetBrowserEnabled;
  }
  if (typeof config.defaultDatasetRelativePath === "string" && config.defaultDatasetRelativePath.trim()) {
    if (!state.datasets.activeDatasetPath) {
      state.datasets.activeDatasetPath = config.defaultDatasetRelativePath.trim();
      state.datasets.activeDatasetName = basenameFromPath(state.datasets.activeDatasetPath);
    }
  } else if (typeof config.defaultDatasetPath === "string" && config.defaultDatasetPath.trim() && !state.datasets.activeDatasetName) {
    state.datasets.activeDatasetName = basenameFromPath(config.defaultDatasetPath.trim());
  }
  if (typeof config.relayOnlyDefault === "boolean" && !state.rtc.forceRelayOnly) {
    state.rtc.forceRelayOnly = config.relayOnlyDefault;
  }
  const defaults = config.defaults && typeof config.defaults === "object" ? config.defaults : {};
  if (Number.isFinite(defaults.targetFps)) {
    state.renderParams.targetFps = Number(defaults.targetFps);
  }
  if (Number.isFinite(defaults.bitrateMbps)) {
    state.renderParams.bitrate = Number(defaults.bitrateMbps);
  }
  if (Number.isFinite(defaults.interactiveDownsample)) {
    state.quality.interactiveDownsample = Number(defaults.interactiveDownsample);
  }
  if (typeof defaults.hqDetailPreset === "string" && defaults.hqDetailPreset.trim()) {
    state.quality.hqDetailPreset = defaults.hqDetailPreset.trim();
  }
  if (Number.isFinite(defaults.wsReconnectBaseDelayMs)) {
    state.transport.wsReconnectBaseDelayMs = Number(defaults.wsReconnectBaseDelayMs);
  }
  if (Number.isFinite(defaults.wsReconnectMaxDelayMs)) {
    state.transport.wsReconnectMaxDelayMs = Number(defaults.wsReconnectMaxDelayMs);
  }
}

async function loadRuntimeConfig() {
  try {
    const response = await fetch("/api/runtime-config", { method: "GET", cache: "no-store" });
    if (!response.ok) {
      return;
    }
    const payload = await response.json();
    applyRuntimeConfig(payload);
    if (state.service.backendVersion || state.service.frontendBuild) {
      logEvent(
        `Build backend=${state.service.backendVersion || "unknown"} frontend=${state.service.frontendBuild || "unknown"}`
      );
    }
  } catch (error) {
    console.warn("Runtime config fetch failed", error);
  }
}

function datasetApiUrl(relativePath = "") {
  const url = new URL("/api/datasets", window.location.origin);
  if (relativePath) {
    url.searchParams.set("path", relativePath);
  }
  const token = elements.authToken.value.trim();
  if (token) {
    url.searchParams.set("token", token);
  }
  return url.toString();
}

function datasetDetailsApiUrl(relativePath = "") {
  const url = new URL("/api/datasets/details", window.location.origin);
  if (relativePath) {
    url.searchParams.set("path", relativePath);
  }
  const token = elements.authToken.value.trim();
  if (token) {
    url.searchParams.set("token", token);
  }
  return url.toString();
}

function formatBytes(value) {
  if (!Number.isFinite(value)) {
    return "-";
  }
  const bytes = Number(value);
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  if (bytes < 1024 ** 2) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }
  if (bytes < 1024 ** 3) {
    return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
  }
  return `${(bytes / 1024 ** 3).toFixed(2)} GB`;
}

function formatTimestamp(ms) {
  if (!Number.isFinite(ms)) {
    return "-";
  }
  return new Date(Number(ms)).toLocaleString();
}

function showDatasetRestoreNotice(message, tone = "ok", timeoutMs = 5000) {
  clearTimeout(state.persistence.noticeTimer);
  state.datasets.restoredMessage = typeof message === "string" ? message : "";
  state.datasets.restoredTone = tone === "danger" ? "danger" : tone === "warn" ? "warn" : "ok";
  renderDatasetBrowser();
  if (!state.datasets.restoredMessage || timeoutMs <= 0) {
    return;
  }
  state.persistence.noticeTimer = window.setTimeout(() => {
    state.datasets.restoredMessage = "";
    state.datasets.restoredTone = "ok";
    renderDatasetBrowser();
  }, timeoutMs);
}

function buildPersistencePreferencesSnapshot() {
  return {
    version: 1,
    restoreOnLoad: Boolean(state.persistence.restoreOnLoad),
  };
}

function persistPersistencePreferences() {
  try {
    window.localStorage.setItem(state.persistence.preferenceKey, JSON.stringify(buildPersistencePreferencesSnapshot()));
  } catch (error) {
    console.warn("Failed to persist VisIVO preferences", error);
  }
}

function restorePersistencePreferences() {
  try {
    const raw = window.localStorage.getItem(state.persistence.preferenceKey);
    if (!raw) {
      return;
    }
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === "object" && typeof parsed.restoreOnLoad === "boolean") {
      state.persistence.restoreOnLoad = parsed.restoreOnLoad;
    }
  } catch (error) {
    console.warn("Failed to restore VisIVO preferences", error);
  }
}

function buildPersistedStateSnapshot() {
  return {
    version: 1,
    savedAt: new Date().toISOString(),
    datasetPath: typeof state.datasets.activeDatasetPath === "string" ? state.datasets.activeDatasetPath : "",
    renderMode: state.renderMode,
    renderParams: {
      scale: state.renderParams.scale,
      bitrate: state.renderParams.bitrate,
      targetFps: state.renderParams.targetFps,
    },
    visualization: {
      mode: state.visualization.mode,
      isoValue: state.visualization.isoValue,
    },
    volume: {
      renderMode: state.volume.renderMode,
      palette: state.volume.palette,
      scaleMode: state.volume.scaleMode,
      opacityScale: state.volume.opacityScale,
      sampleDistanceScale: state.volume.sampleDistanceScale,
      sampleDistanceManual: state.volume.sampleDistanceManual,
      imageSampleDistance: state.volume.imageSampleDistance,
      imageSampleDistanceManual: state.volume.imageSampleDistanceManual,
      shade: state.volume.shade,
      sliceAxis: state.volume.sliceAxis,
      slicePosition: state.volume.slicePosition,
      cropping: {
        enabled: Boolean(state.volume.cropping?.enabled),
        bounds: Array.isArray(state.volume.cropping?.bounds) ? state.volume.cropping.bounds.slice(0, 6) : [0, 1, 0, 1, 0, 1],
      },
    },
    quality: {
      interactiveDownsample: state.quality.interactiveDownsample,
      hqDetailPreset: state.quality.hqDetailPreset,
    },
    ui: {
      activeTab: state.ui.activeTab,
    },
  };
}

function syncPersistencePreferenceUI() {
  if (elements.restorePreviousSession) {
    elements.restorePreviousSession.checked = Boolean(state.persistence.restoreOnLoad);
  }
  const snapshot = loadSavedSessionSnapshot();
  const hasSavedSnapshot = Boolean(snapshot);
  if (elements.savedSessionStatus) {
    elements.savedSessionStatus.textContent = hasSavedSnapshot
      ? `Saved session snapshot available${snapshot?.savedAt ? ` (${new Date(snapshot.savedAt).toLocaleString()})` : ""}.`
      : "No saved session snapshot.";
    elements.savedSessionStatus.dataset.tone = hasSavedSnapshot ? "ok" : "subtle";
  }
  if (elements.restoreSavedSessionButton) {
    elements.restoreSavedSessionButton.disabled = !hasSavedSnapshot;
  }
  if (elements.clearSavedSessionButton) {
    elements.clearSavedSessionButton.disabled = !hasSavedSnapshot;
  }
}

function loadSavedSessionSnapshot() {
  try {
    const raw = window.localStorage.getItem(state.persistence.storageKey);
    if (!raw) {
      return null;
    }
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch (error) {
    console.warn("Failed to read saved VisIVO state", error);
    return null;
  }
}

function persistAppStateNow() {
  clearTimeout(state.persistence.saveTimer);
  state.persistence.saveTimer = 0;
  try {
    window.localStorage.setItem(state.persistence.storageKey, JSON.stringify(buildPersistedStateSnapshot()));
    syncPersistencePreferenceUI();
  } catch (error) {
    console.warn("Failed to persist VisIVO state", error);
  }
}

function scheduleAppStatePersist() {
  clearTimeout(state.persistence.saveTimer);
  state.persistence.saveTimer = window.setTimeout(() => {
    persistAppStateNow();
  }, 150);
}

function markMeaningfulSessionDirty({ persist = true } = {}) {
  state.persistence.dirty = true;
  if (persist) {
    scheduleAppStatePersist();
  }
}

function applyPersistedStateSnapshot(snapshot) {
  if (!snapshot || typeof snapshot !== "object") {
    return false;
  }
  if (typeof snapshot.datasetPath === "string" && snapshot.datasetPath.trim()) {
    state.datasets.activeDatasetPath = snapshot.datasetPath.trim();
    state.datasets.activeDatasetName = basenameFromPath(state.datasets.activeDatasetPath);
  }
  if (typeof snapshot.renderMode === "string" && (snapshot.renderMode === "interactive" || snapshot.renderMode === "high-quality")) {
    state.renderMode = snapshot.renderMode;
  }
  if (snapshot.renderParams && typeof snapshot.renderParams === "object") {
    state.renderParams.scale = clampFloat(Number(snapshot.renderParams.scale), 0.4, 2.0, state.renderParams.scale);
    state.renderParams.bitrate = clampFloat(Number(snapshot.renderParams.bitrate), 1.0, 100.0, state.renderParams.bitrate);
    state.renderParams.targetFps = clampFloat(Number(snapshot.renderParams.targetFps), 5.0, 60.0, state.renderParams.targetFps);
  }
  if (snapshot.visualization && typeof snapshot.visualization === "object") {
    if (typeof snapshot.visualization.mode === "string" && ["volume", "isosurface"].includes(snapshot.visualization.mode)) {
      state.visualization.mode = snapshot.visualization.mode;
    }
    if (Number.isFinite(snapshot.visualization.isoValue)) {
      state.visualization.isoValue = Number(snapshot.visualization.isoValue);
    }
  }
  if (snapshot.volume && typeof snapshot.volume === "object") {
    if (typeof snapshot.volume.renderMode === "string" && ["composite", "mip", "slice"].includes(snapshot.volume.renderMode)) {
      state.volume.renderMode = snapshot.volume.renderMode;
    }
    if (typeof snapshot.volume.palette === "string" && snapshot.volume.palette.trim()) {
      state.volume.palette = snapshot.volume.palette.trim();
    }
    if (typeof snapshot.volume.scaleMode === "string") {
      state.volume.scaleMode = snapshot.volume.scaleMode.toLowerCase().startsWith("log") ? "log" : "linear";
    }
    if (Number.isFinite(snapshot.volume.opacityScale)) {
      state.volume.opacityScale = clampFloat(Number(snapshot.volume.opacityScale), 0.1, 4.0, state.volume.opacityScale);
    }
    if (typeof snapshot.volume.sampleDistanceManual === "boolean") {
      state.volume.sampleDistanceManual = snapshot.volume.sampleDistanceManual;
    }
    if (state.volume.sampleDistanceManual && Number.isFinite(snapshot.volume.sampleDistanceScale)) {
      state.volume.sampleDistanceScale = clampFloat(Number(snapshot.volume.sampleDistanceScale), 0.2, 6.0, state.volume.sampleDistanceScale ?? 1.0);
    }
    if (typeof snapshot.volume.imageSampleDistanceManual === "boolean") {
      state.volume.imageSampleDistanceManual = snapshot.volume.imageSampleDistanceManual;
    }
    if (state.volume.imageSampleDistanceManual && Number.isFinite(snapshot.volume.imageSampleDistance)) {
      state.volume.imageSampleDistance = clampFloat(Number(snapshot.volume.imageSampleDistance), 1.0, 4.0, state.volume.imageSampleDistance ?? 1.0);
    }
    if (typeof snapshot.volume.shade === "boolean") {
      state.volume.shade = snapshot.volume.shade;
    }
    if (typeof snapshot.volume.sliceAxis === "string" && ["x", "y", "z"].includes(snapshot.volume.sliceAxis)) {
      state.volume.sliceAxis = snapshot.volume.sliceAxis;
    }
    if (Number.isFinite(snapshot.volume.slicePosition)) {
      state.volume.slicePosition = clampFloat(Number(snapshot.volume.slicePosition), 0.0, 1.0, state.volume.slicePosition);
    }
    if (snapshot.volume.cropping && typeof snapshot.volume.cropping === "object") {
      state.volume.cropping.enabled = Boolean(snapshot.volume.cropping.enabled);
      if (Array.isArray(snapshot.volume.cropping.bounds) && snapshot.volume.cropping.bounds.length === 6) {
        state.volume.cropping.bounds = snapshot.volume.cropping.bounds.map((value, index) => {
          const fallback = state.volume.cropping.bounds[index] ?? 0;
          return clampFloat(Number(value), 0.0, 1.0, fallback);
        });
      }
    }
  }
  if (snapshot.quality && typeof snapshot.quality === "object") {
    if (Number.isFinite(snapshot.quality.interactiveDownsample)) {
      state.quality.interactiveDownsample = clampFloat(Number(snapshot.quality.interactiveDownsample), 1.0, 4.0, state.quality.interactiveDownsample);
    }
    if (typeof snapshot.quality.hqDetailPreset === "string" && HQ_DETAIL_PRESETS[snapshot.quality.hqDetailPreset]) {
      state.quality.hqDetailPreset = snapshot.quality.hqDetailPreset;
    }
  }
  if (snapshot.ui && typeof snapshot.ui === "object" && typeof snapshot.ui.activeTab === "string") {
    state.ui.activeTab = snapshot.ui.activeTab;
  }
  return true;
}

function restorePersistedAppState() {
  try {
    const parsed = loadSavedSessionSnapshot();
    if (!parsed) {
      return false;
    }
    const restored = applyPersistedStateSnapshot(parsed);
    if (restored) {
      state.persistence.restored = true;
      showDatasetRestoreNotice("Previous session settings restored", "ok");
      logEvent("Previous session settings restored");
      return true;
    }
  } catch (error) {
    console.warn("Failed to restore VisIVO state", error);
  }
  return false;
}

function restoreSavedSessionNow() {
  const previousDatasetPath = state.datasets.activeDatasetPath;
  const restored = restorePersistedAppState();
  if (!restored) {
    showDatasetRestoreNotice("No saved session snapshot available", "warn", 5000);
    logEvent("No saved session snapshot available");
    syncPersistencePreferenceUI();
    return false;
  }
  syncRuntimeDefaultsToUI();
  syncVolumeControlsToUI();
  renderDatasetBrowser();
  if (typeof setActiveControlTab === "function") {
    setActiveControlTab(state.ui.activeTab || "session");
  }
  if (state.ws && state.ws.readyState === WebSocket.OPEN) {
    if (state.datasets.activeDatasetPath && state.datasets.activeDatasetPath !== previousDatasetPath) {
      send({ type: "dataset.select", sessionId: state.sessionId, path: state.datasets.activeDatasetPath });
    }
    setMode(state.renderMode, true);
    sendRenderParams();
  }
  return true;
}

function clearSavedSessionSnapshot() {
  try {
    window.localStorage.removeItem(state.persistence.storageKey);
    state.persistence.restored = false;
    showDatasetRestoreNotice("Saved session snapshot cleared", "ok", 4000);
    logEvent("Saved session snapshot cleared");
  } catch (error) {
    console.warn("Failed to clear saved VisIVO state", error);
    showDatasetRestoreNotice("Failed to clear saved session snapshot", "danger", 6000);
    logEvent("Failed to clear saved session snapshot");
  } finally {
    syncPersistencePreferenceUI();
  }
}

function hasMeaningfulPersistedState() {
  return Boolean(
    state.datasets.activeDatasetPath
    || state.visualization.mode !== "volume"
    || Math.abs(Number(state.visualization.isoValue) || 0) > 1e-6
    || state.volume.renderMode !== "composite"
    || state.volume.palette !== "Inferno"
    || state.volume.scaleMode !== "linear"
    || Math.abs((Number(state.volume.opacityScale) || 0) - 1.8) > 1e-6
    || state.volume.sampleDistanceManual
    || state.volume.imageSampleDistanceManual
    || state.volume.shade !== true
    || state.volume.sliceAxis !== "z"
    || Math.abs((Number(state.volume.slicePosition) || 0) - 0.5) > 1e-6
    || Boolean(state.volume.cropping?.enabled)
    || Math.abs((Number(state.renderParams.scale) || 0) - 1.0) > 1e-6
    || Math.abs((Number(state.renderParams.bitrate) || 0) - 14.0) > 1e-6
    || Math.abs((Number(state.renderParams.targetFps) || 0) - 30.0) > 1e-6
    || Math.abs((Number(state.quality.interactiveDownsample) || 0) - 1.6) > 1e-6
    || state.quality.hqDetailPreset !== "sharp"
  );
}

function shouldWarnOnUnload() {
  const hasLiveSession = Boolean(
    (state.ws && state.ws.readyState === WebSocket.OPEN)
    || (state.pc && state.connectionState !== "disconnected")
    || state.transport.wsFallbackActive
  );
  return Boolean(
    (hasLiveSession && hasMeaningfulPersistedState())
    || (state.persistence.dirty && hasMeaningfulPersistedState())
  );
}

function resetDatasetDetails() {
  state.datasets.selectedEntry = null;
  state.datasets.selectedPath = "";
  state.datasets.selectedHduIndex = null;
  state.datasets.details = null;
  state.datasets.detailsLoading = false;
  state.datasets.detailsError = "";
}

function openDatasetBrowserModal() {
  if (!state.datasets.browserEnabled) {
    return;
  }
  state.datasets.modalOpen = true;
  elements.datasetBrowserModal.classList.remove("hidden");
  elements.datasetBrowserModal.setAttribute("aria-hidden", "false");
  elements.datasetSearchInput.value = "";
  state.datasets.filter = "";
  renderDatasetBrowser();
  window.setTimeout(() => elements.datasetSearchInput?.focus(), 0);
}

function closeDatasetBrowserModal() {
  state.datasets.modalOpen = false;
  elements.datasetBrowserModal.classList.add("hidden");
  elements.datasetBrowserModal.setAttribute("aria-hidden", "true");
  elements.datasetSearchInput.value = "";
  state.datasets.filter = "";
  resetDatasetDetails();
  renderDatasetBrowser();
}

function openDatasetLoadingModal(datasetName) {
  state.datasets.loadingModalOpen = true;
  state.datasets.loadingStatus = "Opening FITS";
  state.datasets.loadingSteps = [
    { key: "opening-fits", label: "Opening FITS", state: "active" },
    { key: "reading-hdu", label: "Reading HDU", state: "pending" },
    { key: "sanitizing-data", label: "Sanitizing data", state: "pending" },
    { key: "building-vtk", label: "Building vtkImageData", state: "pending" },
    { key: "initializing-renderer", label: "Initializing renderer", state: "pending" },
    { key: "warming-up", label: "Warming up first frame", state: "pending" },
    { key: "complete", label: "Dataset ready", state: "pending" },
  ];
  elements.datasetLoadingFile.textContent = datasetName || "-";
  elements.datasetLoadingModal.classList.remove("hidden");
  elements.datasetLoadingModal.setAttribute("aria-hidden", "false");
  renderDatasetLoading();
}

function closeDatasetLoadingModal() {
  state.datasets.loadingModalOpen = false;
  elements.datasetLoadingModal.classList.add("hidden");
  elements.datasetLoadingModal.setAttribute("aria-hidden", "true");
}

function updateDatasetLoadingPhase(phase, label, importMetrics) {
  const phaseToStepKeys = {
    "opening-fits": ["opening-fits"],
    "initializing-renderer": ["opening-fits", "reading-hdu", "sanitizing-data", "building-vtk", "initializing-renderer"],
    "warming-up": ["opening-fits", "reading-hdu", "sanitizing-data", "building-vtk", "initializing-renderer", "warming-up"],
    "complete": ["opening-fits", "reading-hdu", "sanitizing-data", "building-vtk", "initializing-renderer", "warming-up", "complete"],
  };
  const doneKeys = phaseToStepKeys[phase] || [];
  state.datasets.loadingStatus = label || state.datasets.loadingStatus || "Loading dataset";
  state.datasets.loadingSteps = state.datasets.loadingSteps.map((step) => {
    if (phase === "complete") {
      return { ...step, state: "done" };
    }
    if (doneKeys.includes(step.key)) {
      return { ...step, state: step.key === phase ? "active" : "done" };
    }
    return { ...step, state: "pending" };
  });
  if (importMetrics && typeof importMetrics === "object") {
    const timedKeys = {
      "opening-fits": importMetrics.fitsOpenMs,
      "reading-hdu": importMetrics.hduSelectMs,
      "sanitizing-data": importMetrics.sanitizeConvertMs,
      "building-vtk": importMetrics.vtkBuildMs,
    };
    state.datasets.loadingSteps = state.datasets.loadingSteps.map((step) => (
      Number.isFinite(timedKeys[step.key])
        ? { ...step, detail: formatMs(timedKeys[step.key]) }
        : step
    ));
  }
  renderDatasetLoading();
}

function renderDatasetLoading() {
  if (!state.datasets.loadingModalOpen) {
    return;
  }
  elements.datasetLoadingStatus.textContent = state.datasets.loadingStatus || "Loading dataset";
  elements.datasetLoadingSteps.replaceChildren();
  for (const step of state.datasets.loadingSteps) {
    const row = document.createElement("div");
    row.className = "dataset-loading-step";
    row.dataset.state = step.state || "pending";
    const indicator = document.createElement("span");
    indicator.className = "dataset-loading-step-indicator";
    const text = document.createElement("span");
    text.textContent = step.detail ? `${step.label} · ${step.detail}` : step.label;
    row.append(indicator, text);
    elements.datasetLoadingSteps.appendChild(row);
  }
}

function filteredDatasetEntries() {
  const filter = (state.datasets.filter || "").trim().toLowerCase();
  if (!filter) {
    return state.datasets.entries;
  }
  return state.datasets.entries.filter((entry) => String(entry.name || entry.path || "").toLowerCase().includes(filter));
}

function renderDatasetBreadcrumb() {
  elements.datasetBreadcrumb.replaceChildren();
  const parts = state.datasets.currentPath ? state.datasets.currentPath.split("/") : [];
  const makeButton = (label, path) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "dataset-breadcrumb-button";
    button.textContent = label;
    button.addEventListener("click", () => {
      fetchDatasetBrowser(path, { force: true });
    });
    elements.datasetBreadcrumb.appendChild(button);
  };
  makeButton("Root", "");
  let prefix = "";
  for (const part of parts) {
    const sep = document.createElement("span");
    sep.className = "dataset-breadcrumb-sep";
    sep.textContent = "/";
    elements.datasetBreadcrumb.appendChild(sep);
    prefix = prefix ? `${prefix}/${part}` : part;
    makeButton(part, prefix);
  }
}

function formatDatasetHduTitle(hdu) {
  if (!hdu) {
    return "-";
  }
  const name = typeof hdu.name === "string" && hdu.name.trim() ? ` · ${hdu.name.trim()}` : "";
  return `${formatInteger(hdu.index)}${name}`;
}

function formatDatasetHduMeta(hdu) {
  if (!hdu) {
    return "-";
  }
  return [
    hdu.className || null,
    Array.isArray(hdu.shape) ? hdu.shape.join("×") : null,
    hdu.dtype || null,
    Number.isFinite(hdu.ndim) ? `${formatInteger(hdu.ndim)}D` : null,
    hdu.isSelectable === false ? "not renderable" : null,
  ].filter(Boolean).join(" · ");
}

function selectedDatasetHdu(details = state.datasets.details) {
  if (!details?.fits || !Array.isArray(details.fits.hdus)) {
    return null;
  }
  const selected = details.fits.hdus.find((hdu) => hdu.index === state.datasets.selectedHduIndex);
  if (selected) {
    return selected;
  }
  return details.fits.hdus.find((hdu) => hdu.isDefault) || details.fits.hdus.find((hdu) => hdu.isSelectable) || details.fits.hdus[0] || null;
}

function selectedDatasetPathWithHdu() {
  const relativePath = state.datasets.selectedPath;
  if (typeof relativePath !== "string" || !relativePath.trim()) {
    return "";
  }
  const selectedHdu = selectedDatasetHdu();
  if (selectedHdu && Number.isFinite(selectedHdu.index)) {
    return `${relativePath.trim()}#hdu=${selectedHdu.index}`;
  }
  return relativePath.trim();
}

function renderDatasetDetails() {
  const details = state.datasets.details;
  const showDetails = Boolean(details);
  elements.datasetDetailsEmpty.classList.toggle("hidden", showDetails);
  elements.datasetDetailsPanel.classList.toggle("hidden", !showDetails);
  const selectedHdu = selectedDatasetHdu(details);
  const selectableHduCount = Number(details?.fits?.selectableHduCount || 0);
  elements.datasetOpenSelectedButton.disabled = !state.datasets.selectedPath || state.datasets.detailsLoading || !showDetails || details?.supported === false || (Boolean(details?.fits) && !selectedHdu);
  if (!showDetails) {
    if (state.datasets.detailsError) {
      elements.datasetDetailsEmpty.textContent = state.datasets.detailsError;
    } else if (state.datasets.detailsLoading) {
      elements.datasetDetailsEmpty.textContent = "Loading file details...";
    } else {
      elements.datasetDetailsEmpty.textContent = "Select a FITS file to inspect its details.";
    }
    return;
  }
  elements.datasetDetailsName.textContent = details.name || "-";
  elements.datasetDetailsPath.textContent = details.path || "-";
  elements.datasetDetailsSize.textContent = formatBytes(details.sizeBytes);
  elements.datasetDetailsModified.textContent = formatTimestamp(details.modifiedMs);
  elements.datasetDetailsSupported.textContent = details.supported ? "yes" : "no";
  elements.datasetDetailsHduCount.textContent = formatInteger(details.fits?.hduCount);
  elements.datasetHduSelectionSection.classList.toggle("hidden", !(selectableHduCount > 1));
  elements.datasetHduSelectedSummarySection.classList.toggle("hidden", !(details.fits && selectableHduCount <= 1 && selectedHdu));
  elements.datasetHduSelect.replaceChildren();
  for (const hdu of details.fits?.hdus || []) {
    if (!hdu.isSelectable) {
      continue;
    }
    const option = document.createElement("option");
    option.value = String(hdu.index);
    option.textContent = `${formatDatasetHduTitle(hdu)}${formatDatasetHduMeta(hdu) ? ` — ${formatDatasetHduMeta(hdu)}` : ""}`;
    option.selected = Boolean(selectedHdu && hdu.index === selectedHdu.index);
    elements.datasetHduSelect.appendChild(option);
  }
  elements.datasetHduSelectedTitle.textContent = formatDatasetHduTitle(selectedHdu);
  elements.datasetHduSelectedMeta.textContent = formatDatasetHduMeta(selectedHdu);
  elements.datasetDetailsHdus.replaceChildren();
  for (const hdu of details.fits?.hdus || []) {
    const item = document.createElement("div");
    item.className = `dataset-details-item${selectedHdu && hdu.index === selectedHdu.index ? " dataset-details-item-active" : ""}${hdu.isSelectable ? "" : " dataset-details-item-disabled"}`;
    if (hdu.isSelectable) {
      item.setAttribute("role", "button");
      item.tabIndex = 0;
      item.addEventListener("click", () => {
        state.datasets.selectedHduIndex = hdu.index;
        renderDatasetBrowser();
      });
      item.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          state.datasets.selectedHduIndex = hdu.index;
          renderDatasetBrowser();
        }
      });
    }
    const title = document.createElement("div");
    title.className = "dataset-details-item-title";
    title.textContent = formatDatasetHduTitle(hdu);
    const meta = document.createElement("div");
    meta.className = "dataset-details-item-meta";
    meta.textContent = formatDatasetHduMeta(hdu);
    item.append(title, meta);
    elements.datasetDetailsHdus.appendChild(item);
  }
  elements.datasetDetailsHeader.replaceChildren();
  const headerSource = selectedHdu?.headerPreview && Object.keys(selectedHdu.headerPreview).length > 0
    ? selectedHdu.headerPreview
    : (details.fits?.headerPreview || {});
  for (const [key, value] of Object.entries(headerSource)) {
    const item = document.createElement("div");
    item.className = "dataset-details-item";
    const title = document.createElement("div");
    title.className = "dataset-details-item-title";
    title.textContent = key;
    const meta = document.createElement("div");
    meta.className = "dataset-details-item-meta";
    meta.textContent = String(value);
    item.append(title, meta);
    elements.datasetDetailsHeader.appendChild(item);
  }
}

function renderDatasetBrowser() {
  if (!elements.datasetBrowserSection) {
    return;
  }
  elements.datasetBrowserSection.classList.toggle("hidden", false);
  elements.datasetOpenButton.disabled = !state.datasets.browserEnabled;
  elements.datasetActiveFile.textContent = state.datasets.activeDatasetName || basenameFromPath(state.datasets.activeDatasetPath) || "-";
  elements.datasetCurrentPath.textContent = state.datasets.browserEnabled
    ? (state.datasets.activeDatasetPath ? `/${state.datasets.activeDatasetPath}` : "No dataset selected")
    : "Browser unavailable.";
  const summaryStatus = state.datasets.restoredMessage
    || (!state.datasets.browserEnabled
      ? "Configure VISIVO_DATASET_ROOT to enable the dataset browser."
      : (state.datasets.error || "Open the dataset browser to browse and inspect FITS files."));
  elements.datasetBrowserStatus.textContent = summaryStatus;
  elements.datasetBrowserStatus.dataset.tone = state.datasets.restoredMessage
    ? state.datasets.restoredTone
    : (state.datasets.error ? "danger" : "subtle");

  if (!state.datasets.modalOpen) {
    return;
  }

  elements.datasetRefreshButton.disabled = state.datasets.loading;
  renderDatasetBreadcrumb();
  elements.datasetBrowserStatus.textContent = state.datasets.error
    || (state.datasets.loading ? "Loading datasets..." : "Browse folders and select a FITS file to inspect.");
  elements.datasetBrowserStatus.dataset.tone = state.datasets.error ? "danger" : state.datasets.loading ? "subtle" : "ok";
  elements.datasetBrowserList.replaceChildren();

  const addEntryButton = (entry, extraText = "") => {
    const button = document.createElement("button");
    button.type = "button";
    const isActive = entry.type === "file" && entry.active === true;
    const isSelected = entry.type === "file" && entry.path === state.datasets.selectedPath;
    button.className = `dataset-entry ${entry.type === "directory" ? "dataset-entry-directory" : "dataset-entry-file"}${isActive ? " dataset-entry-active" : ""}${isSelected ? " toggle active" : ""}`;
    button.addEventListener("click", () => {
      if (entry.type === "directory") {
        fetchDatasetBrowser(entry.path, { force: true });
        return;
      }
      selectDatasetEntry(entry);
    });
    if (entry.type === "file") {
      button.addEventListener("dblclick", () => {
        selectDatasetEntry(entry);
        confirmDatasetSelection();
      });
    }
    const title = document.createElement("span");
    title.className = "dataset-entry-name";
    title.textContent = entry.name || entry.path || "?";
    const meta = document.createElement("span");
    meta.className = "dataset-entry-meta";
    meta.textContent = extraText;
    button.append(title, meta);
    elements.datasetBrowserList.appendChild(button);
  };

  if (state.datasets.parentPath !== null) {
    addEntryButton({ type: "directory", path: state.datasets.parentPath, name: ".." }, "Up");
  }

  const entries = filteredDatasetEntries();
  for (const entry of entries) {
    const meta = entry.type === "directory"
      ? "Folder"
      : entry.active === true
        ? "Active dataset"
        : formatBytes(entry.sizeBytes);
    addEntryButton(entry, meta);
  }

  if (elements.datasetBrowserList.childElementCount === 0) {
    const empty = document.createElement("div");
    empty.className = "dataset-browser-empty";
    empty.textContent = state.datasets.loading ? "Loading..." : "No matching datasets in this folder.";
    elements.datasetBrowserList.appendChild(empty);
  }

  renderDatasetDetails();
}

async function fetchDatasetBrowser(relativePath = "", { force = false } = {}) {
  if (!state.datasets.browserEnabled) {
    renderDatasetBrowser();
    return;
  }
  if (state.datasets.loading && !force) {
    return;
  }
  state.datasets.loading = true;
  state.datasets.error = "";
  renderDatasetBrowser();
  try {
    const response = await fetch(datasetApiUrl(relativePath), { method: "GET", cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload?.message || "Could not load datasets");
    }
    state.datasets.currentPath = typeof payload.currentPath === "string" ? payload.currentPath : "";
    state.datasets.parentPath = typeof payload.parentPath === "string" ? payload.parentPath : payload.parentPath === "" ? "" : null;
    state.datasets.entries = Array.isArray(payload.entries) ? payload.entries : [];
    if (typeof payload.activeDatasetPath === "string" && payload.activeDatasetPath.trim()) {
      state.datasets.activeDatasetPath = payload.activeDatasetPath.trim();
      state.datasets.activeDatasetName = basenameFromPath(state.datasets.activeDatasetPath);
    }
  } catch (error) {
    state.datasets.error = error?.message || "Could not load datasets";
  } finally {
    state.datasets.loading = false;
    renderDatasetBrowser();
  }
}

async function fetchDatasetDetails(relativePath) {
  if (!relativePath) {
    return;
  }
  state.datasets.detailsLoading = true;
  state.datasets.detailsError = "";
  state.datasets.details = null;
  renderDatasetBrowser();
  try {
    const response = await fetch(datasetDetailsApiUrl(relativePath), { method: "GET", cache: "no-store" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload?.message || "Could not load file details");
    }
    state.datasets.details = payload;
    state.datasets.selectedHduIndex = Number.isFinite(payload?.fits?.defaultHduIndex)
      ? payload.fits.defaultHduIndex
      : ((payload?.fits?.hdus || []).find((hdu) => hdu.isSelectable)?.index ?? null);
  } catch (error) {
    state.datasets.detailsError = error?.message || "Could not load file details";
    state.datasets.selectedHduIndex = null;
  } finally {
    state.datasets.detailsLoading = false;
    renderDatasetBrowser();
  }
}

function selectDatasetEntry(entry) {
  if (!entry || entry.type !== "file") {
    return;
  }
  state.datasets.selectedEntry = entry;
  state.datasets.selectedPath = entry.path;
  state.datasets.selectedHduIndex = null;
  fetchDatasetDetails(entry.path);
}

function confirmDatasetSelection() {
  const relativePath = selectedDatasetPathWithHdu();
  if (typeof relativePath !== "string" || !relativePath.trim()) {
    return;
  }
  state.datasets.activeDatasetPath = relativePath.trim();
  state.datasets.activeDatasetName = basenameFromPath(state.datasets.activeDatasetPath);
  markMeaningfulSessionDirty();
  closeDatasetBrowserModal();
  openDatasetLoadingModal(state.datasets.activeDatasetPath);
  if (!send({ type: "dataset.select", sessionId: state.sessionId, path: state.datasets.activeDatasetPath })) {
    closeDatasetLoadingModal();
    logEvent(`Dataset selected for next connect: ${state.datasets.activeDatasetName}`);
  } else {
    logEvent(`Dataset requested: ${state.datasets.activeDatasetName}`);
  }
  renderDatasetBrowser();
}

function syncRuntimeDefaultsToUI() {
  elements.bitrate.value = String(state.renderParams.bitrate);
  elements.bitrateValue.textContent = formatBitrate(state.renderParams.bitrate);
  elements.targetFps.value = String(state.renderParams.targetFps);
  elements.targetFpsValue.textContent = formatFps(state.renderParams.targetFps);
  elements.interactiveDownsample.value = String(state.quality.interactiveDownsample);
  elements.interactiveDownsampleValue.textContent = `${state.quality.interactiveDownsample.toFixed(1)}x`;
  elements.hqDetailPreset.value = state.quality.hqDetailPreset;
}

elements.sessionId.textContent = state.sessionId;
syncPersistencePreferenceUI();
elements.renderScaleValue.textContent = formatScale(state.renderParams.scale);
elements.bitrateValue.textContent = formatBitrate(state.renderParams.bitrate);
elements.targetFpsValue.textContent = formatFps(state.renderParams.targetFps);
elements.interactiveDownsampleValue.textContent = `${state.quality.interactiveDownsample.toFixed(1)}x`;
elements.hqDetailPreset.value = state.quality.hqDetailPreset;
elements.visualizationMode.value = state.visualization.mode;
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

elements.datasetOpenButton?.addEventListener("click", () => {
  openDatasetBrowserModal();
});

elements.datasetBrowserCloseButton?.addEventListener("click", () => {
  closeDatasetBrowserModal();
});

elements.datasetCancelButton?.addEventListener("click", () => {
  closeDatasetBrowserModal();
});

elements.datasetBrowserModalBackdrop?.addEventListener("click", () => {
  closeDatasetBrowserModal();
});

elements.datasetOpenSelectedButton?.addEventListener("click", () => {
  confirmDatasetSelection();
});

elements.datasetHduSelect?.addEventListener("change", () => {
  const nextValue = Number(elements.datasetHduSelect.value);
  state.datasets.selectedHduIndex = Number.isFinite(nextValue) ? nextValue : null;
  renderDatasetBrowser();
});

elements.authToken?.addEventListener("change", () => {
  fetchDatasetBrowser(state.datasets.currentPath, { force: true });
});

elements.restorePreviousSession?.addEventListener("change", () => {
  state.persistence.restoreOnLoad = Boolean(elements.restorePreviousSession.checked);
  persistPersistencePreferences();
  syncPersistencePreferenceUI();
  logEvent(`Session restore on load ${state.persistence.restoreOnLoad ? "enabled" : "disabled"}`);
});

elements.restoreSavedSessionButton?.addEventListener("click", () => {
  const restored = restoreSavedSessionNow();
  if (restored) {
    logEvent("Saved session snapshot restored manually");
  }
});

elements.clearSavedSessionButton?.addEventListener("click", () => {
  clearSavedSessionSnapshot();
});

elements.datasetRefreshButton?.addEventListener("click", () => {
  fetchDatasetBrowser(state.datasets.currentPath, { force: true });
});

elements.datasetSearchInput?.addEventListener("input", () => {
  state.datasets.filter = (elements.datasetSearchInput.value || "").trim().toLowerCase();
  renderDatasetBrowser();
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

elements.volumePaletteButton.addEventListener("click", () => {
  setPaletteMenuOpen(!state.volume.paletteMenuOpen);
});

elements.volumePaletteSearch.addEventListener("input", () => {
  state.volume.paletteFilter = (elements.volumePaletteSearch.value || "").trim().toLowerCase();
  renderPaletteMenu();
});

elements.volumeScaleMode.addEventListener("change", () => {
  state.volume.scaleMode = elements.volumeScaleMode.value === "log" ? "log" : "linear";
  syncPalettePreview();
  sendRenderParams();
});

document.addEventListener("click", (event) => {
  if (!state.volume.paletteMenuOpen) {
    return;
  }
  if (!elements.volumePalettePicker.contains(event.target)) {
    closePaletteMenu();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && state.volume.paletteMenuOpen) {
    closePaletteMenu({ restoreFocus: true });
    return;
  }
  if (event.key === "Escape" && state.datasets.modalOpen) {
    closeDatasetBrowserModal();
  }
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
window.addEventListener("online", () => {
  if (state.shouldReconnect && !state.ws && state.wsUrl) {
    logEvent("Network online, reconnecting");
    openSocket();
  }
});
window.addEventListener("beforeunload", (event) => {
  persistAppStateNow();
  if (!shouldWarnOnUnload()) {
    return;
  }
  event.preventDefault();
  event.returnValue = "Refreshing now may discard the current VisIVO session state.";
});

const resizeObserver = new ResizeObserver(() => reportResize());
resizeObserver.observe(elements.stageFrame);

installGestureHandlers(elements.gestureLayer);

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
      datasetPath: state.datasets.activeDatasetPath || undefined,
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
  if (manual) {
    state.persistence.dirty = false;
    persistAppStateNow();
  }
  elements.disconnectButton.disabled = true;
  elements.connectButton.disabled = false;
  setConnectionState(manual ? "idle" : "reconnecting", manual ? "subtle" : "warn");
}

function scheduleReconnect() {
  const delay = Math.min(
    state.transport.wsReconnectBaseDelayMs * 2 ** Math.min(state.reconnectAttempts, 5),
    state.transport.wsReconnectMaxDelayMs
  );
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
  setConnectionState("error", "danger", "Socket error");
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
      if (typeof message.datasetRelativePath === "string" && message.datasetRelativePath.trim()) {
        state.datasets.activeDatasetPath = message.datasetRelativePath.trim();
      }
      if (typeof message.datasetName === "string" && message.datasetName.trim()) {
        state.datasets.activeDatasetName = message.datasetName.trim();
      }
      renderDatasetBrowser();
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
        if (message.rendererDiagnostics && typeof message.rendererDiagnostics === "object") {
          mergePaletteCatalog(message.rendererDiagnostics.paletteCatalog);
        }
        syncVolumeControlsToUI();
      }
      if (message.text) {
        logEvent(message.text);
      }
      break;
    case "stream-ready":
      logEvent("VisIVO Connect stream ready");
      break;
    case "dataset.loading":
      if (message.datasetName) {
        elements.datasetLoadingFile.textContent = message.datasetName;
      }
      updateDatasetLoadingPhase(message.phase, message.label, message.importMetrics);
      if (message.done) {
        window.setTimeout(() => {
          closeDatasetLoadingModal();
          fetchDatasetBrowser(state.datasets.currentPath, { force: true });
        }, 250);
      }
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
      if (message.phase === "dataset-switch") {
        closeDatasetLoadingModal();
      }
      if (
        state.persistence.restored
        && message.phase
        && ["dataset-switch", "hello", "session-init"].includes(message.phase)
        && typeof message.code === "string"
        && message.code.startsWith("dataset-")
      ) {
        showDatasetRestoreNotice("Saved dataset settings could not be reopened automatically", "danger", 7000);
      }
      logEvent(
        `Server error${message.code ? ` [${message.code}]` : ""}${message.phase ? ` phase=${message.phase}` : ""}${message.retryable ? " retryable" : ""}`
      );
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
  markMeaningfulSessionDirty();
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
    markMeaningfulSessionDirty();
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
  state.persistence.dirty = true;
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
  state.volume.palette = selected;
  renderPaletteMenu();
}

function palettePreviewColorsFor(name) {
  if (!name) {
    return [];
  }
  if (name === state.volume.palette && Array.isArray(state.volume.palettePreviewColors) && state.volume.palettePreviewColors.length > 0) {
    return state.volume.palettePreviewColors;
  }
  const catalogEntry = paletteCatalogEntry(name);
  return catalogEntry && Array.isArray(catalogEntry.previewColors) ? catalogEntry.previewColors : [];
}

function paletteGradient(colors) {
  return colors.length > 0
    ? `linear-gradient(90deg, ${colors.join(", ")})`
    : "linear-gradient(90deg, rgba(0, 0, 0, 0.35), rgba(255, 255, 255, 0.35))";
}

function paletteCatalogEntry(name) {
  return Array.isArray(state.volume.paletteCatalog)
    ? state.volume.paletteCatalog.find((entry) => entry.name === name) || null
    : null;
}

function paletteMetadataFor(name) {
  const entry = paletteCatalogEntry(name);
  return {
    hasAlpha: Boolean(entry?.hasAlpha),
    isDiscrete: Boolean(entry?.isDiscrete),
  };
}

function buildPaletteBadgeElements(name) {
  const metadata = paletteMetadataFor(name);
  const badges = [];
  if (metadata.hasAlpha) {
    const rgbaBadge = document.createElement("span");
    rgbaBadge.className = "palette-badge palette-badge-rgba";
    rgbaBadge.textContent = "RGBA";
    badges.push(rgbaBadge);
  }
  if (metadata.isDiscrete) {
    const discreteBadge = document.createElement("span");
    discreteBadge.className = "palette-badge palette-badge-discrete";
    discreteBadge.textContent = "Discrete";
    badges.push(discreteBadge);
  }
  return badges;
}

function renderPaletteMenu() {
  const palettes = Array.isArray(state.volume.availablePalettes) && state.volume.availablePalettes.length > 0
    ? state.volume.availablePalettes
    : ["Inferno"];
  const filter = state.volume.paletteFilter;
  const visiblePalettes = filter
    ? palettes.filter((name) => name.toLowerCase().includes(filter))
    : palettes;
  elements.volumePaletteButtonName.textContent = state.volume.palette || palettes[0];
  elements.volumePaletteButtonSwatch.style.background = paletteGradient(palettePreviewColorsFor(state.volume.palette));
  elements.volumePaletteSearch.value = state.volume.paletteFilter;
  elements.volumePaletteOptions.replaceChildren(
    ...(visiblePalettes.length > 0 ? visiblePalettes : ["No matching palette"]).map((name) => {
      if (name === "No matching palette") {
        const empty = document.createElement("div");
        empty.className = "palette-option";
        empty.setAttribute("aria-disabled", "true");
        empty.textContent = name;
        return empty;
      }
      const option = document.createElement("button");
      option.type = "button";
      option.className = "palette-option";
      option.setAttribute("role", "option");
      option.setAttribute("aria-selected", name === state.volume.palette ? "true" : "false");
      option.dataset.value = name;

      const label = document.createElement("span");
      label.className = "palette-option-name";
      label.textContent = name;

      const badges = document.createElement("span");
      badges.className = "palette-option-badges";
      badges.append(...buildPaletteBadgeElements(name));

      const identity = document.createElement("span");
      identity.className = "palette-option-identity";
      identity.append(label, badges);

      const swatch = document.createElement("span");
      swatch.className = "palette-option-swatch";
      swatch.style.background = paletteGradient(palettePreviewColorsFor(name));

      option.append(identity, swatch);
      option.addEventListener("click", () => {
        if (state.volume.palette !== name) {
          state.volume.palette = name;
          state.volume.palettePreviewColors = [];
          syncPalettePreview();
          sendRenderParams();
        }
        closePaletteMenu();
      });
      return option;
    })
  );
}

function setPaletteMenuOpen(open) {
  state.volume.paletteMenuOpen = Boolean(open);
  elements.volumePaletteMenu.classList.toggle("hidden", !state.volume.paletteMenuOpen);
  elements.volumePaletteButton.dataset.open = state.volume.paletteMenuOpen ? "true" : "false";
  elements.volumePaletteButton.setAttribute("aria-expanded", state.volume.paletteMenuOpen ? "true" : "false");
  if (state.volume.paletteMenuOpen) {
    state.volume.paletteFilter = "";
    renderPaletteMenu();
    window.setTimeout(() => {
      elements.volumePaletteSearch.focus();
      elements.volumePaletteSearch.select();
    }, 0);
  } else {
    state.volume.paletteFilter = "";
    elements.volumePaletteSearch.value = "";
  }
}

function closePaletteMenu({ restoreFocus = false } = {}) {
  if (!state.volume.paletteMenuOpen) {
    return;
  }
  setPaletteMenuOpen(false);
  if (restoreFocus) {
    elements.volumePaletteButton.focus();
  }
}

function mergePaletteCatalog(catalog) {
  if (!Array.isArray(catalog) || catalog.length === 0) {
    return;
  }
  state.volume.paletteCatalog = catalog
    .filter((entry) => entry && typeof entry === "object" && typeof entry.name === "string")
    .map((entry) => ({
      name: entry.name,
      previewColors: Array.isArray(entry.previewColors)
        ? entry.previewColors.filter((color) => typeof color === "string" && color.trim())
        : [],
      hasAlpha: Boolean(entry.hasAlpha),
      isDiscrete: Boolean(entry.isDiscrete),
    }));
  if (state.volume.paletteCatalog.length > 0) {
    state.volume.availablePalettes = state.volume.paletteCatalog.map((entry) => entry.name);
  }
}

function currentPalettePreviewColors() {
  return palettePreviewColorsFor(state.volume.palette);
}

function syncPalettePreview() {
  const colors = currentPalettePreviewColors();
  elements.volumePalettePreview.style.background = paletteGradient(colors);
  const scaleLabel = state.volume.scaleMode === "log" ? "log mapping" : "linear mapping";
  elements.volumePalettePreviewCaption.textContent = `${state.volume.palette} · ${scaleLabel}`;
  elements.volumePaletteButtonName.textContent = state.volume.palette;
  elements.volumePaletteButtonBadges.replaceChildren(...buildPaletteBadgeElements(state.volume.palette));
  elements.volumePaletteButtonSwatch.style.background = paletteGradient(colors);
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
  syncPalettePreview();
  renderPaletteMenu();
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
  if (Array.isArray(incoming.palettePreviewColors) && incoming.palettePreviewColors.length > 0) {
    state.volume.palettePreviewColors = incoming.palettePreviewColors
      .filter((value) => typeof value === "string" && value.trim())
      .map((value) => value.trim());
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

function setActiveControlTab(tabKey) {
  closePaletteMenu();
  state.ui.activeTab = tabKey;
  scheduleAppStatePersist();
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
}

function installControlPanelUI() {

  controlTabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const tabKey = button.dataset.tabTarget;
      if (tabKey) {
        setActiveControlTab(tabKey);
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

  setActiveControlTab(state.ui.activeTab || "session");
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

async function bootstrapApp() {
  restorePersistencePreferences();
  await loadRuntimeConfig();
  syncPersistencePreferenceUI();
  if (state.persistence.restoreOnLoad) {
    restorePersistedAppState();
  }
  syncRuntimeDefaultsToUI();
  syncVolumeControlsToUI();
  renderDatasetBrowser();
  await fetchDatasetBrowser(state.datasets.currentPath, { force: true });
  if (elements.wsUrl.value) {
    connect(elements.wsUrl.value.trim());
  }
}

void bootstrapApp();
