let activeConversationId = null;

document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chatLayoutContainer");
    if (!chatContainer) return;

    activeConversationId = chatContainer.dataset.activeConvId;

    const chatForm = document.getElementById("chatForm");
    if (chatForm) {
        chatForm.addEventListener("submit", sendMessage);
    }

    if (activeConversationId) {
        loadConversation(activeConversationId);
    }
});

/**
 * Fetches and displays messages for a specific conversation
 * @param {string} convId - ID of the conversation to load
 */
function loadConversation(convId) {
    activeConversationId = convId;

    const sidebarItems = document.querySelectorAll(".conversation-item");
    sidebarItems.forEach(item => {
        if (item.getAttribute("data-id") === convId) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });

    const messageLog = document.getElementById("chatMessageLog");
    if (!messageLog) return;

    messageLog.innerHTML = `
        <div class="text-center py-5 text-muted">
            <div class="spinner-border spinner-border-sm text-primary me-2"></div>
            Loading conversation...
        </div>
    `;

    fetch(`/chatbot/conversation/${convId}/`)
        .then(res => res.json())
        .then(data => {
            if (!data.success) return;

            const titleHeader = document.getElementById("currentChatTitle");
            if (titleHeader) {
                titleHeader.textContent = data.title;
            }

            messageLog.innerHTML = "";

            if (data.messages.length === 0) {
                messageLog.innerHTML = `
                    <div class="text-center py-5 text-muted">
                        <i class="bi bi-chat-heart fs-1 mb-3 text-primary opacity-50 d-block"></i>
                        <h5 class="fw-bold text-dark">Start the Conversation</h5>
                        <p class="small mb-0">Ask anything related to employee handbook, company policy, or support guidelines.</p>
                    </div>
                `;
                return;
            }

            data.messages.forEach(msg => {
                appendMessageBubble(msg.question, msg.ai_answer, msg.created_at);
            });
            scrollToBottom();
        })
        .catch(err => {
            messageLog.innerHTML = `
                <div class="text-center py-5 text-danger">
                    <i class="bi bi-exclamation-triangle fs-1 d-block mb-2"></i>
                    Failed to load conversation.
                </div>
            `;
        });
}

/**
 * Appends a user message and AI response bubble to the chat logs window
 * @param {string} question - Question typed by user
 * @param {string} answer - Answer returned by Llama 3 AI
 * @param {string} timeStr - Timestamp string
 */
function appendMessageBubble(question, answer, timeStr) {
    const messageLog = document.getElementById("chatMessageLog");
    if (!messageLog) return;

    const emptyState = messageLog.querySelector(".text-center");
    if (emptyState) {
        emptyState.remove();
    }

    const userMsg = document.createElement("div");
    userMsg.className = "msg-wrapper user";
    userMsg.innerHTML = `
        <div class="msg-bubble">
            <div>${escapeHtml(question)}</div>
            <small class="msg-meta">${timeStr}</small>
        </div>
    `;
    messageLog.appendChild(userMsg);

    const aiMsg = document.createElement("div");
    aiMsg.className = "msg-wrapper ai";
    aiMsg.innerHTML = `
        <div class="msg-bubble">
            <div>${answer}</div>
            <small class="msg-meta">${timeStr}</small>
        </div>
    `;
    messageLog.appendChild(aiMsg);
}

function scrollToBottom() {
    const messageLog = document.getElementById("chatMessageLog");
    if (messageLog) {
        messageLog.scrollTop = messageLog.scrollHeight;
    }
}

/**
 * Encodes special HTML characters to prevent XSS vulnerability when rendering user inputs
 * @param {string} text - Raw input string
 * @returns {string} Safe HTML string
 */
function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Captures user input and sends it to the server backend
 * @param {Event} e - Submit event object
 */
function sendMessage(e) {
    e.preventDefault();

    const inputField = document.getElementById("userInput");
    if (!inputField) return;

    const question = inputField.value.trim();
    if (!question) return;

    inputField.value = "";

    const indicator = document.getElementById("typingIndicator");
    if (indicator) {
        indicator.style.display = "inline-flex";
    }
    scrollToBottom();

    const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

    fetch("/chatbot/conversation/send/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            conversation_id: activeConversationId,
            question: question
        })
    })
        .then(res => res.json())
        .then(data => {
            if (indicator) {
                indicator.style.display = "none";
            }

            if (data.success) {
                appendMessageBubble(data.question, data.ai_answer, data.created_at);

                const titleSpan = document.getElementById(`title-${activeConversationId}`);
                if (titleSpan) {
                    titleSpan.textContent = data.conv_title;
                }

                const titleHeader = document.getElementById("currentChatTitle");
                if (titleHeader) {
                    titleHeader.textContent = data.conv_title;
                }

                scrollToBottom();
            } else {
                alert(`Error sending message: ${data.error}`);
            }
        })
        .catch(err => {
            if (indicator) {
                indicator.style.display = "none";
            }
            alert("Error connecting to server. Please try again.");
        });
}
