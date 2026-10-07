const root = document.getElementById("sessions");
const refresh = document.getElementById("refresh");
const updated = document.getElementById("updated");
const connection = document.getElementById("connection");
let loading = false;

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function timeLabel(value) {
  const timestamp = Number(value);
  if (!timestamp) return "Not yet received";
  const seconds = Math.max(0, Math.floor(Date.now() / 1000 - timestamp));
  if (seconds < 5) return "Just now";
  if (seconds < 60) return `${seconds}s ago`;
  return `${Math.floor(seconds / 60)}m ago`;
}

function statusLabel(status) {
  return ({
    ACTIVE: "Active",
    REVIEW_REQUIRED: "Needs review",
    INACTIVE: "Inactive"
  })[status] || status || "Unknown";
}

async function load() {
  if (loading) return;
  loading = true;
  refresh.disabled = true;
  connection.textContent = "Updating";

  try {
    const res = await fetch("/api/sessions", {cache: "no-store"});
    if (!res.ok) throw new Error(`Sessions request failed: ${res.status}`);
    const data = await res.json();
    const sessions = Array.isArray(data.sessions) ? data.sessions : [];

    if (!sessions.length) {
      document.getElementById("count-total").textContent = "0";
      document.getElementById("count-active").textContent = "0";
      document.getElementById("count-review").textContent = "0";
      document.getElementById("count-inactive").textContent = "0";
      root.innerHTML = '<div class="empty-state"><strong>No sessions yet</strong><span>New candidate sessions will appear here automatically.</span></div>';
      updated.textContent = `Updated ${new Date().toLocaleTimeString()}`;
      connection.textContent = "Connected";
      connection.className = "connection connected";
      return;
    }

    const alertResults = await Promise.all(sessions.map(async s => {
      try {
        const response = await fetch(`/api/alerts/${encodeURIComponent(s.session_id)}`, {cache: "no-store"});
        if (!response.ok) throw new Error("Alert request failed");
        const payload = await response.json();
        return [s.session_id, Array.isArray(payload.alerts) ? payload.alerts : []];
      } catch {
        return [s.session_id, null];
      }
    }));
    const alertsBySession = new Map(alertResults);
    const now = Date.now() / 1000;
    const presentedSessions = sessions.map(session => {
      const alerts = alertsBySession.get(session.session_id);
      const latestAlertTime = Number(alerts?.[0]?.timestamp) || 0;
      const lastSeen = Math.max(Number(session.last_seen) || 0, latestAlertTime);
      const alertScore = alerts?.reduce((total, alert) => {
        if (alert.signal === "NORMAL") return total;
        return total + (Number(alert.severity) || 0) * (Number(alert.confidence) || 0);
      }, 0) || 0;
      const score = Math.max(Number(session.score) || 0, alertScore);
      const status = session.status === "REVIEW_REQUIRED" || score >= 10
        ? "REVIEW_REQUIRED"
        : lastSeen && now - lastSeen <= 8 ? "ACTIVE" : "INACTIVE";
      return {...session, score, status, last_seen: lastSeen};
    });
    const counts = {
      total: presentedSessions.length,
      active: presentedSessions.filter(s => s.status === "ACTIVE").length,
      review: presentedSessions.filter(s => s.status === "REVIEW_REQUIRED").length,
      inactive: presentedSessions.filter(s => s.status === "INACTIVE").length
    };
    document.getElementById("count-total").textContent = counts.total;
    document.getElementById("count-active").textContent = counts.active;
    document.getElementById("count-review").textContent = counts.review;
    document.getElementById("count-inactive").textContent = counts.inactive;
    updated.textContent = `Updated ${new Date().toLocaleTimeString()}`;
    connection.textContent = "Connected";
    connection.className = "connection connected";

    root.innerHTML = presentedSessions.map(s => {
      const score = Math.min(10, Math.max(0, Number(s.score) || 0));
      const riskWidth = Math.min(100, score * 10);
      const alerts = alertsBySession.get(s.session_id);
      const latestAlert = alerts?.[0];
      const alertMarkup = alerts === null
        ? '<p class="alert-empty">Alert feed unavailable.</p>'
        : alerts?.length
          ? alerts.slice(0, 3).map(a => `<div class="alert"><span class="alert-signal">${escapeHTML(a.signal)}</span><span>${escapeHTML(a.message || "No detail provided")}</span><time>${timeLabel(a.timestamp)}</time></div>`).join("")
          : '<p class="alert-empty">No risk signals recorded.</p>';
      const statusClass = s.status === "REVIEW_REQUIRED" ? "review" : s.status === "INACTIVE" ? "inactive" : "active";
      return `<article class="session ${statusClass}">
        <div class="session-top"><div class="identity"><span class="status-dot"></span><div><h3>Candidate session</h3><code>${escapeHTML(s.session_id)}</code></div></div><span class="status-badge">${escapeHTML(statusLabel(s.status))}</span></div>
        <div class="session-stats"><div><span>Risk score</span><strong>${score.toFixed(1)} <small>/ 10</small></strong><div class="risk-track"><i style="width:${riskWidth}%"></i></div></div><div><span>Latest signal</span><strong>${escapeHTML(s.last_signal || alerts?.[0]?.signal || "None")}</strong></div><div><span>Last camera frame</span><strong>${timeLabel(s.last_seen)}</strong></div><div><span>Recent alerts</span><strong>${alerts === null ? "—" : alerts.length}</strong></div></div>
        ${s.last_message ? `<p class="last-message">${escapeHTML(s.last_message)}</p>` : ""}
        <details class="alert-details"><summary>Recent signals${latestAlert ? ` · latest ${timeLabel(latestAlert.timestamp)}` : ""}</summary><div class="alert-list">${alertMarkup}</div></details>
      </article>`;
    }).join("");
  } catch (err) {
    connection.textContent = "Connection issue";
    connection.className = "connection disconnected";
    updated.textContent = "Could not refresh dashboard";
  } finally {
    loading = false;
    refresh.disabled = false;
  }
}

refresh.onclick = load;
load();
