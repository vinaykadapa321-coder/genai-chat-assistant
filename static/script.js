const chatContainer = document.getElementById("chatContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const voiceButton = document.getElementById("voiceButton");
const clearButton = document.getElementById("clearButton");
const typingIndicator = document.getElementById("typingIndicator");


// --------------------------------------------------
// Add message to chat
// --------------------------------------------------

function addMessage(sender, message, isUser = false) {

    const messageElement = document.createElement("div");

    messageElement.className = isUser
        ? "message user-message"
        : "message ai-message";

    const avatar = isUser ? "👤" : "🤖";

    let formattedMessage;

    if (isUser) {
        formattedMessage = escapeHtml(message);
    } else {
        // Convert Markdown to HTML
        formattedMessage = marked.parse(message);
    }

    messageElement.innerHTML = `
        <div class="avatar">
            ${avatar}
        </div>

        <div class="message-content">

            <div class="message-name">
                ${isUser ? "You" : "AI Assistant"}
            </div>

            <div class="bubble">
                ${formattedMessage}
            </div>

        </div>
    `;

    chatContainer.appendChild(messageElement);

    scrollToBottom();
}


// --------------------------------------------------
// Escape HTML for user messages
// --------------------------------------------------

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// --------------------------------------------------
// Scroll chat to bottom
// --------------------------------------------------

function scrollToBottom() {

    chatContainer.scrollTop = chatContainer.scrollHeight;
}


// --------------------------------------------------
// Show loading
// --------------------------------------------------

function showLoading() {

    typingIndicator.classList.remove("hidden");

    sendButton.disabled = true;
    voiceButton.disabled = true;

    scrollToBottom();
}


// --------------------------------------------------
// Hide loading
// --------------------------------------------------

function hideLoading() {

    typingIndicator.classList.add("hidden");

    sendButton.disabled = false;
    voiceButton.disabled = false;
}


// --------------------------------------------------
// Send text message
// --------------------------------------------------

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Display user message
    addMessage("You", message, true);

    // Clear input
    messageInput.value = "";

    // Reset textarea height
    messageInput.style.height = "auto";

    showLoading();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        const data = await response.json();


        if (!response.ok) {

            addMessage(
                "AI Assistant",
                data.reply || "Something went wrong."
            );

            return;
        }


        addMessage(
            "AI Assistant",
            data.reply || "No response received."
        );

    }

    catch (error) {

        console.error("Chat error:", error);

        addMessage(
            "AI Assistant",
            "❌ Unable to connect to the server. Please try again."
        );
    }

    finally {

        hideLoading();
    }
}


// --------------------------------------------------
// Voice input
// --------------------------------------------------

async function startVoice() {

    showLoading();

    voiceButton.classList.add("recording");

    voiceButton.innerHTML = "🔴";

    try {

        const response = await fetch("/voice");

        const data = await response.json();


        // Display recognized speech
        if (data.user) {

            addMessage(
                "You",
                data.user,
                true
            );
        }


        // Display AI response
        if (data.reply) {

            addMessage(
                "AI Assistant",
                data.reply
            );
        }

    }

    catch (error) {

        console.error("Voice error:", error);

        addMessage(
            "AI Assistant",
            "❌ Voice processing failed. Please try again."
        );
    }

    finally {

        hideLoading();

        voiceButton.classList.remove("recording");

        voiceButton.innerHTML = "🎤";
    }
}


// --------------------------------------------------
// Clear chat
// --------------------------------------------------

function clearChat() {

    chatContainer.innerHTML = `
        <div class="message ai-message">

            <div class="avatar">
                🤖
            </div>

            <div class="message-content">

                <div class="message-name">
                    AI Assistant
                </div>

                <div class="bubble">

                    <p>
                        Hello! 👋
                    </p>

                    <p>
                        Chat cleared. How can I help you?
                    </p>

                </div>

            </div>

        </div>
    `;
}


// --------------------------------------------------
// Enter key
// --------------------------------------------------

messageInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
});


// --------------------------------------------------
// Auto resize textarea
// --------------------------------------------------

messageInput.addEventListener("input", function() {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 150) + "px";
});


// --------------------------------------------------
// Button events
// --------------------------------------------------

sendButton.addEventListener("click", sendMessage);

voiceButton.addEventListener("click", startVoice);

clearButton.addEventListener("click", clearChat);