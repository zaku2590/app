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

function fetchTodayPomodoroCount() {
  fetch("/get_progress_count")
    .then(res => res.json())
    .then(data => {
      pomodoroCount = data.count || 0;
      countDisplay.textContent = `現在 ${pomodoroCount} ポモドーロ`;
    });
}

function switchMode() {
  if (isWorkMode) {
    fetch("/record_progress", { method: "POST" })
      .then(res => {
        if (res.status === 401) {
          alert("⚠️ ログインしていないため記録されません。ログインしてください。");
          return;
        }
        return res.json();
      })
      .then(data => {
        if (data) {
          console.log("✅ 記録:", data);
          fetchTodayPomodoroCount();
        }
      });
  }

  isWorkMode = !isWorkMode;
  currentTime = isWorkMode ? workTime : breakTime;
  updateDisplay();
}

function startTimer() {
  if (isRunning) return;

  isRunning = true;
  startButton.classList.add("active");
  startButton.textContent = "⏳";

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
  startButton.classList.remove("active");
  startButton.textContent = "▶";
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
fetchTodayPomodoroCount();
