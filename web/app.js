const elements = {
  appShell: document.getElementById("appShell"),
  stageFrame: document.getElementById("stageFrame"),
  stageOverlay: document.getElementById("stageOverlay"),
  remoteVideo: document.getElementById("remoteVideo"),
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
  eventLog: document.getElementById("eventLog"),
  clearLogButton: document.getElementById("clearLogButton"),
};

const state = {
  ws: null,
  wsUrl: "",
  reconnectTimer: null,
  reconnectAttempts: 0,
  reconnectEnabled: true,
  shouldReconnect: true,
  pc: null,
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
    bitrate: 10,
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
    opacityScale: 1.8,
    sampleDistanceScale: 1.2,
    imageSampleDistance: 2.2,
    shade: true,
    sliceAxis: "z",
    slicePosition: 0.5,
    cropping: {
      enabled: false,
      bounds: [0, 1, 0, 1, 0, 1],
    },
  },
};

const DEFAULT_WS_URL = "/ws";
{
  const initialWsUrl = pickInitialWsUrl();
  elements.wsUrl.value = initialWsUrl && initialWsUrl.trim() ? initialWsUrl.trim() : DEFAULT_WS_URL;
  console.info("[VisIVO Connect] bootstrap wsUrl=", elements.wsUrl.value, "location=", window.location.href);
}
elements.sessionId.textContent = state.sessionId;
elements.renderScaleValue.textContent = formatScale(state.renderParams.scale);
elements.bitrateValue.textContent = formatBitrate(state.renderParams.bitrate);
elements.targetFpsValue.textContent = formatFps(state.renderParams.targetFps);
elements.visualizationMode.value = state.visualization.mode;
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

elements.volumeSampleDistanceScale.addEventListener("input", () => {
  state.volume.sampleDistanceScale = Number(elements.volumeSampleDistanceScale.value);
  elements.volumeSampleDistanceScaleValue.textContent = formatFloat(state.volume.sampleDistanceScale);
  sendRenderParams();
});

elements.volumeImageSampleDistance.addEventListener("input", () => {
  state.volume.imageSampleDistance = Number(elements.volumeImageSampleDistance.value);
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
    });
    sendRenderParams();
    reportResize(true);
    maybeCreatePeerConnection();
  });

  socket.addEventListener("message", (event) => {
    handleSocketMessage(event.data);
  });

  socket.addEventListener("close", (event) => {
    state.ws = null;
    elements.disconnectButton.disabled = true;
    elements.connectButton.disabled = false;
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
    case "error":
      setConnectionState("error", "danger", message.message || "Server error");
      break;
    case "pong":
      break;
    default:
      logEvent(`RX ${message.type || "unknown"}`);
  }
}

function maybeCreatePeerConnection() {
  if (state.pc) {
    return state.pc;
  }

  const pc = new RTCPeerConnection({
    iceServers: [],
  });
  state.pc = pc;

  pc.addEventListener("track", (event) => {
    const [stream] = event.streams;
    if (stream) {
      state.remoteStream = stream;
      elements.remoteVideo.srcObject = stream;
      state.videoTrackFound = true;
      elements.stageOverlay.classList.add("hidden");
      logEvent("VisIVO Connect track attached");
    }
  });

  pc.addEventListener("icecandidate", (event) => {
    if (event.candidate) {
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
      elements.stageOverlay.classList.add("hidden");
      setConnectionState("connected", "ok");
    }
    if (pc.connectionState === "failed" || pc.connectionState === "disconnected") {
      setConnectionState("reconnecting", "warn", "RTC reconnecting");
    }
  });

  pc.addTransceiver("video", { direction: "recvonly" });
  return pc;
}

async function applyRemoteDescription(payload) {
  const pc = maybeCreatePeerConnection();
  const sdp = normalizeDescription(payload);
  if (!sdp) {
    return;
  }

  await pc.setRemoteDescription(sdp);
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
  const candidate = payload?.candidate ?? payload;
  if (!candidate || !pc.remoteDescription) {
    return;
  }
  try {
    await pc.addIceCandidate(candidate);
  } catch (error) {
    console.warn("Failed to add ICE candidate", error);
  }
}

function cleanupPeerConnection() {
  clearTimeout(state.pendingInteractionEnd);
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
  state.remoteStream = null;
  state.videoTrackFound = false;
  elements.remoteVideo.srcObject = null;
  elements.stageOverlay.classList.remove("hidden");
}

function send(payload) {
  if (!state.ws || state.ws.readyState !== WebSocket.OPEN) {
    return false;
  }
  state.ws.send(JSON.stringify(payload));
  return true;
}

