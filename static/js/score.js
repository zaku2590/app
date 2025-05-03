function truncateComment(comment, maxLen = 90) {
  if (comment.length <= maxLen) return comment;

  // 「。」や「！」や「？」の直後で90文字以内の最長位置を探す
  const punctuation = ["。", "！", "？"];
  let cutPos = -1;
  for (const mark of punctuation) {
    const pos = comment.lastIndexOf(mark, maxLen);
    if (pos > cutPos) cutPos = pos + 1; // 句点の直後で切る
  }

  // 区切れる句読点が見つかった場合
  if (cutPos > 0) {
    return comment.substring(0, cutPos);
  }

  // それでもなければ強制的にカットして「…」追加
  return comment.substring(0, maxLen) + "…";
}

function showScoreResult(result) {
  const scoreMatch = result.match(/評価[:：]\s*([A-Z]+)/);
  const commentMatch = result.match(/コメント[:：]\s*(.+)/);

  const score = scoreMatch ? scoreMatch[1] : "？";
  let comment = commentMatch ? commentMatch[1] : "コメントなし";

  // ✅ コメントを自然な位置で最大90文字に制限
  comment = truncateComment(comment);

  const scoreElem = document.getElementById("scoreNumber");
  const commentElem = document.getElementById("scoreComment");
  const tweetButton = document.getElementById("tweetButton");

  scoreElem.textContent = score;
  commentElem.textContent = comment;
  scoreElem.className = "score-rank " + score.toLowerCase();
  document.getElementById("resultBox").style.display = "block";

  const tweetText = `📊今日の評価：${score}！\n🧠AIから一言：${comment}\n#ぽもログ #すき間ジム`;
  const tweetURL = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(tweetText);
  tweetButton.href = tweetURL;
  tweetButton.style.display = "inline-block";
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
