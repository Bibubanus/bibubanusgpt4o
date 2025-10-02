# automate_process.py — ULTIMAI v1.1 (обновлено под OpenAI SDK >=1.0.0)

import openai
import os
import sys

# Убедитесь, что у вас установлен openai>=1.0.0
# pip install --upgrade openai

# Получаем API-ключ из переменных окружения или GitHub Secrets
api_key = os.getenv("OPENAI_API_KEY")

# Validate API key exists
if not api_key:
    print("❌ Error: OPENAI_API_KEY environment variable is not set")
    sys.exit(1)

# Create OpenAI client with proper initialization (SDK >=1.0.0)
client = openai.OpenAI(api_key=api_key)

# 📂 Данные для reasoning (примеры)
reasoning_prompt = "Generate a reasoning patch for ULTIMAI memetic loop integrity."

# 🧠 Обновлённый синтаксис для chat/completions
try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a reasoning architect for a self-evolving AI ecosystem."},
            {"role": "user", "content": reasoning_prompt}
        ]
    )
except openai.APIError as e:
    print(f"❌ OpenAI API error: {e}")
    sys.exit(1)
except openai.RateLimitError as e:
    print(f"❌ Rate limit exceeded: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error during API call: {e}")
    sys.exit(1)

# 💾 Сохраняем результат
try:
    output_text = response.choices[0].message.content
    
    if not output_text:
        print("⚠️ Warning: Empty response from API")
        output_text = "No content generated"
    
    with open("REASONING_RESULT.md", "w", encoding="utf-8") as f:
        f.write("# 🧠 Auto-Generated Reasoning Patch\n\n")
        f.write(output_text)
    
    print("✅ REASONING_RESULT.md сгенерирован и готов к коммиту")
except IOError as e:
    print(f"❌ File write error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error during file write: {e}")
    sys.exit(1)
