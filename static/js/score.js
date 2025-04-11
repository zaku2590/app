window.addEventListener("DOMContentLoaded", () => {
  fetch("/score_today")
    .then(res => res.json())
    .then(data => {
      if (data.result && !data.result.includes("まだ記録がありません")) {
        showScoreResult(data.result);
        document.getElementById("scoreButton").style.display = "none";
      }
    });
});

document.getElementById("scoreButton").addEventListener("click", () => {
  fetch("/score_today")
    .then(res => res.json())
    .then(data => {
      showScoreResult(data.result);
      document.getElementById("scoreButton").style.display = "none";
    });
});

function showScoreResult(result) {
  const scoreMatch = result.match(/評価[:：]\s*([A-Z]+)/);
  const commentMatch = result.match(/コメント[:：]\s*(.+)/);

  const score = scoreMatch ? scoreMatch[1] : "？";
  const comment = commentMatch ? commentMatch[1] : "コメントなし";

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
