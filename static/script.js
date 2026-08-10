// ==========================================
// GenAI Chat Assistant - script.js
// ==========================================


// ==========================================
// Send Text Message
// ==========================================

async function sendMessage() {
    const messageInput = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");

    if (!messageInput) {
        console.error("messageInput not found");
        return;
    }

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Show user's message
    addMessage("You", message);

    // Clear input
    messageInput.value = "";

    // Disable send button
    if (sendButton) {
        sendButton.disabled = true;
        sendButton.textContent = "Sending...";
    }

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

        if (!response.ok) {
            throw new Error("Server error: " + response.status);
        }

        const data = await response.json();

        if (data.reply) {
            addMessage("AI", data.reply);
        } else {
            addMessage("AI", "No response received.");
        }

    } catch (error) {
        console.error("Chat Error:", error);

        addMessage(
            "AI",
            "Sorry, something went wrong. Please try again."
        );

    } finally {
        // Enable send button
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.textContent = "Send";
        }

        messageInput.focus();
    }
}


// ==========================================
// Voice Assistant
// ==========================================

async function startVoiceRecognition() {
    const micButton = document.getElementById("micButton");
    const messageInput = document.getElementById("messageInput");

    try {
        // Change microphone button
        if (micButton) {
            micButton.textContent = "🔴";
            micButton.disabled = true;
        }

        console.log("Starting voice recognition...");

        // Call Flask /voice endpoint
        const response = await fetch("/voice", {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error("Voice server error: " + response.status);
        }

        const data = await response.json();

        console.log("Voice response:", data);

        // Display recognized speech
        if (data.user) {
            if (messageInput) {
                messageInput.value = data.user;
            }

            addMessage("You", data.user);
        }

        // Display AI response
        if (data.reply) {
            addMessage("AI", data.reply);
        } else {
            addMessage(
                "AI",
                "I couldn't generate a response."
            );
        }

    } catch (error) {
        console.error("Voice Error:", error);

        addMessage(
            "AI",
            "Could not process your voice. Please try again."
        );

    } finally {
        // Reset microphone button
        if (micButton) {
            micButton.textContent = "🎤";
            micButton.disabled = false;
        }

        console.log("Voice recognition finished.");
    }
}


// ==========================================
// Add Message to Chat
// ==========================================

function addMessage(sender, message) {
    const chatMessages =
        document.getElementById("chatMessages");

    if (!chatMessages) {
        console.error("chatMessages element not found");
        return;
    }

    const messageDiv =
        document.createElement("div");

    // Add different class for user and AI
    if (sender === "You") {
        messageDiv.className = "user-message";
    } else {
        messageDiv.className = "bot-message";
    }

    const strong =
        document.createElement("strong");

    strong.textContent = sender + ":";

    const span =
        document.createElement("span");

    span.textContent = " " + message;

    messageDiv.appendChild(strong);
    messageDiv.appendChild(span);

    chatMessages.appendChild(messageDiv);

    // Scroll to latest message
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// ==========================================
// Enter Key Support
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const messageInput =
            document.getElementById("messageInput");

        if (messageInput) {

            messageInput.addEventListener(
                "keydown",
                function (event) {

                    if (event.key === "Enter") {

                        event.preventDefault();

                        sendMessage();
                    }
                }
            );
        }

    }
);