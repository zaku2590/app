document.getElementById("user-info-form").addEventListener("submit", function(event) {
    event.preventDefault(); // フォームの送信を防ぐ

    // 入力値を取得
    var gender = document.getElementById("gender-input").value || "未入力";
    var age = document.getElementById("age-input").value || "未入力";
    var relationship = document.getElementById("relationship-input").value || "未入力";

    // ツールチップ内の内容を更新
    document.getElementById("tooltip-gender").textContent = gender;
    document.getElementById("tooltip-age").textContent = age;
    document.getElementById("tooltip-relationship").textContent = relationship;
});
