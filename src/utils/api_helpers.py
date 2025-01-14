from openai import OpenAI
from config import settings  # Relative import from current directory

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_completion(prompt: str, model: str = "gpt-4-turbo-preview") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating completion: {e}")
        return None