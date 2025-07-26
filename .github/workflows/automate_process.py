# automate_process.py — ULTIMAI v2.4 (безопасная генерация JS)
import os
import sys
import openai
from datetime import datetime
import json

def escape_js(s):
    # Безопасно экранирует строку для вставки в JS (XSS mitigation)
    return json.dumps(s, ensure_ascii=False)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[ERROR] Не найден OPENAI_API_KEY. Добавьте секрет в настройки GitHub Actions или переменную окружения.")
    sys.exit(1)

openai.api_key = api_key

model_name = os.getenv("OPENAI_MODEL", "gpt-4o")

response = openai.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "Ты — Мыслящий архитектор саморазвивающейся экосистемы искусственного интеллекта."},
        {"role": "user", "content": "рассуди и предложи reasoning-патч к текущему reasoning-графу"}
    ]
)

result = response.choices[0].message.content

now_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
filename_md = f"output/reasoning_patch_{now_str}.md"

os.makedirs("output", exist_ok=True)
with open(filename_md, "w", encoding="utf-8") as f:
    f.write(result)

# Безопасная генерация JS-файла (шаблонизация через json.dumps, экранирование XSS)
with open("docs/reasoning_patch.js", "w", encoding="utf-8") as js_file:
    js_file.write(f'document.getElementById("output").textContent = {escape_js(result)};\n')
