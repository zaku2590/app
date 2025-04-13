document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  const toggleBtn = document.getElementById('toggleVisibilityBtn');
  const userSearchInput = document.getElementById('userSearchInput');
  const resetCalendarButton = document.getElementById('resetCalendarButton');

  let calendar = null;

  function updateToggleButton(isPublic) {
    toggleBtn.textContent = isPublic
      ? "🔓 公開中（クリックで非公開）"
      : "🔒 非公開中（クリックで公開）";

    toggleBtn.classList.remove("btn-public", "btn-private");
    toggleBtn.classList.add(isPublic ? "btn-public" : "btn-private");
  }

  fetch("/get_visibility_status")
    .then(res => res.json())
    .then(data => {
      updateToggleButton(data.is_public);
    });

  toggleBtn.addEventListener("click", () => {
    fetch("/toggle_calendar_visibility", { method: "POST" })
      .then(res => {
        if (res.status === 401) {
          alert("ログインが必要です");
          return;
        }
        return res.json();
      })
      .then(data => {
        if (data && "is_public" in data) {
          updateToggleButton(data.is_public);
          alert("公開設定を更新しました");
        }
      });
  });

  function renderCalendar(events, readOnly = false, username = null) {
    if (calendar) calendar.destroy(); // 🔁 前回のカレンダーを破棄

    calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      events: events,
      dateClick: function (info) {
        const dateStr = info.dateStr;
        let url = `/get_memo?date=${dateStr}`;
        if (readOnly && username) url += `&username=${username}`;

        fetch(url)
          .then(res => res.json())
          .then(data => {
            openModal(dateStr, data.count || 0, data.memo || "", readOnly);
          });
      }
    });

    calendar.render();
  }

  fetch("/get_progress_calendar")
    .then(res => res.json())
    .then(events => {
      console.log("📅 自分のイベント一覧:", events);
      renderCalendar(events, false);
    });

  document.getElementById("userSearchButton").addEventListener("click", loadCalendarForUser);

  function loadCalendarForUser() {
    const username = userSearchInput.value.trim();
    if (!username) return;

    fetch(`/get_progress_calendar?username=${username}`)
      .then(res => res.json())
      .then(events => {
        console.log("🔍 他人のイベント一覧:", events);
        renderCalendar(events, true, username);
        resetCalendarButton.style.display = "inline-block";
        toggleBtn.style.display = "none"; // 他人の時は非表示
      });
  }

  resetCalendarButton.addEventListener("click", () => {
    userSearchInput.value = "";
    resetCalendarButton.style.display = "none";

    fetch("/get_progress_calendar")
      .then(res => res.json())
      .then(events => {
        renderCalendar(events, false);
        toggleBtn.style.display = "inline-block"; // 自分に戻ると表示
      });
  });
});

let selectedDate = null;

function openModal(dateStr, currentCount, currentMemo, readOnly = false) {
  selectedDate = dateStr;
  document.getElementById("memoModalDate").textContent = `📅 ${dateStr}`;
  document.getElementById("memoModalPomodoro").textContent = `ポモ回数: ${currentCount}`;
  document.getElementById("memoInput").value = currentMemo || "";
  document.getElementById("memoInput").readOnly = readOnly;

  const buttons = document.querySelector(".modal-buttons");
  buttons.innerHTML = "";

  if (!readOnly) {
    buttons.innerHTML = `
      <button onclick="saveMemo()">💾 保存</button>
      <button onclick="closeModal()">✖ 閉じる</button>
    `;
  } else {
    buttons.innerHTML = `
      <button onclick="closeModal()">✖ 閉じる</button>
    `;
  }

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
      location.reload();
    });
}
