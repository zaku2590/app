let workTime = 25 * 60;
let breakTime = 5 * 60;
let currentTime = workTime;
let timerInterval = null;
let isRunning = false;
let isWorkMode = true;
let pomodoroCount = 0;

const timerDisplay = document.getElementById('timer');
const modeDisplay = document.getElementById('mode');
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const resetButton = document.getElementById('reset');
const countDisplay = document.getElementById('pomodoro-count');

function updateDisplay() {
  const minutes = String(Math.floor(currentTime / 60)).padStart(2, '0');
  const seconds = String(currentTime % 60).padStart(2, '0');
  timerDisplay.textContent = `${minutes}:${seconds}`;
  modeDisplay.textContent = isWorkMode ? '作業中' : '休憩中';
}

function switchMode() {
  if (!isWorkMode) {
    pomodoroCount++;
    countDisplay.textContent = `現在 ${pomodoroCount} ポモドーロ`;

    // ✅ 自動で進捗を記録する
    fetch("/record_progress", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        console.log("記録:", data);
        alert(`✅ 作業完了！\n${data.message}（${data.count}回目）`);
      })
      .catch(err => {
        console.error("記録エラー:", err);
        alert("⚠️ 記録に失敗しました。ログインしているか確認してください。");
      });
  }

  isWorkMode = !isWorkMode;
  currentTime = isWorkMode ? workTime : breakTime;
  updateDisplay();
}

function startTimer() {
  if (isRunning) return;
  isRunning = true;
  timerInterval = setInterval(() => {
    if (currentTime > 0) {
      currentTime--;
      updateDisplay();
    } else {
      clearInterval(timerInterval);
      isRunning = false;
      switchMode();
      startTimer();
    }
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
  isRunning = false;
}

function resetTimer() {
  stopTimer();
  currentTime = isWorkMode ? workTime : breakTime;
  updateDisplay();
}

startButton.addEventListener('click', startTimer);
stopButton.addEventListener('click', stopTimer);
resetButton.addEventListener('click', resetTimer);

updateDisplay();
