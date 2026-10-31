from openai import OpenAI
from dotenv import load_dotenv
from src.modules.conversation.domain.models.conversation_models import ConversationMessage
from src.modules.conversation.domain.contracts.conversation_gateway import ConversationGateway
from .openai_config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MODEL_REASONING, OPENAI_MODEL_VERBOSITY

load_dotenv()

class OpenAIGateway(ConversationGateway):

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def stream_chat(self, messages: list[ConversationMessage]):
        print(f"\n\nOpenAIAdapter: Streaming chat with messages: {messages}\n\n")
        
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                formatted_messages.append({
                    "role": msg.get("role").value if hasattr(msg.get("role"), "value") else msg.get("role"),
                    "content": msg.get("content")
                })
            else:
                formatted_messages.append({
                    "role": msg.role.value,
                    "content": msg.content
                })

        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=formatted_messages,
            stream=True,
            temperature=1,
            max_completion_tokens=220,
            reasoning_effort=OPENAI_MODEL_REASONING,
            verbosity=OPENAI_MODEL_VERBOSITY
        )

        for chunk in response:
            if not chunk.choices:
                continue

            token = chunk.choices[0].delta.content

            if token:
                # Codifica a string para bytes antes de enviar pelo stream
                yield token
    
    def single_response(self, message, system, format):
        response = self.client.responses.create(
            model=OPENAI_MODEL,
            text={
                "format": format
            },
            instructions=system,
            input=message
        )

        return response