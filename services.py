import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_response_score(data):
    count = data["count"]
    memo = data["memo"]

    # 回数に応じたランク
    if count >= 15:
        grade = "SSS"
    elif count >= 12:
        grade = "SS"
    elif count >= 9:
        grade = "S"
    elif count >= 6:
        grade = "A"
    elif count >= 3:
        grade = "B"
    elif count >= 1:
        grade = "C"
    else:
        grade = "D"

    # コメントはOpenAIで優しい一言を生成
    prompt = f"""
    今日のポモドーロ回数は {count} 回、以下のメモがありました：
    「{memo}」

    以下の評価ランクとメモに基づいて、ユーザーの努力を優しく応援してください：

    🔥 評価ランク: {grade}

    フォーマット：
    コメント：◯◯◯
    評価：{grade}
    """

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたはやさしくユーザーの努力を評価するAIです。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"エラー: {str(e)}"

