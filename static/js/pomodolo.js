let workTime = 25 * 60;
let breakTime = 5 * 60;
let currentTime = workTime;
let timerInterval = null;
let isRunning = false;
let isWorkMode = true;

const timerDisplay = document.getElementById('timer');
const modeDisplay = document.getElementById('mode');
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const resetButton = document.getElementById('reset');

function updateDisplay() {
  const minutes = String(Math.floor(currentTime / 60)).padStart(2, '0');
  const seconds = String(currentTime % 60).padStart(2, '0');
  timerDisplay.textContent = `${minutes}:${seconds}`;
  modeDisplay.textContent = isWorkMode ? '作業中' : '休憩中';
}

function switchMode() {
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
      startTimer(); // 自動で次のモードを開始
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

updateDisplay(); // 初期表示
