function truncateComment(comment, maxLen = 90) {
  if (comment.length <= maxLen) return comment;

  const punctuation = ["。", "！", "？"];
  let cutPos = -1;
  for (const mark of punctuation) {
    const pos = comment.lastIndexOf(mark, maxLen);
    if (pos > cutPos) cutPos = pos + 1;
  }

  if (cutPos > 0) {
    return comment.substring(0, cutPos);
  }

  return comment.substring(0, maxLen) + "…";
}

function showScoreResult(result) {
  const scoreMatch = result.match(/評価[:：]\s*([A-Z]+)/);
  const commentMatch = result.match(/コメント[:：]\s*(.+)/);

  const score = scoreMatch ? scoreMatch[1] : "？";
  const fullComment = commentMatch ? commentMatch[1] : "コメントなし";
  const tweetComment = truncateComment(fullComment);

  const scoreElem = document.getElementById("scoreNumber");
  const commentElem = document.getElementById("scoreComment");
  const tweetButton = document.getElementById("tweetButton");

  scoreElem.textContent = score;
  commentElem.textContent = fullComment;
  scoreElem.className = "score-rank " + score.toLowerCase();
  document.getElementById("resultBox").style.display = "block";

  const tweetText = `📊今日の評価：${score}！\n🧠AIから一言：${tweetComment}\n#ぽもログ #勉強垢`;
  const tweetURL = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(tweetText);
  tweetButton.href = tweetURL;
  tweetButton.style.display = "inline-block";

  tweetButton.addEventListener("click", () => {
    fetch("/shared_on_x", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        alert(data.message);
      });
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const isLoggedIn = (typeof IS_LOGGED_IN !== "undefined") && IS_LOGGED_IN === true;
  const scoreButton = document.getElementById("scoreButton");
  const spinner = document.createElement("span");
  spinner.classList.add("spinner");
  spinner.style.marginLeft = "12px";

  if (!isLoggedIn) {
    scoreButton.addEventListener("click", () => {
      alert("採点にはログインが必要です。ログイン後に再度お試しください。");
    });
    return;
  }

  fetch("/score_today")
    .then(res => res.json())
    .then(data => {
      if (data.result && !data.result.includes("まだ記録がありません")) {
        showScoreResult(data.result);
        scoreButton.style.display = "none";
      }
    });

  scoreButton.addEventListener("click", () => {
    scoreButton.disabled = true;
    scoreButton.textContent = "🧠 採点中...";
    scoreButton.appendChild(spinner);

    fetch("/score_today")
      .then(res => res.json())
      .then(data => {
        showScoreResult(data.result);
        scoreButton.style.display = "none";
      })
      .catch(error => {
        alert("エラーが発生しました：" + error.message);
        scoreButton.disabled = false;
        scoreButton.textContent = "🧠 採点する";
        spinner.remove();
      });
  });
});
