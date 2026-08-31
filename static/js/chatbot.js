let activeConversationId = null;
let chatUserName = "";

document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chatLayoutContainer");
    if (!chatContainer) return;

    activeConversationId = chatContainer.dataset.activeConvId;
    chatUserName = chatContainer.dataset.userName || "";

    const chatForm = document.getElementById("chatForm");
    if (chatForm) {
        chatForm.addEventListener("submit", sendMessage);
    }

    if (activeConversationId) {
        loadConversation(activeConversationId);
    }
});

function loadConversation(convId) {
    activeConversationId = convId;

    document.querySelectorAll(".conversation-item").forEach(item => {
        item.classList.toggle("active", item.getAttribute("data-id") === convId);
    });

    const messageLog = document.getElementById("chatMessageLog");
    if (!messageLog) return;

    messageLog.innerHTML = `<div class="text-center py-5 text-muted">Loading...</div>`;

    fetch(`/chatbot/conversation/${convId}/`)
        .then(res => res.json())
        .then(data => {
            if (!data.success) return;

            const titleHeader = document.getElementById("currentChatTitle");
            if (titleHeader && chatUserName) {
                titleHeader.textContent = chatUserName;
            }

            messageLog.innerHTML = "";

            if (data.messages.length === 0) {
                messageLog.innerHTML = `
                    <div class="text-center py-5 text-muted">
                        <h5 class="fw-bold text-dark">Start the Conversation</h5>
                        <p class="small mb-0">Ask anything related to company policy or support guidelines.</p>
                    </div>`;
                return;
            }

            data.messages.forEach(msg => appendMessageBubble(msg.question, msg.ai_answer, msg.created_at));
            scrollToBottom();
        })
        .catch(() => {
            messageLog.innerHTML = `<div class="text-center py-5 text-danger">Failed to load conversation.</div>`;
        });
}

function appendMessageBubble(question, answer, timeStr) {
    const messageLog = document.getElementById("chatMessageLog");
    if (!messageLog) return;

    const emptyState = messageLog.querySelector(".text-center");
    if (emptyState) emptyState.remove();

    const userMsg = document.createElement("div");
    userMsg.className = "msg-wrapper user";
    userMsg.innerHTML = `
        <div class="msg-bubble">
            <div class="msg-sender">${escapeHtml(chatUserName)}</div>
            <div>${escapeHtml(question)}</div>
            <small class="msg-meta">${timeStr}</small>
        </div>`;
    messageLog.appendChild(userMsg);

    const aiMsg = document.createElement("div");
    aiMsg.className = "msg-wrapper ai";
    aiMsg.innerHTML = `
        <div class="msg-bubble">
            <div class="msg-sender">SupportSphere AI</div>
            <div>${answer}</div>
            <small class="msg-meta">${timeStr}</small>
        </div>`;
    messageLog.appendChild(aiMsg);
}

function scrollToBottom() {
    const messageLog = document.getElementById("chatMessageLog");
    if (messageLog) messageLog.scrollTop = messageLog.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function sendMessage(e) {
    e.preventDefault();

    const inputField = document.getElementById("userInput");
    if (!inputField) return;

    const question = inputField.value.trim();
    if (!question) return;

    inputField.value = "";

    const indicator = document.getElementById("typingIndicator");
    if (indicator) indicator.style.display = "inline-flex";
    scrollToBottom();

    const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

    fetch("/chatbot/conversation/send/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ conversation_id: activeConversationId, question })
    })
    .then(res => res.json())
    .then(data => {
        if (indicator) indicator.style.display = "none";
        if (data.success) {
            appendMessageBubble(data.question, data.ai_answer, data.created_at);
            scrollToBottom();
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(() => {
        if (indicator) indicator.style.display = "none";
        alert("Error connecting to server. Please try again.");
    });
}
