from openai import OpenAI
from config import config

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=config.AI_API_KEY,
)

completion = client.chat.completions.create(
  model=config.AI_MODEL_NAME,
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?"
        },
      ]
    }
  ]
)
print(completion.choices[0].message.content)