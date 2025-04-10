import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_response_score(data):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
    以下はユーザーの今日の活動記録です。

    🔢 ポモドーロ回数: {data['count']} 回
    📝 メモ内容: {data['memo']}

    この内容をもとに、以下のフォーマットで評価してください。

    コメント：◯◯◯
    評価：S / A / B / C / D
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたはやさしくユーザーの努力を採点するAIです。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"エラー: {str(e)}"


