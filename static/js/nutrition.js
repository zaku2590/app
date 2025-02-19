document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("upload-form").addEventListener("submit", async function(event) {
        event.preventDefault();
        
        const formData = new FormData();
        const fileInput = document.getElementById("food-image");
        formData.append("food-image", fileInput.files[0]);
        
        const resultWindow = document.getElementById("analysis-result");
        resultWindow.innerHTML = "<strong>解析中...</strong>"; // 解析中メッセージを表示
        
        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            console.log("🚀 サーバーからのレスポンス:", result);  // ✅ JSONの構造を確認

            resultWindow.innerHTML = ""; // クリア

            // エラーハンドリング
            if (result.error) {
                resultWindow.innerHTML = `<strong>エラー: ${result.error}</strong>`;
                return;
            }

            // `result.result` がオブジェクトになっているので、適切に処理
            if (typeof result.result === "object" && result.result.解析結果) {
                resultWindow.innerHTML = `<strong>解析結果:</strong><br>${result.result.解析結果.replace(/\n/g, "<br>")}`;
            } else if (typeof result.result === "string") {
                resultWindow.innerHTML = `<strong>解析結果:</strong><br>${result.result.replace(/\n/g, "<br>")}`;
            } else {
                resultWindow.innerHTML = "<strong>エラー: 解析結果の形式が正しくありません。</strong>";
                console.error("🚨 解析結果のデータ形式エラー:", result.result);
            }

        } catch (error) {
            console.error("🚨 フェッチエラー:", error);
            resultWindow.innerHTML = "<strong>エラーが発生しました。もう一度試してください。</strong>";
        }
    });
});
