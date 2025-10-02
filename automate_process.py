# automate_process.py — ULTIMAI v1.1 (обновлено под OpenAI SDK >=1.0.0)

from openai import OpenAI
import os
import sys

# Убедитесь, что у вас установлен openai>=1.0.0
# pip install --upgrade openai

# Получаем API-ключ из переменных окружения или GitHub Secrets
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ Отсутствует переменная окружения OPENAI_API_KEY")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# 📂 Данные для reasoning (примеры)
reasoning_prompt = "Generate a reasoning patch for ULTIMAI memetic loop integrity."

# 🧠 Обновлённый синтаксис для chat/completions (OpenAI SDK v1)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a reasoning architect for a self-evolving AI ecosystem."},
        {"role": "user", "content": reasoning_prompt}
    ]
)

# 💾 Сохраняем результат
output_text = response.choices[0].message.content

with open("REASONING_RESULT.md", "w", encoding="utf-8") as f:
    f.write("# 🧠 Auto-Generated Reasoning Patch\n\n")
    f.write(output_text)

print("✅ REASONING_RESULT.md сгенерирован и готов к коммиту")
