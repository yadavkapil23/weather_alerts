const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");

function addMessage(text, type) {
    const messageDiv = document.createElement("div");
    messageDiv.className = type;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to Fetch Disaster Alerts
async function fetchAlerts() {
    try {
        const response = await fetch("http://127.0.0.1:5000/disaster_alerts");
        const data = await response.json();
        let message = "🌍 Latest Disaster Alerts:\n\n";
        data.alerts.forEach(alert => {
            message += `⚠️ ${alert.title}\n🔗 More info: ${alert.link}\n\n`;
        });
        addMessage(message, "bot");
    } catch (error) {
        console.error("Error fetching alerts:", error);
        addMessage("❌ Unable to fetch disaster updates.", "bot");
    }
}

// Function to Send User Message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    addMessage(message, "user");
    userInput.value = "";

    if (message.toLowerCase().includes("disaster update")) {
        fetchAlerts();
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        addMessage(data.response, "bot");
    } catch (error) {
        console.error("Error:", error);
        addMessage("❌ Oops! Something went wrong.", "bot");
    }
}

sendButton.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") sendMessage();
});
