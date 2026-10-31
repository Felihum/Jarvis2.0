from openai import OpenAI
from dotenv import load_dotenv

from .llm_adapter import LLMAdapter

load_dotenv()

class OpenAIAdapter(LLMAdapter):

    def __init__(self):
        self.client = OpenAI()

    def stream_chat(self, messages: list[dict], model: str):
        print(f"\n\nOpenAIAdapter: Streaming chat with model '{model}' and messages: {messages}\n\n")
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
            temperature=1,
            max_completion_tokens=220,
            reasoning_effort="none",
            verbosity="low"
        )

        for chunk in response:

            if not chunk.choices:
                continue

            token = chunk.choices[0].delta.content

            if token:
                yield token
    
    def single_response(self, message, system, model, format):
        response = self.client.responses.create(
            model=model,
            text={
                "format": format
            },
            instructions=system,
            input=message
        )

        return response