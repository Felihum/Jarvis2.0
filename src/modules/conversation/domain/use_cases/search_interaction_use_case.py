from src.modules.shared import InteractionType, UseCase, DoneChunk, MetricChunk, TokenChunk, FilesChunk
from src.modules.conversation.domain.contracts.conversation_gateway import ConversationGateway
from src.modules.conversation.domain.models import ConversationRoleEnum, IntentionResponse, ConversationMessage
import time

class SearchInteractionUseCase(UseCase):

    interaction_type = InteractionType.SEARCH.value
    
    def __init__(self, conversation_gateway: ConversationGateway, bert_service):
        self.conversation_gateway = conversation_gateway
        self.bert_service = bert_service

    def execute(self, user_query: list[ConversationMessage], system_prompt: str, intention_response: IntentionResponse):
        last_message = ConversationMessage(**user_query[-1])
        user_content = last_message.content.strip()
        
        query_results = self.bert_service.search_query_fast(
            query=intention_response.context,
            chunks_num=4,
        )

        contexts = query_results.get("context", [])
        filenames = query_results.get("filenames", [])
        titles = query_results.get("titles", [])

        context_text = ""

        for context in contexts:
            title = context.get("title", "")
            filename = context.get("filename", "")
            page = context.get("page", "")
            chunk = context.get("chunk", "")

            context_text += f"[Fonte: {title} | Arquivo: {filename} | Página: {page}\n"
            context_text += f"{chunk}\n\n"

        prompt = f"""
            {system_prompt}

            ### CONTEXTO RECUPERADO DA BASE:
            {context_text}

            ### DISSERTAÇÕES/TÍTULOS ENCONTRADOS:
            {", ".join(titles)}

            ### PERGUNTA DO USUÁRIO:
            {user_content}

            ### REGRAS DE RESPOSTA:
            - Responda em português do Brasil.
            - Seja claro, natural e adequado para uma NPC em realidade virtual.
            - Responda de forma objetiva, preferencialmente em até 3 parágrafos.
            - Use apenas o contexto recuperado quando falar das dissertações.
            - Cite os títulos ou arquivos encontrados quando forem relevantes.
            - Se o contexto não for suficiente, diga que não encontrou informação suficiente na base.
            - Não invente autores, títulos, páginas ou arquivos.
            - Quando houver dissertações, informe que o usuário pode clicar nelas para ver mais detalhes.
        """

        messages = [
            {"role": ConversationRoleEnum.SYSTEM, "content": system_prompt},
            {"role": ConversationRoleEnum.USER, "content": prompt}
        ]

        yield FilesChunk(filenames)

        stream = self.conversation_gateway.stream_chat(messages=messages)
                
        first_token_sent = False

        for token in stream:
            if not first_token_sent:
                first_token_sent = True
                yield MetricChunk(name='first_token_at', value=time.time())

            print(token, end="", flush=True)
            yield TokenChunk(content=token)

        yield DoneChunk()