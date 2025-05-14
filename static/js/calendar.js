document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  const toggleBtn = document.getElementById('toggleVisibilityBtn');
  const userSearchInput = document.getElementById('userSearchInput');
  const resetCalendarButton = document.getElementById('resetCalendarButton');
  const supportButton = document.getElementById('supportButton');
  const supportAmountInput = document.getElementById('supportAmount');
  const errorBox = document.getElementById("searchError");

  let calendar = null;
  let selectedUsername = null;

  function updateToggleButton(isPublic) {
    toggleBtn.textContent = isPublic
      ? "🔓 公開中（クリックで非公開）"
      : "🔒 非公開中（クリックで公開）";

    toggleBtn.classList.remove("btn-public", "btn-private");
    toggleBtn.classList.add(isPublic ? "btn-public" : "btn-private");
  }

  fetch("/get_visibility_status")
    .then(res => res.json())
    .then(data => updateToggleButton(data.is_public));

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
    if (calendar) calendar.destroy();
    selectedUsername = username;

    calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: "dayGridMonth",
      events: events,
      height: 'auto',
      dateClick: function (info) {
        const dateStr = info.dateStr;
        let url = `/get_memo?date=${dateStr}`;
        if (readOnly && username) url += `&username=${username}`;

        fetch(url)
          .then(res => res.json())
          .then(data => openModal(dateStr, data.count || 0, data.memo || "", readOnly));
      }
    });

    calendar.render();
  }

  fetch("/get_progress_calendar")
    .then(res => res.json())
    .then(events => renderCalendar(events, false));

  document.getElementById("userSearchButton").addEventListener("click", loadCalendarForUser);

  function loadCalendarForUser() {
    const username = userSearchInput.value.trim();
    errorBox.textContent = "";
    if (!username) return;

    fetch(`/get_progress_calendar?username=${username}`)
      .then(res => {
        if (!res.ok) {
          return res.json().then(err => {
            throw new Error(err.error || "エラーが発生しました");
          });
        }
        return res.json();
      })
      .then(events => {
        renderCalendar(events, true, username);
        resetCalendarButton.style.display = "inline-block";
        toggleBtn.style.display = "none";
        supportButton.style.display = "inline-block";
        supportAmountInput.style.display = "inline-block";
      })
      .catch(error => {
        errorBox.textContent = "❌ " + error.message;
      });
  }

  resetCalendarButton.addEventListener("click", () => {
    userSearchInput.value = "";
    errorBox.textContent = "";
    resetCalendarButton.style.display = "none";
    supportButton.style.display = "none";
    supportAmountInput.style.display = "none";

    fetch("/get_progress_calendar")
      .then(res => res.json())
      .then(events => {
        renderCalendar(events, false);
        toggleBtn.style.display = "inline-block";
      });
  });

  supportButton.addEventListener("click", () => {
    if (!selectedUsername) return;

    const amount = parseInt(supportAmountInput.value);
    if (!amount || amount <= 0) {
      alert("1以上のポイント数を入力してください。");
      return;
    }

    fetch("/support_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ to_username: selectedUsername, amount: amount })
    })
      .then(res => res.json())
      .then(data => alert(data.message))
      .catch(err => alert("エラー: " + err));
  });
});

let selectedDate = null;

function openModal(dateStr, currentCount, currentMemo, readOnly = false) {
  selectedDate = dateStr;
  document.getElementById("memoModalDate").textContent = `📅 ${dateStr}`;
  document.getElementById("memoModalPomodoro").textContent = `ポモ回数:${currentCount}`;
  document.getElementById("memoInput").value = currentMemo || "";
  document.getElementById("memoInput").readOnly = readOnly;

  const buttons = document.querySelector(".modal-buttons");
  buttons.innerHTML = "";

  const closeBtn = document.createElement("button");
  closeBtn.textContent = "✖ 閉じる";
  closeBtn.onclick = closeModal;

  if (!readOnly) {
    const saveBtn = document.createElement("button");
    saveBtn.textContent = "💾 保存";
    saveBtn.onclick = saveMemo;
    buttons.appendChild(saveBtn);
  }

  buttons.appendChild(closeBtn);

  const modal = document.getElementById("memoModal");
  modal.style.display = "flex";
}

function closeModal() {
  document.getElementById("memoModal").style.display = "none";
}

function saveMemo() {
  const memoText = document.getElementById("memoInput").value;
  fetch("/save_memo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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
