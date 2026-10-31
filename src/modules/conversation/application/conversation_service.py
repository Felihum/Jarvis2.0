from src.modules.shared import Service, UseCase, ErrorChunk
from src.modules.conversation.domain.models import ConversationMessage, IntentionResponse
from config import NPC_CONFIGS, DEFAULT_NPC

class ConversationService(Service):

    def __init__(self, analyse_intention: UseCase, interaction_use_cases: list[UseCase]):
        self.analyze_intention = analyse_intention
        self.interaction_use_cases = {
            uc.interaction_type: uc.execute for uc in interaction_use_cases
        }

    def execute(self, user_query: list[ConversationMessage], npc_id: str):
        if not user_query:
            yield ErrorChunk(content="Campo query é obrigatório.")
            return

        npc_config = NPC_CONFIGS.get(npc_id, NPC_CONFIGS[DEFAULT_NPC])

        intention_response: IntentionResponse = self.analyze_intention.execute(user_query)

        yield from self.interaction_use_cases[intention_response.intention](
            user_query=user_query, 
            system_prompt=npc_config["system_prompt"], 
            intention_response=intention_response
        )