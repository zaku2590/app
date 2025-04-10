document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
  
    fetch("/get_progress_calendar")
      .then(res => res.json())
      .then(events => {
        const calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: "dayGridMonth",
          events: events,
          dateClick: function (info) {
            const dateStr = info.dateStr;
  
            // メモとポモ回数取得
            fetch(`/get_memo?date=${dateStr}`)
              .then(res => res.json())
              .then(data => {
                const memo = data.memo || "";
                const count = data.count || 0;
                openModal(dateStr, count, memo);
              });
          }
        });
        calendar.render();
      });
  });
  
  // モーダル操作用グローバル変数
  let selectedDate = null;
  
  function openModal(dateStr, currentCount, currentMemo) {
    selectedDate = dateStr;
    document.getElementById("memoModalDate").textContent = `📅 ${dateStr}`;
    document.getElementById("memoModalPomodoro").textContent = `ポモ回数: ${currentCount}`;
    document.getElementById("memoInput").value = currentMemo || "";
    document.getElementById("memoModal").style.display = "block";
  }
  
  function closeModal() {
    document.getElementById("memoModal").style.display = "none";
  }
  
  function saveMemo() {
    const memoText = document.getElementById("memoInput").value;
    fetch("/save_memo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        date: selectedDate,
        memo: memoText
      })
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
        closeModal();
        location.reload(); // 更新後にカレンダーを再描画
      });
  }
  