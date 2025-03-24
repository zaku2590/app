import openai
import os
import base64
import numpy as np


def generate_response_book(book_title):
    prompt = f"""
    本のタイトル:
    {book_title}
    上記の本の要約を1500〜2000文字で日本語で作成してください。
    もし内容がわからない場合は「その本の情報が見つかりませんでした」と返答してください。
    """

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            # あなたは本の要約を1500〜2000文字で作成する日本語対応のAIです。
            messages=[
                {"role": "system", "content": "あなたは本に一言のキャッチコピーを作成する日本語対応のAIです。"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"エラー: {str(e)}"

# 許可する拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image(image_path):
    """ 画像を Base64 にエンコード """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_food(image_path):
    base64_image = encode_image(image_path)
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは栄養の専門家です。画像内の食品を識別し、その栄養価をリストアップしてください。"},
                {"role": "user", "content": [
                    {"type": "text", "text": "1日の栄養素で足りないものを教えてください。またおすすめの料理も教えてください。"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=1000
        )

        # `content` が期待通りのフォーマットであるかチェック
        if not hasattr(response, "choices") or len(response.choices) == 0:
            print("🚨 API レスポンスが空または不正")
            return None

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"🚨 OpenAI API エラー: {str(e)}")  # ✅ API エラーを表示
        return None
