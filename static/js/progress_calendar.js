document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Flatpickr script loaded!");

    async function fetchProgressData() {
        try {
            let response = await fetch("/progress_calendar");
            if (!response.ok) throw new Error("❌ API request failed");

            let data = await response.json();
            console.log("✅ Progress data received:", data);

            // ハイライトする日付リスト
            let highlightDates = Object.keys(data);

            flatpickr("#calendar", {
                enable: highlightDates, // 進捗がある日付のみ選択可能にする
                dateFormat: "Y-m-d",
                locale: "ja",
                onChange: function(selectedDates, dateStr) {
                    if (data[dateStr]) {
                        alert(`📖 読書: ${data[dateStr].books_read || "なし"}\n🍎 栄養: ${data[dateStr].nutrition_status || "未記録"}`);
                    }
                }
            });

        } catch (error) {
            console.error("❌ Error loading progress data:", error);
        }
    }

    fetchProgressData();
});