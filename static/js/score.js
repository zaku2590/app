
document.getElementById("scoreButton").addEventListener("click", () => {
    fetch("/score_today")
      .then(res => res.json())
      .then(data => {
        const result = data.result;
        const scoreMatch = result.match(/評価[:：]\s*([A-Z]+)/);
        const commentMatch = result.match(/コメント[:：]\s*(.+)/);

        const score = scoreMatch ? scoreMatch[1] : "？";
        const comment = commentMatch ? commentMatch[1] : "コメントなし";
  
        const scoreElem = document.getElementById("scoreNumber");
        const commentElem = document.getElementById("scoreComment");
        const tweetButton = document.getElementById("tweetButton");
  
        // スコアとコメントをセット
        scoreElem.textContent = score;
        commentElem.textContent = comment;
  
        // クラス設定（リセット→再設定）
        scoreElem.className = "";
        scoreElem.classList.add(score.toLowerCase());
  
        // 表示とアニメーション
        document.getElementById("resultBox").style.display = "block";
        scoreElem.style.animation = "none";
        void scoreElem.offsetWidth;
        scoreElem.style.animation = "growScore 1s forwards";
  
        commentElem.style.opacity = 0;
        setTimeout(() => {
          commentElem.style.opacity = 1;
        }, 1000);
  
        // Twitter共有リンク設定
        const tweetText = `📊今日の評価：${score}！\n🧠AIから一言：${comment}\n#ぽもログ #すき間ジム`;
        const tweetURL = "https://twitter.com/intent/tweet?text=" + encodeURIComponent(tweetText);
        tweetButton.href = tweetURL;
        tweetButton.style.display = "inline-block";
      });
  });
  