# automate_process.py — ULTIMAI v1.1
import os
import openai

# Получаем ключ из GitHub Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Обновлённый синтаксис SDK 1.0.0+
response = openai.chat.completions.create(
    model="gpt-4o",  # или "gpt-4-0613" при необходимости
    messages=[
        {"role": "system", "content": "Ты — Мыслящий архитектор саморазвивающейся экосистемы искусственного интеллекта."},
        {"role": "user", "content": "рассуди и предложи reasoning-патч к текущему reasoning-графу"}
    ]
)

# Выводим ответ
print(response.choices[0].message.content)
