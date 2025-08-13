from openai import AsyncOpenAI
from schemas.user import User
from config import config
from llm.prompt import PromptManager
from exceptions import AIRequestError


class AIClient:
    CLIENT = AsyncOpenAI(api_key=config.AI_API_KEY,
                         base_url="https://openrouter.ai/api/v1",
                         max_retries=config.AI_API_MAX_RETRIES)
    MODEL = config.AI_MODEL_NAME

    @classmethod
    async def _create_text_response(cls, prompt: str) -> str:
        """
        Short-cut function for getting response
        from ai client using text.
        Returns client's answer text.
        """
        # making a request
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
        # extracting the response
        response = completion.choices[0].message.content
        if response:
            return response
        raise AIRequestError(f"AI couldn't provide any answer to the request:\n{prompt[:200]}...")

    @classmethod
    async def generate_user_plan(cls, 
                                 user: User, 
                                 extra: str | None) -> str:
        """
        Generate training plan for the user using
        their data.
        """
        prompt = PromptManager.get_plan_prompt(user, extra)
        response = await cls._create_text_response(prompt)
        return response
    
    @classmethod
    async def generate_user_response(cls, 
                                     user: User, 
                                     user_request: str | None) -> str:
        """
        Generate a general response for user request.

        User can ask questions, ask for help,
        guidance, etc.
        """
        prompt = PromptManager.get_user_request_prompt(user, user_request)
        response = await cls._create_text_response(prompt)
        return response
