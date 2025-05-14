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
  const tweetComment = truncateComment(fullComment);  // ✅ ツイート用に短縮

  const scoreElem = document.getElementById("scoreNumber");
  const commentElem = document.getElementById("scoreComment");
  const tweetButton = document.getElementById("tweetButton");

  // ✅ 画面には全文を表示
  scoreElem.textContent = score;
  commentElem.textContent = fullComment;
  scoreElem.className = "score-rank " + score.toLowerCase();
  document.getElementById("resultBox").style.display = "block";

  // ✅ ツイートには短縮版コメントを使う
  const tweetText = `📊今日の評価：${score}！\n🧠AIから一言：${tweetComment}\n#ぽもログ #勉強垢`;
  const tweetURL = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(tweetText);
  tweetButton.href = tweetURL;
  tweetButton.style.display = "inline-block";

  // ✅ 共有時に200pt付与
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
    fetch("/score_today")
      .then(res => res.json())
      .then(data => {
        showScoreResult(data.result);
        scoreButton.style.display = "none";
      });
  });
});
