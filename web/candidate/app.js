const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const start = document.getElementById("start");
const stop = document.getElementById("stop");
const statusEl = document.getElementById("status");
const sessionEl = document.getElementById("session");

let stream = null;
let timer = null;
let sessionId = null;
let tabSwitchWarningActive = false;

async function reportAlert(signal, message, severity = 2, confidence = 1.0) {
  if (!sessionId) return;

  try {
    await fetch("/api/event", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        session_id: sessionId,
        signal,
        severity,
        confidence,
        message,
        timestamp: Date.now() / 1000
      })
    });
  } catch (err) {
    console.warn("Event dispatch failed:", err);
  }
}

function handleTabVisibilityChange() {
  if (!sessionId) return;

  if (document.hidden && !tabSwitchWarningActive) {
    tabSwitchWarningActive = true;
    statusEl.textContent = "Tab switched away — suspicious activity detected";
    reportAlert("TAB_SWITCH", "Candidate switched away from the exam tab.", 4, 1.0);
  }

  if (!document.hidden) {
    tabSwitchWarningActive = false;
    statusEl.textContent = "Proctoring active — focus restored";
  }
}

async function createSession() {
  const res = await fetch("/api/session/start", {method: "POST"});
  const data = await res.json();
  sessionId = data.session_id;
  sessionEl.textContent = "Session: " + sessionId;
}

async function sendFrame() {
  if (!stream || !sessionId) return;

  const ctx = canvas.getContext("2d");
  canvas.width = video.videoWidth || 640;
  canvas.height = video.videoHeight || 480;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const frame = canvas.toDataURL("image/jpeg", 0.65);

  try {
    await fetch("/api/frame", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        session_id: sessionId,
        frame_base64: frame,
        timestamp: Date.now() / 1000
      })
    });
    statusEl.textContent = "Proctoring active — frame sent";
  } catch {
    statusEl.textContent = "Connection problem";
  }
}

start.onclick = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: {width: {ideal: 640}, height: {ideal: 480}},
      audio: false
    });
    video.srcObject = stream;
    await createSession();
    document.addEventListener("visibilitychange", handleTabVisibilityChange);
    window.addEventListener("blur", () => {
      if (sessionId && !tabSwitchWarningActive) {
        tabSwitchWarningActive = true;
        statusEl.textContent = "Window lost focus — suspicious activity detected";
        reportAlert("TAB_SWITCH", "Candidate switched away from the exam window.", 4, 1.0);
      }
    });
    window.addEventListener("focus", () => {
      tabSwitchWarningActive = false;
      statusEl.textContent = "Proctoring active — window focus restored";
    });
    timer = setInterval(sendFrame, 1000);
    start.disabled = true;
    stop.disabled = false;
  } catch (err) {
    statusEl.textContent = "Camera permission failed: " + err.message;
  }
};

stop.onclick = () => {
  if (timer) clearInterval(timer);
  if (stream) stream.getTracks().forEach(t => t.stop());
  timer = null;
  stream = null;
  video.srcObject = null;
  start.disabled = false;
  stop.disabled = true;
  statusEl.textContent = "Stopped";
};
