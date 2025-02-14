import openai
import os

def generate_response_book(book_title):
    prompt = f"""
    本のタイトル:
    {book_title}
    上記の本の要約を2000〜2500文字で日本語で作成してください。
    もし内容がわからない場合は「その本の情報が見つかりませんでした」と返答してください。
    """

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            # あなたは本の要約を2000〜2500文字で作成する日本語対応のAIです。
            messages=[
                {"role": "system", "content": "あなたは本に一言のキャッチコピーを作成する日本語対応のAIです。"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"エラー: {str(e)}"
