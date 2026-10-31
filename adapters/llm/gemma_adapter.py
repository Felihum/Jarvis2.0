import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .llm_adapter import LLMAdapter

load_dotenv()

class GemmaAdapter(LLMAdapter):

    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def stream_chat(self, messages: list[dict], model: str):
        print(f"\n\nGemmaAdapter: Streaming chat with model '{model}'\n\n")
        
        contents = []
        for msg in messages:
            role = msg["role"]
            if role == "assistant":
                role = "model"
            elif role == "system":
                continue
            
            # Criando objetos tipados conforme exigido pelo SDK
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        response = self.client.models.generate_content_stream(
            model=model,
            contents=contents
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text
    
    def single_response(self, message: list[dict], system: str, model: str, format: dict):
        contents = []
        for msg in message:
            role = msg["role"]
            if role == "assistant":
                role = "model"
            elif role == "system":
                continue
            
            # Criando objetos tipados conforme exigido pelo SDK
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        config = types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json"
        )

        if format and "schema" in format:
            schema_copy = format["schema"].copy()
            schema_copy.pop("additionalProperties", None)
            schema_copy.pop("additional_properties", None)
            config.response_schema = schema_copy

        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )

        class GemmaResponse:
            def __init__(self, text):
                self.output_text = text

        return GemmaResponse(response.text)