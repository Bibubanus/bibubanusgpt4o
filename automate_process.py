# automate_process.py — ULTIMAI v1.1 (обновлено под OpenAI SDK >=1.0.0)

import openai
import os
import sys
from pathlib import Path

# Убедитесь, что у вас установлен openai>=1.0.0
# pip install --upgrade openai

def main():
    """Main function with proper error handling and security measures."""
    # Получаем API-ключ из переменных окружения или GitHub Secrets
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Security: Validate API key exists and is not empty
    if not api_key or not api_key.strip():
        print("❌ Error: OPENAI_API_KEY environment variable is not set or empty")
        sys.exit(1)
    
    # Initialize OpenAI client with proper error handling
    try:
        client = openai.OpenAI(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing OpenAI client: {e}")
        sys.exit(1)

    # 📂 Данные для reasoning (примеры)
    reasoning_prompt = "Generate a reasoning patch for ULTIMAI memetic loop integrity."

    try:
        # 🧠 Обновлённый синтаксис для chat/completions
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a reasoning architect for a self-evolving AI ecosystem."},
                {"role": "user", "content": reasoning_prompt}
            ],
            max_tokens=2000,  # Add reasonable limits
            temperature=0.7
        )

        # 💾 Сохраняем результат с proper error handling
        output_text = response.choices[0].message.content
        
        if not output_text:
            print("⚠️ Warning: Empty response from OpenAI API")
            output_text = "No content generated."
        
        # Use pathlib for safer file operations
        output_file = Path("REASONING_RESULT.md")
        
        with output_file.open("w", encoding="utf-8") as f:
            f.write("# 🧠 Auto-Generated Reasoning Patch\n\n")
            f.write(output_text)

        print("✅ REASONING_RESULT.md сгенерирован и готов к коммиту")
        
    except openai.APIError as e:
        print(f"❌ OpenAI API Error: {e}")
        sys.exit(1)
    except openai.RateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        sys.exit(1)
    except openai.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"❌ File operation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
