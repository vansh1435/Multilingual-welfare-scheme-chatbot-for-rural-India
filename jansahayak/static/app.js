const messages = document.querySelector("#messages");
const form = document.querySelector("#chat-form");
const input = document.querySelector("#message");
const recs = document.querySelector("#recommendations");
const statusText = document.querySelector("#status");
const payloadSize = document.querySelector("#payload-size");
const restart = document.querySelector("#restart");

let sessionId = localStorage.getItem("jansahayak_session");
if (!sessionId) {
  sessionId = `web-${crypto.getRandomValues(new Uint32Array(2)).join("")}`;
  localStorage.setItem("jansahayak_session", sessionId);
}

function addBubble(text, who) {
  const node = document.createElement("div");
  node.className = `bubble ${who}`;
  node.textContent = text;
  messages.appendChild(node);
  messages.scrollTop = messages.scrollHeight;
}

function bytes(text) {
  return new TextEncoder().encode(text || "").length;
}

function renderRecommendations(list, lang) {
  recs.innerHTML = "";
  if (!list || !list.length) {
    const empty = document.createElement("p");
    empty.className = "meta";
    empty.textContent = "No shortlist yet";
    recs.appendChild(empty);
    return;
  }
  list.forEach((item, index) => {
    const card = document.createElement("article");
    card.className = "scheme";

    const title = document.createElement("h3");
    title.textContent = `${index + 1}. ${item.name}`;

    const benefit = document.createElement("p");
    benefit.textContent = item.benefit;

    const meta = document.createElement("div");
    meta.className = "meta";
    meta.textContent = `${item.confidence.replace("_", " ")} · score ${item.score}`;

    const source = document.createElement("a");
    source.href = item.source.url;
    source.target = "_blank";
    source.rel = "noopener";
    source.textContent = item.source.title;

    const button = document.createElement("button");
    button.className = "download";
    button.type = "button";
    button.textContent = "Checklist";
    button.addEventListener("click", () => {
      window.location.href = `/api/checklist?session_id=${encodeURIComponent(sessionId)}&scheme=${encodeURIComponent(item.id)}&lang=${encodeURIComponent(lang || "en")}`;
    });

    card.append(title, benefit, meta, source, button);
    recs.appendChild(card);
  });
}

async function sendMessage(text, showUser = true) {
  if (!text.trim()) return;
  if (showUser) addBubble(text, "user");
  input.value = "";
  input.disabled = true;
  const payload = { session_id: sessionId, message: text, channel: "web" };
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  sessionId = data.session_id;
  localStorage.setItem("jansahayak_session", sessionId);
  addBubble(data.reply, "bot");
  renderRecommendations(data.recommendations, data.lang);
  statusText.textContent = `State: ${data.state}`;
  payloadSize.textContent = `${bytes(data.reply)} B`;
  input.disabled = false;
  input.focus();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll("[data-quick]").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.quick));
});

restart.addEventListener("click", async () => {
  localStorage.removeItem("jansahayak_session");
  sessionId = `web-${crypto.getRandomValues(new Uint32Array(2)).join("")}`;
  localStorage.setItem("jansahayak_session", sessionId);
  messages.innerHTML = "";
  recs.innerHTML = "";
  await sendMessage("restart", false);
});

addBubble("Choose language: 1 Hindi, 2 Tamil, 3 English.", "bot");
renderRecommendations([]);
