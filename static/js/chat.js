/**
 * Chat Page JavaScript
 * Handles message sending, AI response rendering, and voice input.
 */

let conversationId = null;

const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const btnVoice = document.getElementById("btn-voice");

// ── Send Message ──────────────────────────────────────────────

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("user", message);
    chatInput.value = "";

    try {
        const res = await fetch("/chat/send", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, conversation_id: conversationId }),
        });
        const data = await res.json();
        conversationId = data.conversation_id;
        appendMessage("assistant", data.response);
    } catch (err) {
        appendMessage("assistant", "Sorry, something went wrong. Please try again.");
    }
});

// ── Render Message Bubble ─────────────────────────────────────

function appendMessage(role, content) {
    // Remove the placeholder if present
    const placeholder = chatMessages.querySelector(".text-center.text-muted");
    if (placeholder) placeholder.remove();

    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.innerHTML = `<div class="bubble">${escapeHtml(content)}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// ── Voice Input (Browser Web Speech API) ──────────────────────

if (btnVoice && "webkitSpeechRecognition" in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;

    btnVoice.addEventListener("click", () => {
        recognition.start();
        btnVoice.classList.add("btn-danger");
        btnVoice.innerHTML = '<i class="bi bi-mic-fill"></i> Listening...';
    });

    recognition.onresult = (event) => {
        chatInput.value = event.results[0][0].transcript;
        btnVoice.classList.remove("btn-danger");
        btnVoice.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
    };

    recognition.onerror = () => {
        btnVoice.classList.remove("btn-danger");
        btnVoice.innerHTML = '<i class="bi bi-mic"></i> Voice Input';
    };
}
