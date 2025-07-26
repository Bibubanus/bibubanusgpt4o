# automate_process.py — ULTIMAI v1.1 (обновлено под OpenAI SDK >=1.0.0)

import openai
import os

# Убедитесь, что у вас установлен openai>=1.0.0
# pip install --upgrade openai

# Получаем API-ключ из переменных окружения или GitHub Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📂 Данные для reasoning (примеры)
reasoning_prompt = "Generate a reasoning patch for ULTIMAI memetic loop integrity."

# 🧠 Обновлённый синтаксис для chat/completions
response = openai.chat.completions.create(
    model="gpt-4o",
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
