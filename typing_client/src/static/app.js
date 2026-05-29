const consent = document.querySelector("#consent");
const typingBox = document.querySelector("#typingBox");
const sendBtn = document.querySelector("#sendBtn");
const loadBtn = document.querySelector("#loadBtn");
const clearBtn = document.querySelector("#clearBtn");
const output = document.querySelector("#output");
const charCount = document.querySelector("#charCount");
const totalLogs = document.querySelector("#totalLogs");
const lastStatus = document.querySelector("#lastStatus");

function showOutput(data) {
  output.textContent = JSON.stringify(data, null, 2);
}

function setStatus(text) {
  lastStatus.textContent = text;
}

consent.addEventListener("change", () => {
  const enabled = consent.checked;
  typingBox.disabled = !enabled;
  sendBtn.disabled = !enabled;
  setStatus(enabled ? "Consent on" : "Ready");
});

typingBox.addEventListener("input", () => {
  charCount.textContent = `${typingBox.value.length} chars`;
});

sendBtn.addEventListener("click", async () => {
  const text = typingBox.value.trim();

  if (!text) {
    showOutput({ error: "Please type a sample first." });
    return;
  }

  setStatus("Sending...");

  const response = await fetch("/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  const result = await response.json();

  showOutput(result);
  setStatus(result.status || "Done");

  await refreshLogs();

  typingBox.value = "";
  charCount.textContent = "0 chars";
});

async function refreshLogs() {
  const response = await fetch("/logs");
  const result = await response.json();

  totalLogs.textContent = result.count ?? 0;
  showOutput(result);

  return result;
}

loadBtn.addEventListener("click", async () => {
  setStatus("Loading...");

  const response = await fetch("/logs");
  const result = await response.json();

  totalLogs.textContent = result.count ?? 0;
  showOutput(result);
  setStatus("Loaded");
});

clearBtn.addEventListener("click", async () => {
  setStatus("Clearing...");

  const response = await fetch("/clear", {
    method: "POST",
  });

  const result = await response.json();

  totalLogs.textContent = "0";
  showOutput(result);
  setStatus("Cleared");
});