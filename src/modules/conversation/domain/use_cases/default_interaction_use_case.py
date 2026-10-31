from src.modules.shared import InteractionType, UseCase, DoneChunk, MetricChunk, TokenChunk
from src.modules.conversation.domain.contracts import ConversationGateway
from src.modules.conversation.domain.models import ConversationRoleEnum, ConversationMessage, IntentionResponse
import time

class DefaultInteractionUseCase(UseCase):

    interaction_type = InteractionType.DEFAULT.value
    
    def __init__(self, conversation_gateway: ConversationGateway):
        self.conversation_gateway = conversation_gateway

    def execute(self, user_query: list[ConversationMessage], system_prompt: str, intention_response: IntentionResponse = None):
        messages = [
            ConversationMessage(role=ConversationRoleEnum.SYSTEM, content=system_prompt)
        ] + user_query

        stream = self.conversation_gateway.stream_chat(messages=messages)
        
        first_token_sent = False

        for token in stream:
            if not first_token_sent:
                first_token_sent = True
                yield MetricChunk(name='first_token_at', value=time.time())

            print(token, end="", flush=True)
            yield TokenChunk(content=token)

        yield DoneChunk()