function sendRenderParams() {
  send({
    type: "render.params",
    sessionId: state.sessionId,
    params: {
      mode: state.renderMode,
      scale: state.renderParams.scale,
      bitrateMbps: state.renderParams.bitrate,
      targetFps: state.renderParams.targetFps,
      visualizationMode: state.visualization.mode,
      isoValue: state.visualization.isoValue,
      volume: buildVolumeParamsPayload(),
    },
  });
  logEvent(
    `Render params scale=${state.renderParams.scale.toFixed(2)} bitrate=${state.renderParams.bitrate}Mbps vis=${state.visualization.mode} mode=${state.volume.renderMode} iso=${formatIso(state.visualization.isoValue)}`
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

    const point = normalizePoint(event);
    pointer.last = point;
    state.activePointers.set(event.pointerId, pointer);

    if (state.activePointers.size === 1) {
      const baseline = state.pointerBaseline || point;
      const dx = point.x - baseline.x;
      const dy = point.y - baseline.y;
      sendInteractionMove({
        kind: pointer.kind,
        pointerId: event.pointerId,
        x: point.x,
        y: point.y,
        dx,
        dy,
        buttons: event.buttons,
        pressure: event.pressure,
      });
    } else if (state.activePointers.size >= 2) {
      const [first, second] = [...state.activePointers.values()];
      const center = midpoint(first.last, second.last);
      const distance = Math.hypot(second.last.x - first.last.x, second.last.y - first.last.y);
      const scale = state.gestureStartDistance ? distance / state.gestureStartDistance : 1;
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
    const payload = {
      type: "camera.wheel",
      sessionId: state.sessionId,
      deltaX: event.deltaX,
      deltaY: event.deltaY,
      deltaMode: event.deltaMode,
      ctrlKey: event.ctrlKey,
      shiftKey: event.shiftKey,
      altKey: event.altKey,
      mode: event.ctrlKey ? "zoom" : "pan",
    };
    send(payload);
    logGesture("wheel", `${payload.mode} ${Math.round(event.deltaX)},${Math.round(event.deltaY)}`);
    scheduleInteractionEnd();
  }, { passive: false });

  target.addEventListener("contextmenu", (event) => {
    event.preventDefault();
  });

  function finishPointer(event) {
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
    }
    if (state.activePointers.size === 0) {
      state.pointerBaseline = null;
      scheduleInteractionEnd();
    }
    logGesture("pointerup", `${event.pointerType}`);
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

function syncVolumeControlsToUI() {
  elements.volumeRenderMode.value = state.volume.renderMode;
  elements.volumeOpacityScale.value = String(state.volume.opacityScale);
  elements.volumeOpacityScaleValue.textContent = formatFloat(state.volume.opacityScale);
  elements.volumeSampleDistanceScale.value = String(state.volume.sampleDistanceScale);
  elements.volumeSampleDistanceScaleValue.textContent = formatFloat(state.volume.sampleDistanceScale);
  elements.volumeImageSampleDistance.value = String(state.volume.imageSampleDistance);
  elements.volumeImageSampleDistanceValue.textContent = formatFloat(state.volume.imageSampleDistance);
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
  if (Number.isFinite(incoming.opacityScale)) {
    state.volume.opacityScale = Number(incoming.opacityScale);
  }
  if (Number.isFinite(incoming.sampleDistanceScale)) {
    state.volume.sampleDistanceScale = Number(incoming.sampleDistanceScale);
  }
  if (Number.isFinite(incoming.imageSampleDistance)) {
    state.volume.imageSampleDistance = Number(incoming.imageSampleDistance);
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
  return {
    renderMode: state.volume.renderMode,
    opacityScale: state.volume.opacityScale,
    sampleDistanceScale: state.volume.sampleDistanceScale,
    imageSampleDistance: state.volume.imageSampleDistance,
    shade: state.volume.shade,
    sliceAxis: state.volume.sliceAxis,
    slicePosition: state.volume.slicePosition,
    cropping: {
      enabled: state.volume.cropping.enabled,
      bounds: state.volume.cropping.bounds,
    },
  };
}

function applyAutoContrastPreset() {
  state.visualization.mode = "volume";
  elements.visualizationMode.value = "volume";

  if (state.volume.renderMode === "slice") {
    state.volume.renderMode = "composite";
  }

  if (state.volume.renderMode === "mip") {
    state.volume.opacityScale = 1.0;
    state.volume.sampleDistanceScale = state.renderMode === "interactive" ? 1.4 : 1.0;
    state.volume.imageSampleDistance = state.renderMode === "interactive" ? 1.8 : 1.2;
    state.volume.shade = false;
  } else {
    state.volume.renderMode = "composite";
    state.volume.opacityScale = 2.3;
    state.volume.sampleDistanceScale = state.renderMode === "interactive" ? 1.2 : 0.9;
    state.volume.imageSampleDistance = state.renderMode === "interactive" ? 2.0 : 1.2;
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
