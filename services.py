import openai
import os

#dataにはpomodoroの回数やユーザーが記録した今日やったことのデータを渡す（仮）
def generate_response_onephrase(data):
    prompt = f"""
    本のタイトル:
    
    {data}
    上記の本の要約を1500〜2000文字で日本語で作成してください。
    もし内容がわからない場合は「その本の情報が見つかりませんでした」と返答してください。
    """

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "点数をつけるAIです"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"エラー: {str(e)}"
