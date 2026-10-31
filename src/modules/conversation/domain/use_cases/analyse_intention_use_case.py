from src.modules.shared import UseCase, InteractionType
from src.modules.conversation.domain.contracts import ConversationGateway
from src.modules.conversation.domain.models import IntentionResponse
import os
import json

class AnalyseIntentionUseCase(UseCase):

    def __init__(self, conversation_gateway: ConversationGateway):
        self.conversation_gateway = conversation_gateway

    def execute(self, messages) -> IntentionResponse:        
        response = self.conversation_gateway.single_response(
            message=messages,
            system="""
                # ROLE
                Você é um classificador de intenções especializado em filtragem de consultas para um banco de dados de dissertações de mestrado.

                # TASK
                Analíse a entrada do usuário e determine se ele deseja realizar uma consulta de dissertações sobre um assunto acadêmico.

                # REGRAS CRÍTICAS
                1. Para identificar se o usuário deseja realizar uma consulta, analíse todo o contexto, buscando entender se o rumo da conversa leva a essa intenção.
                2. Se o assunto for irrelevante ou o usuário não pedir uma consulta de forma clara, a intenção deve ser "none".
                3. SAÍDA RESTRITA: Responda exclusivamente em formato JSON. Não adicione saudações, explicações ou qualquer texto fora do bloco JSON.

                # FORMATO DE SAÍDA
                {"intention": """ + InteractionType.SEARCH.value + """ | """ + InteractionType.DEFAULT.value + """, "context": "assunto extraído ou null"}

                # EXEMPLOS
                - Usuário: "Gostaria de ver dissertações sobre redes neurais."
                Resposta: {"intention": """ + InteractionType.SEARCH.value + """, "context": "redes neurais"}

                - Usuário: "Estou trabalhando em um projeto de pesquisa sobre aprendizado de máquina."
                - Assistente: "Que legal! Você gostaria de ver dissertações relacionadas a aprendizado de máquina?"
                - Usuário: "Sim."
                Resposta: {"intention": """ + InteractionType.SEARCH.value + """,, "context": "aprendizado de máquina"}

                - Usuário: "Como está o clima hoje?"
                Resposta: {"intention": """ + InteractionType.DEFAULT.value + """, "context": null}

                - Usuário: "Quero pesquisar trabalhos sobre Machado de Assis."
                Resposta: {"intention": """ + InteractionType.SEARCH.value + """, "context": "Machado de Assis"}
            """,
            format={
                "type": "json_schema",
                "name": "intention_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "intention": {
                            "type": "string"
                        },
                        "context": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "intention",
                        "context"
                    ],
                    "additionalProperties": False
                }
            }
        )

        return IntentionResponse(**json.loads(response.output_text))