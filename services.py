import openai
import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO

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

# 許可する拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# YOLOv8モデルのロード
model = YOLO("path/to/food-detection-model.pt")  # カスタムモデルを指定

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (640, 640))  # YOLOの推奨サイズ
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCVはBGR、YOLOはRGBを使用
    return img


# 食材と栄養素のマッピング（仮のデータ）
nutrition_data = {
    'apple': ['ビタミンC', '食物繊維'],
    'banana': ['カリウム', 'ビタミンB6'],
    'broccoli': ['ビタミンC', 'ビタミンK'],
    'milk': ['カルシウム', 'ビタミンD'],
    'fish': ['オメガ3', 'ビタミンD'],
    'omurice': ['炭水化物', 'たんぱく質'],
    'hamburger': ['たんぱく質', '鉄分'],
    'spaghetti': ['炭水化物', '食物繊維'],
}

food_suggestions = {
    'ビタミンC': ['オレンジ', 'パプリカ', 'ブロッコリー'],
    '鉄分': ['レバー', 'ほうれん草', '豆類'],
    'カルシウム': ['牛乳', 'チーズ', '小魚'],
    'カリウム': ['バナナ', 'じゃがいも', 'ほうれん草'],
    'オメガ3': ['魚', 'ナッツ', '亜麻仁油'],
    'ビタミンB6': ['鶏肉', 'バナナ', '玄米'],
    '食物繊維': ['玄米', 'さつまいも', 'ごぼう'],
    'ビタミンD': ['きのこ', '魚', '卵'],
}

def analyze_nutrition(image_path):
    img = preprocess_image(image_path)
    results = model(img)

    detected_foods = []
    for result in results:
        for box in result.boxes:
            food_item = model.names[int(box.cls)]
            if food_item not in detected_foods:
                detected_foods.append(food_item)

    if not detected_foods:
        detected_foods.append("食品が検出されませんでした")

    detected_nutrients = []
    for food in detected_foods:
        if food in nutrition_data:
            detected_nutrients.extend(nutrition_data[food])

    all_nutrients = set(food_suggestions.keys())
    missing_nutrients = list(all_nutrients - set(detected_nutrients))
    missing_food_suggestions = {nutrient: food_suggestions.get(nutrient, ["データなし"]) for nutrient in missing_nutrients}

    return {
        '検出された食品': detected_foods,
        '含まれる栄養素': list(set(detected_nutrients)),
        '不足している栄養素': missing_nutrients,
        '補うための食材': missing_food_suggestions
    }
