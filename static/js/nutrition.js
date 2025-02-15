document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("upload-form").addEventListener("submit", async function(event) {
        event.preventDefault();
        
        const formData = new FormData();
        const fileInput = document.getElementById("food-image");
        formData.append("food-image", fileInput.files[0]);
        
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        
        const result = await response.json();
        const resultWindow = document.getElementById("analysis-result");
        
        resultWindow.innerHTML = ""; // クリア

        if (result.message) {
            resultWindow.innerHTML += `<strong>${result.message}</strong><br>`;
        }
        if (result.result) {
            resultWindow.innerHTML += `<strong>検出された食品:</strong> ${result.result['検出された食品'].join(", ")}<br>`;
            resultWindow.innerHTML += `<strong>含まれる栄養素:</strong> ${result.result['含まれる栄養素'].join(", ")}<br>`;
            resultWindow.innerHTML += `<strong>不足している栄養素:</strong> ${result.result['不足している栄養素'].join(", ")}<br>`;
            
            let suggestions = "";
            for (let nutrient in result.result['補うための食材']) {
                suggestions += `<strong>${nutrient}:</strong> ${result.result['補うための食材'][nutrient].join(", ")}<br>`;
            }
            resultWindow.innerHTML += `<strong>補うための食材:</strong><br> ${suggestions}`;
        }
    });
});