from ollama import chat

from .llm_adapter import LLMAdapter


class OllamaAdapter(LLMAdapter):

    def stream_chat(self, messages: list[dict], model: str):
        print(f"\n\nOllamaAdapter: Streaming chat with model '{model}' and messages: {messages}\n\n")
        response = chat(
            model=model,
            messages=messages,
            stream=True,
            keep_alive="30m",
            options={
                "temperature": 0.3,
                "num_ctx": 4096
            }
        )

        for chunk in response:

            if (
                chunk
                and chunk.message
                and chunk.message.content
            ):
                yield chunk.message.content


    def single_response(self, message, system, model, format):
        return super().single_response(message, system, model, format)