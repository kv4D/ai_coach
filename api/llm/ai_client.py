from openai import AsyncOpenAI
from schemas.user import User
from config import config
from llm.prompt import PromptManager


class AIClient:
    CLIENT = AsyncOpenAI(api_key=config.AI_API_KEY,
                         base_url="https://openrouter.ai/api/v1")
    MODEL = config.AI_MODEL_NAME

    @classmethod
    async def _create_text_response(cls, prompt: str) -> str:
        """
        Short-cut function for getting response
        from ai client using text.
        Returns client's answer text.
        """
        completion = await cls.CLIENT.chat.completions.create(
            model=config.AI_MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": prompt},
                        ]
                    }
                ]
            )
        # TODO: should add some exception catching
        response = completion.choices[0].message.content
        if response:
            return response
        # TODO: should raise something
        return "К сожалению, ИИ не смог предоставить ответ"
    
    @classmethod
    async def generate_user_plan(cls, user: User):
        """
        Generate training plan for the user using
        his data.
        """
        prompt = PromptManager.get_plan_prompt(user)
        response = await cls._create_text_response(prompt)
        return response
    
    @classmethod
    async def generate_user_response(cls, user: User, user_request: str | None):
        """
        Generate response for user request.
        User can ask question, ask for help,
        guidance, etc.
        """
        prompt = PromptManager.get_user_request_prompt(user, user_request)
        response = await cls._create_text_response(prompt)
        return response
