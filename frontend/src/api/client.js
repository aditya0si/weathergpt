const API_BASE = "";

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function sendChatMessage(message, language = null, sessionId = "default-session") {
  const res = await fetch(`${API_BASE}/api/v1/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      language,
      session_id: sessionId,
    }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to process chat query");
  }
  return res.json();
}

export async function fetchCurrentWeather(location = "Guwahati") {
  const res = await fetch(`${API_BASE}/api/v1/weather/current?location=${encodeURIComponent(location)}`);
  if (!res.ok) throw new Error("Failed to fetch weather");
  return res.json();
}

export async function fetchForecast(location = "Guwahati", days = 7) {
  const res = await fetch(`${API_BASE}/api/v1/weather/forecast?location=${encodeURIComponent(location)}&days=${days}`);
  if (!res.ok) throw new Error("Failed to fetch forecast");
  return res.json();
}

export async function fetchAlerts(location = "Guwahati") {
  const res = await fetch(`${API_BASE}/api/v1/weather/alerts?location=${encodeURIComponent(location)}`);
  if (!res.ok) throw new Error("Failed to fetch alerts");
  return res.json();
}
