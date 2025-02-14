document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("user-request");
    const chatWindow = document.getElementById("chat-window");
    const loadingMessage = document.getElementById("loading-message");

    chatForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const userMessage = chatInput.value.trim();
        if (!userMessage) {
            alert("メッセージを入力してください");
            return;
        }

        appendMessage("user", "👤 " + userMessage);
        chatInput.value = ""; // 入力欄をクリア
        loadingMessage.style.display = "block"; // AIの返信待機中を表示

        try {
            const response = await fetch("/chat2", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();
            loadingMessage.style.display = "none"; // AIの返信待機中を非表示

            if (data.ai) {
                appendMessage("ai", "🤖 " + data.ai);
            } else {
                appendMessage("ai", "エラーが発生しました。");
            }
        } catch (error) {
            console.error("Error:", error);
            loadingMessage.style.display = "none"; // AIの返信待機中を非表示
            appendMessage("ai", "サーバーに接続できませんでした。");
        }
    });

    function appendMessage(role, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", role);
        messageDiv.textContent = text;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
